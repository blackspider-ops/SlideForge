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


def check_venv_module():
    """Check if venv module is available, install if not."""
    try:
        import venv
        print("✓ venv module available")
        return True
    except ImportError:
        print("⚠ venv module not found, attempting to install...")
        
        # Try to install venv
        system = platform.system()
        try:
            if system == 'Linux':
                print("  Installing python3-venv...")
                subprocess.run(
                    ['sudo', 'apt-get', 'install', '-y', 'python3-venv'],
                    check=True
                )
            elif system == 'Darwin':  # macOS
                print("  venv should be included with Python on macOS")
                print("  If this fails, reinstall Python from python.org")
                return False
            elif system == 'Windows':
                print("  venv should be included with Python on Windows")
                print("  If this fails, reinstall Python from python.org")
                return False
            
            # Try importing again
            import venv
            print("✓ venv module installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install venv module: {e}")
            print("\n💡 Manual installation:")
            if system == 'Linux':
                print("   sudo apt-get install python3-venv")
            else:
                print("   Reinstall Python from https://www.python.org/downloads/")
            return False


def check_venv():
    """Check if virtual environment exists, create if not."""
    venv_path = Path('src/venv')
    
    if venv_path.exists():
        print("✓ Virtual environment found")
        return True
    
    # Check if venv module is available
    if not check_venv_module():
        return False
    
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
        print("\n💡 Try running manually:")
        print(f"   {sys.executable} -m venv src/venv")
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


def clean_slides_directory(slides_dir: str):
    """Delete all HTML files in slides directory with double confirmation."""
    from pathlib import Path
    import glob
    
    slides_path = Path(slides_dir)
    
    if not slides_path.exists():
        print(f"Slides directory not found: {slides_path}")
        return
    
    # Get HTML files
    pattern = str(slides_path / "*.html")
    html_files = sorted(glob.glob(pattern))
    
    if not html_files:
        print(f"No HTML files found in {slides_path}")
        return
    
    print(f"\n{'='*60}")
    print("⚠️  WARNING: DELETE ALL SLIDES")
    print(f"{'='*60}")
    print(f"\nThis will permanently delete {len(html_files)} HTML file(s) from:")
    print(f"  {slides_path}")
    print("\nFiles to be deleted:")
    for i, file in enumerate(html_files[:10], 1):  # Show first 10
        print(f"  {i}. {Path(file).name}")
    if len(html_files) > 10:
        print(f"  ... and {len(html_files) - 10} more files")
    
    print(f"\n{'='*60}")
    response1 = input("Are you sure you want to delete ALL slides? (yes/no): ").strip().lower()
    
    if response1 != 'yes':
        print("Operation cancelled.")
        return
    
    print(f"\n{'='*60}")
    print("⚠️  FINAL CONFIRMATION")
    print(f"{'='*60}")
    response2 = input(f"Type 'DELETE' to confirm deletion of {len(html_files)} files: ").strip()
    
    if response2 != 'DELETE':
        print("Operation cancelled.")
        return
    
    # Delete files
    print(f"\n🗑️  Deleting {len(html_files)} HTML files...")
    deleted_count = 0
    failed_count = 0
    
    for html_file in html_files:
        try:
            Path(html_file).unlink()
            deleted_count += 1
        except Exception as e:
            print(f"  Failed to delete {Path(html_file).name}: {e}")
            failed_count += 1
    
    print(f"\n✓ Deleted {deleted_count} file(s)")
    if failed_count > 0:
        print(f"⚠ Failed to delete {failed_count} file(s)")
    
    print(f"\n{'='*60}")
    print("Slides directory cleaned successfully!")
    print(f"{'='*60}\n")


