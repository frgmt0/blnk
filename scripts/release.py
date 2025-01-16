#!/usr/bin/env python3
"""
Release script for blnk-chat.
Automates version bumping, changelog updates, and git tagging.

Usage:
    python scripts/release.py [major|minor|patch]
"""

import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def get_current_version():
    """Get current version from pyproject.toml"""
    with open("pyproject.toml") as f:
        content = f.read()
    match = re.search(r'version = "([^"]+)"', content)
    return match.group(1) if match else None

def bump_version(current, bump_type):
    """Bump version according to semver"""
    major, minor, patch = map(int, current.split('.'))
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"

def update_version_files(new_version):
    """Update version in all required files"""
    # Update pyproject.toml
    with open("pyproject.toml", 'r') as f:
        content = f.read()
    content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    with open("pyproject.toml", 'w') as f:
        f.write(content)

    # Update __init__.py
    init_path = Path("src/blnk-chat/__init__.py")
    with open(init_path, 'r') as f:
        content = f.read()
    content = re.sub(
        r'__version__ = "[^"]+"',
        f'__version__ = "{new_version}"',
        content
    )
    with open(init_path, 'w') as f:
        f.write(content)

def update_changelog(version):
    """Update CHANGELOG.md with new version"""
    today = datetime.now().strftime("%Y-%m-%d")
    new_version_entry = f"""
## [{version}] - {today}

### Added
- <add new features>

### Changed
- <add changes>

### Fixed
- <add bug fixes>
"""
    
    with open("CHANGELOG.md", 'r') as f:
        content = f.read()
    
    # Insert new version after header
    content = re.sub(
        r"(# Changelog\n\n)",
        f"\\1{new_version_entry}\n",
        content
    )
    
    with open("CHANGELOG.md", 'w') as f:
        f.write(content)

def git_commands(version):
    """Run git commands for release"""
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", f"release: version {version}"],
        ["git", "tag", "-a", f"v{version}", "-m", f"Release v{version}"],
        ["git", "push", "origin", "main", "--tags"]
    ]
    
    for cmd in commands:
        subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['major', 'minor', 'patch']:
        print("Usage: python scripts/release.py [major|minor|patch]")
        sys.exit(1)

    bump_type = sys.argv[1]
    current_version = get_current_version()
    if not current_version:
        print("Could not determine current version")
        sys.exit(1)

    new_version = bump_version(current_version, bump_type)
    print(f"Bumping version: {current_version} -> {new_version}")

    try:
        update_version_files(new_version)
        update_changelog(new_version)
        git_commands(new_version)
        print(f"Successfully released version {new_version}")
    except Exception as e:
        print(f"Error during release process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
