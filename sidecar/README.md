# Tailor Sidecar

The Python backend for the Tailor Desktop Application. It operates as a sidecar process, handling vault-specific logic, AI orchestration (LangGraph), and plugin management.

## Architecture

The Sidecar communicates with the main Tauri process via **WebSockets** (JSON-RPC 2.0).

- **`main.py`**: Entry point. Starts `WebSocketServer` and `VaultBrain`.
- **`websocket_server.py`**: Handles bi-directional communication with Tauri.
- **`vault_brain.py`**: Core orchestrator. Loads plugins, manages lifecycle, and executes commands.
- **`api/plugin_base.py`**: Base class for all plugins.
- **`event_emitter.py`**: Utility for plugins to send events to the UI.

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Development

### Setup
```bash
cd sidecar
pip install -r requirements.txt
pip install -r test-requirements.txt
```

### Running Tests
We use `pytest` for unit and integration testing.
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=.
```

### Type Checking
We use `mypy` for strict type enforcement.
```bash
mypy --explicit-package-bases .
```

### Project Structure
```text
sidecar/
├── api/             # Public APIs for plugins
├── utils/           # Shared utilities (logging, paths, json-rpc)
├── tests/           # Unit and Integration tests
├── main.py          # Entry point
├── vault_brain.py   # Core logic
└── ...
```

## Plugin Development

Plugins reside in the Vault's `plugins/` directory. Each plugin must have a `main.py` defining a `Plugin` class that inherits from `api.plugin_base.PluginBase`.

Example:
```python
from api.plugin_base import PluginBase

class Plugin(PluginBase):
    def register_commands(self):
        self.brain.register_command("my.command", self.handle_command, self.name)

    async def handle_command(self, **kwargs):
        self.emitter.notify("Command executed!")
        return {"status": "ok"}
```
