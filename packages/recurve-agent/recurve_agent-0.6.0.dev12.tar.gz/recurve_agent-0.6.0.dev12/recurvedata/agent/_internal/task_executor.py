import asyncio
import base64
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

from .schemas import TaskItem, TaskStatus, UpdateTaskInstanceStatus
from .utils import utcnow

if TYPE_CHECKING:
    from .client import AgentClient


class TaskExecutor:
    def __init__(
        self,
        client: "AgentClient",
        task_heartbeat_interval: int = 5,
        task_retry_interval: int = 5,
    ):
        self.client = client
        self.task_heartbeat_interval = task_heartbeat_interval
        self.task_retry_interval = task_retry_interval

    async def execute(self, task: "TaskItem") -> None:
        start_time = time.time()
        with tempfile.TemporaryDirectory() as temp_dir:
            await self.client.update_task_status(
                task.task_instance_id,
                UpdateTaskInstanceStatus(
                    status=TaskStatus.RUNNING,
                    logs=[f"{utcnow()} | Task {task.task_instance_id} started in working directory: {temp_dir}"],
                ),
            )

            logger.info(f"Task {task.task_instance_id} started in working directory: {temp_dir}")
            await self._execute_in_tempdir(task, temp_dir)

        logger.info(f"Task {task.task_instance_id} completed in {time.time() - start_time:.2f} seconds.")

    async def _execute_in_tempdir(self, task: "TaskItem", workdir: str):
        task_instance_id = task.task_instance_id
        retries = 0

        cmd_args, output_file = self._prepare_execution_context(task, workdir)

        while retries <= task.max_retries:
            task_event = asyncio.Event()
            task_event.clear()
            log_queue = asyncio.Queue()

            # the heartbeat task keeps sending the task status and logs to the server
            heartbeat_task = asyncio.create_task(self.send_heartbeat(task_instance_id, task_event, log_queue))

            try:
                logger.info(f"Executing task: {task_instance_id} (Attempt {retries + 1})")
                await log_queue.put(f"{utcnow()} | Attempt {retries + 1}")

                await self.execute_in_subprocess(
                    *cmd_args,
                    cwd=workdir,
                    log_queue=log_queue,
                    timeout=task.max_duration,
                )

                # success, read result and update status
                result = None
                if output_file.exists():
                    result = json.loads(output_file.read_text())

                logger.info(f"Task {task_instance_id} completed successfully.")

                await self.client.update_task_status(
                    task_instance_id,
                    UpdateTaskInstanceStatus(
                        status=TaskStatus.SUCCESS,
                        result=result,
                        logs=await self.drain_queue(log_queue),
                    ),
                )
                break
            except (subprocess.CalledProcessError, TimeoutError) as e:
                retries += 1
                logger.error(f"Attempt {retries} failed: {e}")
                await log_queue.put(f"{utcnow()} | Attempt {retries} failed: {e}")
                if retries > task.max_retries:
                    await self.client.update_task_status(
                        task_instance_id,
                        UpdateTaskInstanceStatus(
                            status=TaskStatus.FAILED,
                            logs=await self.drain_queue(log_queue),
                        ),
                    )
                    task_event.set()
                    await heartbeat_task
                    return

                await asyncio.sleep(self.task_retry_interval)

            finally:
                task_event.set()
                await heartbeat_task

    def _prepare_execution_context(self, task: "TaskItem", workdir: str) -> tuple[tuple[str, ...], Path]:
        script = Path(workdir) / f"handler.{task.handler_format}"
        script.write_bytes(base64.b64decode(task.handler_code))

        input_file = Path(workdir) / "payload.json"
        input_file.write_text(json.dumps(task.payload, indent=2))

        output_file = Path(workdir) / "result.json"

        # python /path/to/handler.py --input /path/to/payload.json --output /path/to/result.json
        cmd_args = (
            str(script),
            "--input",
            str(input_file),
            "--output",
            str(output_file),
        )
        return cmd_args, output_file

    async def execute_in_subprocess(self, *args: str, cwd: str, log_queue: asyncio.Queue[str], timeout: int):
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            *args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            await asyncio.wait_for(
                asyncio.gather(
                    self.read_stream(process.stdout, log_queue),
                    self.read_stream(process.stderr, log_queue),
                ),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            logger.error(f"Subprocess timed out after {timeout} seconds, killing it.")
            process.kill()
            await process.wait()
            raise TimeoutError(f"Subprocess timed out after {timeout} seconds")

        rc = await process.wait()
        if rc != 0:
            raise subprocess.CalledProcessError(rc, "python")

    async def read_stream(self, stream: asyncio.StreamReader, log_queue: asyncio.Queue[str]):
        while True:
            line = await stream.readline()
            if not line:
                break
            await log_queue.put(line.decode().strip())

    async def send_heartbeat(self, task_instance_id: int, task_event: asyncio.Event, log_queue: asyncio.Queue):
        logger.info(f"Task {task_instance_id} heartbeat started.")
        while not task_event.is_set():
            logs: list[str] = []
            while not log_queue.empty():
                logs.append(await log_queue.get())

            payload = UpdateTaskInstanceStatus(
                status=TaskStatus.RUNNING,
                logs=logs,
            )
            await self.client.update_task_status(task_instance_id, payload)
            await asyncio.sleep(self.task_heartbeat_interval)

        logger.info(f"Task {task_instance_id} heartbeat stopped.")

    async def drain_queue(self, log_queue: asyncio.Queue[str]) -> list[str]:
        logs: list[str] = []
        while not log_queue.empty():
            logs.append(await log_queue.get())
        return logs
