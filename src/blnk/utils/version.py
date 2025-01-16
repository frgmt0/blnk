import argparse
import json
import os
from datetime import datetime
from pathlib import Path

def update_version(version_str, pyproject_path):
    """Update version in pyproject.toml"""
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    # Update version in pyproject.toml
    new_content = content.replace(
        f'version = "{".".join(content.split("version = ")[1].split('"')[1].split("."))}"',
        f'version = "{version_str}"'
    )
    
    with open(pyproject_path, 'w') as f:
        f.write(new_content)

def update_init_version(version_str, init_path):
    """Update version in __init__.py"""
    with open(init_path, 'r') as f:
        content = f.read()
    
    new_content = content.replace(
        f'__version__ = "{".".join(content.split("__version__ = ")[1].split('"')[1].split("."))}"',
        f'__version__ = "{version_str}"'
    )
    
    with open(init_path, 'w') as f:
        f.write(new_content)

def get_contributors():
    """Get list of contributors from CONTRIBUTORS.md"""
    contributors_path = Path(__file__).parent.parent / "CONTRIBUTORS.md"
    if not contributors_path.exists():
        return []
        
    with open(contributors_path) as f:
        lines = f.readlines()
        
    contributors = []
    for line in lines:
        if line.startswith("- "):
            # Extract name and GitHub URL
            parts = line.strip("- ").split("[")
            if len(parts) > 1:
                name = parts[1].split("]")[0]
                url = parts[1].split("(")[1].split(")")[0]
                contributors.append({"name": name, "url": url})
    
    return contributors

def update_changelog(version_str, release_notes_path, contributors):
    """Update CHANGELOG.md with new version and release notes"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Read existing changelog
    if os.path.exists(release_notes_path):
        with open(release_notes_path, 'r') as f:
            existing_content = f.read()
    else:
        existing_content = "# Changelog\n\n"
    
    # Format contributors section
    contributors_section = "\n### Contributors\n\n"
    for contributor in contributors:
        contributors_section += f"- [{contributor['name']}]({contributor['url']})\n"
    
    # Add new version section
    new_version_content = f"""
## [{version_str}] - {today}

{contributors_section}
"""
    
    # Combine content
    new_content = existing_content.split("## [")[0] + new_version_content + \
                 "## [".join(existing_content.split("## [")[1:])
    
    # Write updated changelog
    with open(release_notes_path, 'w') as f:
        f.write(new_content)

def main():
    parser = argparse.ArgumentParser(description='Update version and generate release notes')
    parser.add_argument('-major', help='Major version number')
    parser.add_argument('-minor', help='Minor version number')
    parser.add_argument('-patch', help='Patch version number')
    parser.add_argument('-release-notes', help='Path to CHANGELOG.md', default='CHANGELOG.md')
    
    args = parser.parse_args()
    
    # Construct version string
    if args.major and args.minor and args.patch:
        version_str = f"{args.major}.{args.minor}.{args.patch}"
    elif args.major:
        version_str = args.major
    else:
        raise ValueError("Please provide version number(s)")
    
    # Get project root directory
    root_dir = Path(__file__).parent.parent
    
    # Update version in pyproject.toml
    update_version(version_str, root_dir / "pyproject.toml")
    
    # Update version in __init__.py
    update_init_version(version_str, root_dir / "__init__.py")
    
    # Get contributors
    contributors = get_contributors()
    
    # Update changelog
    update_changelog(version_str, args.release_notes, contributors)
    
    print(f"Version updated to {version_str}")
    print(f"Changelog updated at {args.release_notes}")

if __name__ == "__main__":
    main()
