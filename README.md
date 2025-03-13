# MCP Command History

A powerful tool for exploring, searching, and managing your shell command history through the MCP (Model Control Protocol) interface. This project allows you to easily access, search, and retrieve your previously executed shell commands.

## Features

- **Command History Access**: Access your shell command history programmatically
- **Powerful Search**: Search through your command history with text queries
- **Recent Commands**: Quickly retrieve your most recently executed commands
- **MCP Integration**: Seamlessly integrates with Cursor and other MCP-compatible tools

## Installation

### Prerequisites

- Python 3.6 or higher
- A shell with history support (Bash, Zsh, etc.)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-cmd-history.git
cd mcp-cmd-history

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python mcp_history_server.py
```

By default, the server will read your shell history from the location specified in the `HISTFILE` environment variable, or fall back to `~/.bash_history`.

### Using with Cursor

Once the server is running, you can use the following MCP tools in Cursor:

1. **Get Recent Commands**:
   ```
   Please show me my most recent shell commands.
   ```

2. **Search Command History**:
   ```
   Please search my command history for 'git commit' and show me the results.
   ```

3. **Get Specific Command**:
   You can retrieve a specific command by its ID after searching or listing recent commands.

## API Reference

### MCP Tools

- `search_commands(query: str)`: Search for commands in shell history
- `get_recent_commands(limit: int = 10)`: Get the most recent commands from history
- `get_command(command_id: int)`: Get a specific command by ID

### MCP Resources

- `history://recent/{limit}`: Get recent commands (HTTP endpoint)
- `history://search/{query}`: Search for commands (HTTP endpoint)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 