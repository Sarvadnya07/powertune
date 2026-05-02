import os
import importlib.util

class PluginManager:
    """
    Phase 10: Ecosystem & Scale - Plugin Architecture.
    Discovers and loads vendor-specific modules and custom analyzers.
    """
    def __init__(self, root_dir="."):
        self.root_dir = root_dir
        self.plugins_dir = os.path.join(root_dir, "plugins")
        os.makedirs(self.plugins_dir, exist_ok=True)
        self.plugins = []

    def discover_plugins(self):
        """Recursively finds all plugin modules in the plugins/ directory."""
        self.plugins = []
        for root, dirs, files in os.walk(self.plugins_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    self.plugins.append(os.path.join(root, file))
        return self.plugins

    def run_plugins(self):
        """Executes all discovered plugins and returns their telemetry."""
        master_telemetry = []
        for plugin_path in self.discover_plugins():
            try:
                module_name = os.path.splitext(os.path.basename(plugin_path))[0]
                spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'get_telemetry'):
                    master_telemetry.extend(module.get_telemetry())
            except Exception as e:
                print(f"     [!] Failed to load plugin {plugin_path}: {e}")
        return master_telemetry

if __name__ == "__main__":
    pm = PluginManager()
    print(f"Found {len(pm.discover_plugins())} plugins.")
