# plugin_manager.py

import importlib
import pkgutil
import inspect
from .plugin import Plugin


class PluginManager:
    def __init__(self):
        self.plugins = {}
        self._load_plugins()

    def _load_plugins(self):
        # Dynamically import all modules in the 'plugins' package
        import plugins

        for _, plugin_name, _ in pkgutil.iter_modules(plugins.__path__):
            module = importlib.import_module(f"plugins.{plugin_name}")
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Plugin)
                    and obj is not Plugin
                ):
                    self.register_plugin(obj())

    def register_plugin(self, plugin):
        self.plugins[plugin.name] = plugin

    def has_plugin(self, name):
        return name in self.plugins

    def execute_plugin(self, magic_table, name, *args, **kwargs):
        if name in self.plugins:
            return self.plugins[name].execute(magic_table, *args, **kwargs)
        raise AttributeError(
            f"'{type(magic_table).__name__}' object has no attribute '{name}'"
        )
