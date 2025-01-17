#!/bin/bash

# Create config directory
mkdir -p ~/.blnk/config

# Copy default config if it doesn't exist
if [ ! -f ~/.blnk/config/config.yaml ]; then
    cp ./config/config.yaml ~/.blnk/config/
fi

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .

echo "Installation complete! Run 'blnk' to start."