# blnk

A powerful terminal-based chat application for seamless interaction with multiple AI providers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Multi-provider support (OpenAI, Anthropic, Google Gemini)
- Rich CLI interface with markdown formatting
- Dynamic model switching and API selection
- MCP integration for advanced reasoning
- Streaming responses with progress indicators
- Command system with help documentation
- YAML configuration with automatic JSON conversion
- Secure API key storage in user's home directory

## Installation

Requires Python 3.13 or higher.

1. Clone the repository:
```bash
git clone https://github.com/frgmt0/blnk.git
cd blnk
```

2. Run the installation script:
```bash
./install.sh
```

This will:
- Create necessary config directories
- Install dependencies
- Set up the default configuration
- Install blnk in development mode

## Quick Start

1. Run the setup command to configure your API providers:
```bash
blnk
/setup
```

2. Follow the prompts to configure your providers and API keys.

## Usage

Start blnk:
```bash
blnk
```

### Available Commands

- `/help` - Show help message
- `/apis` - List available AI providers
- `/use <api>` - Switch to specified AI provider
- `/model-list` - Show available models for current/all providers
- `/switch-model` - Switch to a different model for current provider
- `/tools` - List available MCP tools
- `/exit` - Exit the application

### Examples

```bash
/use anthropic                               # Switch to Anthropic provider
/switch-model claude-3-5-sonnet-20241022    # Switch to Claude 3 model
/tools                                      # Show available tools
```

## Configuration

blnk stores its configuration in `~/.blnk/config/`:

- `config.yaml` - Main configuration file (edit this for changes)
- `config.json` - Runtime configuration (automatically generated)
- `mcp/*.json` - MCP server configurations

### MCP Integration

blnk supports integration with MCP (Machine Cognition Protocol) servers. While native MCP-reasoner support is planned for future releases, you can already configure and use MCP servers:

1. Create a JSON config file in `~/.blnk/config/mcp/` (e.g., `default.json`)
2. Configure the server details:
```json
{
    "server": {
        "command": "node",
        "args": ["path/to/mcp-reasoner/dist/index.js"],
        "env": {}
    }
}
```

Multiple MCP servers can be configured by creating additional JSON files in the `mcp/` directory.

The configuration includes:
- Default API provider
- Model preferences
- API keys (securely stored)
- Token limits
- MCP settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [MCP-Reasoner](https://github.com/Jacck/mcp-reasoner) for advanced reasoning capabilities
- Thanks to all [contributors](CONTRIBUTORS.md)

## Author

[frgmt0](https://github.com/frgmt0) - frgmt_@frgmt.xyz
