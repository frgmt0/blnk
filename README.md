# blnk

A powerful terminal-based chat application for seamless interaction with multiple AI providers.

[![PyPI version](https://badge.fury.io/py/blnk.svg)](https://badge.fury.io/py/blnk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Multi-provider support (OpenAI, Anthropic, Google Gemini)
- Rich CLI interface with markdown formatting
- Dynamic model switching and API selection
- MCP integration for advanced reasoning
- Streaming responses with progress indicators
- Command system with help documentation
- Configurable setup with environment management

## Installation

```bash
pip install blnk-chat
```

Requires Python 3.13 or higher.

## Quick Start

1. Install blnk:
```bash
pip install blnk-chat
```

2. Run the setup command:
```bash
blnk
/setup
```

3. Configure your API providers and settings following the prompts.

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
/switch-model claude-3-5-sonnet-20241022     # Switch to Claude 3 model
/tools                                       # Show available tools
```

## Configuration

blnk-chat uses environment variables for API keys. Create a `.env` file in your project directory:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

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
