#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Updating blnk...${NC}"

# Navigate to the git repository directory
cd "$(dirname "$0")"

# Pull latest changes
echo -e "\n${GREEN}Pulling latest changes...${NC}"
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "\n${GREEN}Adding remote repository...${NC}"
    git remote add origin https://github.com/frgmt0/blnk.git
fi

if ! git pull origin main; then
    echo -e "${RED}Failed to pull latest changes${NC}"
    echo -e "Try: git branch --set-upstream-to=origin/main main"
    exit 1
fi

# Reinstall package and dependencies
echo -e "\n${GREEN}Reinstalling package...${NC}"
pip install --user --upgrade -r requirements.txt
pip install --user --upgrade .

echo -e "\n${GREEN}Update complete! Run 'blnk' to start chatting.${NC}"
