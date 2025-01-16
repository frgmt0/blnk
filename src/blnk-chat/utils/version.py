import argparse
import json
import os
import subprocess
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
    contributors_path = Path(__file__).parent.parent.parent.parent / "CONTRIBUTORS.md"
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

def update_changelog(version_str, changelog_path, contributors):
    """Update CHANGELOG.md with new version and release notes"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Read existing changelog
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r') as f:
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
    with open(changelog_path, 'w') as f:
        f.write(new_content)

def git_commit_and_tag(version_str):
    """Commit version changes and create a new tag"""
    try:
        # Stage changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_msg = f'release: version {version_str}'
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Create and push tag
        tag = f'v{version_str}'
        subprocess.run(['git', 'tag', '-a', tag, '-m', f'Release {tag}'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        subprocess.run(['git', 'push', 'origin', tag], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in git operations: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Release automation script')
    parser.add_argument('version', help='New version number (e.g., 0.1.0)')
    parser.add_argument('--no-git', action='store_true', help='Skip git operations')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    version_str = args.version
    
    # Get project root directory
    root_dir = Path(__file__).parent.parent.parent.parent
    
    if args.dry_run:
        print(f"Would update version to {version_str} in:")
        print(f"- {root_dir}/pyproject.toml")
        print(f"- {root_dir}/src/blnk-chat/__init__.py")
        print(f"Would update CHANGELOG.md")
        if not args.no_git:
            print("Would create git commit and tag")
        return
    
    # Update version in pyproject.toml
    update_version(version_str, root_dir / "pyproject.toml")
    print(f"✓ Updated version in pyproject.toml")
    
    # Update version in __init__.py
    update_init_version(version_str, root_dir / "src" / "blnk-chat" / "__init__.py")
    print(f"✓ Updated version in __init__.py")
    
    # Get contributors
    contributors = get_contributors()
    
    # Update changelog
    update_changelog(version_str, root_dir / "CHANGELOG.md", contributors)
    print(f"✓ Updated CHANGELOG.md")
    
    if not args.no_git:
        if git_commit_and_tag(version_str):
            print(f"✓ Created git commit and tag v{version_str}")
            print("\nRelease process completed successfully!")
            print(f"GitHub Actions will now build and publish version {version_str}")
        else:
            print("\n✗ Failed to complete git operations")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
