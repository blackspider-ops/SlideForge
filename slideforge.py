#!/usr/bin/env python3
"""
SlideForge - Universal launcher script
Works on macOS, Linux, and Windows
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_banner():
    """Print SlideForge banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ███████╗██╗     ██╗██████╗ ███████╗███████╗ ██████╗    ║
    ║   ██╔════╝██║     ██║██╔══██╗██╔════╝██╔════╝██╔═══██╗   ║
    ║   ███████╗██║     ██║██║  ██║█████╗  █████╗  ██║   ██║   ║
    ║   ╚════██║██║     ██║██║  ██║██╔══╝  ██╔══╝  ██║   ██║   ║
    ║   ███████║███████╗██║██████╔╝███████╗██║     ╚██████╔╝   ║
    ║   ╚══════╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝      ╚═════╝    ║
    ║                                                           ║
    ║        Forge HTML slides into PowerPoint or PDF          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_python_command():
    """Get the correct Python command for the platform."""
    # Try python3 first, then python
    for cmd in ['python3', 'python']:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def check_python_version():
    """Check if Python version is 3.7 or higher."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def check_venv():
    """Check if virtual environment exists, create if not."""
    venv_path = Path('src/venv')
    
    if venv_path.exists():
        print("✓ Virtual environment found")
        return True
    
    print("⚙ Creating virtual environment...")
    try:
        subprocess.run(
            [sys.executable, '-m', 'venv', str(venv_path)],
            check=True
        )
        print("✓ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def get_venv_python():
    """Get the path to Python in the virtual environment."""
    system = platform.system()
    venv_path = Path('src/venv')
    
    if system == 'Windows':
        return venv_path / 'Scripts' / 'python.exe'
    else:
        return venv_path / 'bin' / 'python'


def get_activation_command():
    """Get the virtual environment activation command."""
    system = platform.system()
    
    if system == 'Windows':
        return 'src\\venv\\Scripts\\activate'
    else:
        return 'source src/venv/bin/activate'


def run_converter(args):
    """Run the converter with provided arguments."""
    venv_python = get_venv_python()
    
    if not venv_python.exists():
        print("❌ Virtual environment Python not found")
        sys.exit(1)
    
    # Build command
    cmd = [str(venv_python), 'src/converter.py'] + args
    
    print(f"\n{'='*60}")
    print("Running SlideForge...")
    print(f"{'='*60}\n")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Conversion failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        sys.exit(0)


def show_usage():
    """Show usage information."""
    print("\n📖 Usage:")
    print("  python slideforge.py --format pdf")
    print("  python slideforge.py --format ppt")
    print("  python slideforge.py --format pdf --method weasyprint")
    print("  python slideforge.py --format ppt -o presentation")
    print("\n📚 For more options:")
    print("  python slideforge.py --help")
    print()


def main():
    """Main entry point."""
    print_banner()
    
    # Check Python version
    print("\n🔍 Checking system requirements...")
    check_python_version()
    
    # Check/create virtual environment
    if not check_venv():
        sys.exit(1)
    
    # Show platform info
    print(f"✓ Platform: {platform.system()} {platform.release()}")
    
    # Parse arguments
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        show_usage()
        if '--help' in sys.argv or '-h' in sys.argv:
            run_converter(['--help'])
        else:
            print("💡 Tip: Run with --help to see all available options")
        sys.exit(0)
    
    # Get arguments (skip script name)
    args = sys.argv[1:]
    
    # Run converter
    run_converter(args)
    
    print(f"\n{'='*60}")
    print("✨ Done! Thank you for using SlideForge")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