def run_converter(args):
    """Run the converter with provided arguments."""
    from version import __version__, __author__, __description__
    from config import show_config, set_config_value
    
    # Check if --version flag is present
    if '--version' in args:
        print(f"\nSlideForge v{__version__}")
        print(f"{__description__}")
        print(f"Author: {__author__}")
        print(f"GitHub: https://github.com/blackspider-ops/SlideForge\n")
        return
    
    # Check if --show-config flag is present
    if '--show-config' in args:
        show_config()
        return
    
    # Check if --set-config flag is present
    if '--set-config' in args:
        idx = args.index('--set-config')
        if idx + 2 < len(args):
            key = args[idx + 1]
            value = args[idx + 2]
            if set_config_value(key, value):
                return
        else:
            print("Error: --set-config requires KEY and VALUE")
        return
    
    # Check if --list flag is present
    if '--list' in args:
        # Get slides directory from args or use default
        slides_dir = '../slides'
        if '--slides-dir' in args:
            idx = args.index('--slides-dir')
            if idx + 1 < len(args):
                slides_dir = args[idx + 1]
        
        # Resolve path relative to main.py location
        script_dir = Path(__file__).parent
        slides_path = (script_dir / slides_dir).resolve()
        
        # List slides
        import glob
        if not slides_path.exists():
            print(f"Slides directory not found: {slides_path}")
            return
        
        pattern = str(slides_path / "*.html")
        html_files = sorted(glob.glob(pattern))
        
        if not html_files:
            print(f"No HTML files found in {slides_path}")
            return
        
        print(f"\n{'='*60}")
        print(f"Found {len(html_files)} HTML slide(s) in {slides_path}")
        print(f"{'='*60}\n")
        
        for i, file in enumerate(html_files, 1):
            file_path = Path(file)
            size = file_path.stat().st_size / 1024  # KB
            print(f"  {i:2d}. {file_path.name:<30} ({size:.1f} KB)")
        
        print(f"\n{'='*60}\n")
        return
    
    # Check if --clean flag is present
    if '--clean' in args:
        # Get slides directory from args or use default
        slides_dir = '../slides'
        if '--slides-dir' in args:
            idx = args.index('--slides-dir')
            if idx + 1 < len(args):
                slides_dir = args[idx + 1]
        
        # Resolve path relative to main.py location
        script_dir = Path(__file__).parent
        slides_path = (script_dir / slides_dir).resolve()
        
        clean_slides_directory(str(slides_path))
        return
    
    venv_python = get_venv_python()
    
    if not venv_python.exists():
        print("❌ Virtual environment Python not found")
        sys.exit(1)
    
    # Build command - converter.py is in same directory as main.py
    converter_path = Path(__file__).parent / 'converter.py'
    cmd = [str(venv_python), str(converter_path)] + args
    
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
    system = platform.system()
    
    if system == 'Windows':
        cmd = 'slideforge.bat'
    else:
        cmd = './slideforge.sh'
    
    print("\n📖 Usage:")
    print(f"  {cmd} --format pdf")
    print(f"  {cmd} --format ppt")
    print(f"  {cmd} --format pdf --method weasyprint")
    print(f"  {cmd} --format ppt -o presentation")
    print("\n📚 For more options:")
    print(f"  {cmd} --help")
    print()


def install_dependencies():
    """Install dependencies in virtual environment."""
    venv_python = get_venv_python()
    
    # CRITICAL: Verify venv Python exists before installing anything
    if not venv_python.exists():
        print("❌ Virtual environment Python not found, cannot install dependencies")
        return False
    
    # Check for requirements.txt in root or src
    requirements_file = Path('requirements.txt')
    if not requirements_file.exists():
        requirements_file = Path('src/requirements.txt')
    
    if not requirements_file.exists():
        print("⚠ requirements.txt not found, skipping dependency installation")
        return True
    
    print("\n📦 Checking dependencies...")
    
    # Check if dependencies are already installed
    try:
        result = subprocess.run(
            [str(venv_python), '-m', 'pip', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check for key packages
        installed = result.stdout.lower()
        if 'playwright' in installed or 'weasyprint' in installed:
            print("✓ Dependencies already installed")
            return True
    except Exception:
        pass
    
    # Install dependencies
    print("⚙ Installing dependencies (this may take a minute)...")
    try:
        # Upgrade pip first
        print("  Upgrading pip...")
        subprocess.run(
            [str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'],
            capture_output=True,
            check=True
        )
        
        # Install requirements
        print("  Installing packages...")
        subprocess.run(
            [str(venv_python), '-m', 'pip', 'install', '-r', str(requirements_file)],
            check=True
        )
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("\n💡 Try installing manually:")
        print(f"   {venv_python} -m pip install -r {requirements_file}")
        return False


def main():
    """Main entry point."""
    print_banner()
    
    # Check Python version
    print("\n🔍 Checking system requirements...")
    check_python_version()
    
    # Check/create virtual environment
    if not check_venv():
        print("\n❌ Cannot proceed without virtual environment")
        sys.exit(1)
    
    # Install dependencies if needed
    if not install_dependencies():
        print("\n⚠ Warning: Dependencies may not be fully installed")
        print("   The converter will attempt to install them when needed")
    
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
