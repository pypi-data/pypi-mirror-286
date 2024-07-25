import importlib
import sys
from types import ModuleType

# The name of your new package
NEW_PACKAGE = "nshtrainer"

# Import the new package
new_package = importlib.import_module(NEW_PACKAGE)


# Create a custom module class that inherits from ModuleType
class ProxyModule(ModuleType):
    def __getattr__(self, name):
        return getattr(new_package, name)

    def __dir__(self):
        return dir(new_package)


# Create a new module instance
old_module = ProxyModule(__name__)

# Copy attributes from new_package to old_module
for attr in dir(new_package):
    if not attr.startswith("__"):
        setattr(old_module, attr, getattr(new_package, attr))

# Replace the module in sys.modules
sys.modules[__name__] = old_module


# Handle submodule imports
class SubmoduleProxy:
    def __getattr__(self, name):
        return importlib.import_module(f"{NEW_PACKAGE}.{name}")


# Add submodule handling to the proxy module
old_module.__class__ = type(
    "ProxyModuleWithSubmodules", (ProxyModule, SubmoduleProxy), {}
)
