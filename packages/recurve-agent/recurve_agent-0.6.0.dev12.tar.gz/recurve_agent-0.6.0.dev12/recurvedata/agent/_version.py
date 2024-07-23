import importlib.metadata

try:
    VERSION = importlib.metadata.version("recurve-agent")
except importlib.metadata.PackageNotFoundError:
    # this should not happen in a normal environment, but it's useful for testing
    VERSION = "0.0.0"
