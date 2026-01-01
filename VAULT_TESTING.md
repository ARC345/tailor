# Vault Testing UI

A lightweight browser-based testing interface for vault operations.

## Quick Start

1. **Open a vault** using the main Tailor app (`index.html`)
   - Click "Open Vault" 
   - Select your vault directory (e.g., `example-vault`)
   - Note the WebSocket port in the status message (e.g., `Port: 9001`)

2. **Open the testing UI**
   - Open `vault-test.html` in your browser
   - Enter the WebSocket port number shown in the Tailor app
   - Click "Connect"

3. **Start testing!**
   - The connection status indicator will turn green when connected
   - Try sending a chat message
   - Execute plugin commands
   - Monitor events in the log

## Available Features

### 🔌 Connection Panel
- Connect to vault WebSocket server
- Disconnect when done
- Real-time connection status indicator

### 💬 Chat Test
- Send messages to the vault
- Test chat.send_message command
- View responses in event log

### ⚡ Execute Command
- Run any registered plugin command
- Pass arguments as JSON
- Test custom plugin functionality

### 🚀 Quick Commands
- **List Available Commands**: Get all registered commands from plugins
- **Get Vault Info**: View vault configuration and loaded plugins

### 📊 Event Log
- Real-time monitoring of all WebSocket messages
- Color-coded log entries (info, success, error, event)
- Timestamps for each entry
- Clear log button

## Example Commands

### Basic Chat
```javascript
// In Chat Test panel:
Message: "Hello vault!"
```

### Execute Plugin Command
```javascript
// In Execute Command panel:
Command ID: demo_plugin.greet
Arguments: {"name": "World"}
```

### List All Commands
```javascript
// Click "List Available Commands" button
// Returns all registered plugin commands
```

### Get Vault Information
```javascript
// Click "Get Vault Info" button
// Returns vault path, name, version, loaded plugins
```

## WebSocket Protocol

The testing UI uses JSON-RPC 2.0 protocol:

### Request Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "command_name",
  "params": {
    "key": "value"
  }
}
```

### Response Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "status": "success",
    "data": {}
  }
}
```

### Event Format (from server)
```json
{
  "jsonrpc": "2.0",
  "method": "event",
  "params": {
    "event_type": "NOTIFY",
    "data": {
      "message": "Something happened"
    }
  }
}
```

## Built-in Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| `chat.send_message` | Send a chat message | `message: string` |
| `execute_command` | Execute a registered command | `command: string, args: object` |
| `list_commands` | List all available commands | None |
| `get_vault_info` | Get vault configuration | None |

## Testing Plugin Commands

To test custom plugin commands:

1. Make sure your plugin is loaded in the vault's `plugins/` directory
2. Your plugin should register commands via `brain.register_command()`
3. In the testing UI, use the "Execute Command" panel
4. Enter the command ID (e.g., `my_plugin.do_something`)
5. Add any required arguments as JSON

## Troubleshooting

### Connection Failed
- Ensure the vault is opened in the main Tailor app first
- Check that the WebSocket port matches the one shown in Tailor
- Verify the sidecar process is running

### Command Not Found
- Use "List Available Commands" to see all registered commands
- Check that the plugin loaded successfully (check console logs)
- Verify the command ID spelling

### No Response
- Check the event log for error messages
- Verify the command parameters are correct JSON
- Look for error messages in the Tauri app console

## Tips

- Keep the event log open to monitor all WebSocket communication
- Use the timestamp to correlate requests and responses
- Clear the log periodically for easier debugging
- Test commands incrementally (start with simple commands)
- Use "Get Vault Info" to verify plugins are loaded correctly
