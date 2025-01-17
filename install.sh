#!/bin/bash

# Create config directory
mkdir -p ~/.blnk/config

# Install dependencies and package globally
pip install --user -r requirements.txt
pip install --user .

# Create configs directory if it doesn't exist
mkdir -p ~/.blnk/config/mcp

# Copy default MCP config if it doesn't exist
if [ ! -f ~/.blnk/config/mcp/default.json ]; then
    cat > ~/.blnk/config/mcp/default.json << EOL
{
    "server": {
        "command": "node",
        "args": ["$(npm root -g)/mcp-reasoner/dist/index.js"],
        "env": {
            "NODE_ENV": "production",
            "MCP_LOG_LEVEL": "info"
        }
    },
    "tools": {
        "enabled": ["*"],
        "disabled": []
    }
}
EOL
fi

# Create default config if it doesn't exist
if [ ! -f ~/.blnk/config/config.yaml ]; then
    cat > ~/.blnk/config/config.yaml << EOL
default_api: anthropic
default_models:
  openai: gpt-4o
  anthropic: claude-3-5-sonnet-20241022
  gemini: gemini-2.0-flash-exp
max_tokens:
  openai: 2000
  anthropic: 1000
  gemini: 1000
api_keys: {}
EOL
fi

echo "Installation complete! Run 'blnk' from anywhere to start."
