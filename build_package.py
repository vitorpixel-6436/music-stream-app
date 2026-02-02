#!/usr/bin/env python3
"""
Steam UI Framework - Package Build Script
==========================================

Automated script to build and package the Steam UI Framework.

Usage:
    python build_package.py

Requirements:
    pip install build wheel twine
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_step(message):
    print(f"{Colors.OKCYAN}{Colors.BOLD}[*] {message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}[✓] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}[✗] {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}[!] {message}{Colors.ENDC}")

def run_command(cmd, description):
    """Run shell command with error handling"""
    print_step(description)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        print_success(f"{description} - Done")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} - Failed")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("="*60)
    print("  Steam UI Framework - Package Builder")
    print("="*60)
    print(f"{Colors.ENDC}")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print_error("Python 3.8+ required")
        sys.exit(1)
    
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Read version from steam_ui/__init__.py
    init_file = project_root / 'steam_ui' / '__init__.py'
    if not init_file.exists():
        print_error("steam_ui/__init__.py not found")
        sys.exit(1)
    
    version = None
    with open(init_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                version = line.split('=')[1].strip().strip('"\'')
                break
    
    if not version:
        print_error("Could not read version from steam_ui/__init__.py")
        sys.exit(1)
    
    print_success(f"Building version: {version}")
    
    # Clean old builds
    print_step("Cleaning old builds...")
    dirs_to_clean = ['build', 'dist', 'steam_ui.egg-info', 'steam_ui_framework.egg-info']
    for dir_name in dirs_to_clean:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  Removed: {dir_name}")
    print_success("Cleanup complete")
    
    # Check if build tools are installed
    print_step("Checking build tools...")
    try:
        import build
        print_success("build module found")
    except ImportError:
        print_warning("build module not found, installing...")
        if not run_command(
            f"{sys.executable} -m pip install build wheel",
            "Installing build tools"
        ):
            sys.exit(1)
    
    # Build package
    if not run_command(
        f"{sys.executable} -m build",
        "Building package (wheel + sdist)"
    ):
        print_error("Build failed")
        sys.exit(1)
    
    # List built files
    dist_dir = project_root / 'dist'
    if dist_dir.exists():
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}Built packages:{Colors.ENDC}")
        for file in dist_dir.iterdir():
            size = file.stat().st_size / 1024  # KB
            print(f"  - {file.name} ({size:.1f} KB)")
    
    # Final instructions
    print(f"\n{Colors.HEADER}{Colors.BOLD}="*60)
    print("  Build Complete!")
    print("="*60 + Colors.ENDC)
    
    print(f"\n{Colors.OKCYAN}Installation commands:{Colors.ENDC}")
    print(f"  Local: pip install dist/steam_ui_framework-{version}-py3-none-any.whl")
    print(f"  Upload to PyPI: twine upload dist/*")
    
    print(f"\n{Colors.WARNING}Next steps:{Colors.ENDC}")
    print("  1. Test the wheel: pip install dist/*.whl")
    print("  2. Create GitHub Release")
    print("  3. Upload wheel to GitHub Release")
    print("  4. (Optional) Publish to PyPI")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Build cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
