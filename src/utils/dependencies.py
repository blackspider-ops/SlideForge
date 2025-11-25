"""Dependency management utilities."""

import sys
import subprocess


def install_package(package_name: str) -> bool:
    """Install a Python package using pip."""
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}")
        return False


def install_playwright_browsers() -> bool:
    """Install Playwright browsers."""
    try:
        print("Installing Playwright Chromium browser...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        return True
    except subprocess.CalledProcessError:
        print("Failed to install Playwright browsers")
        return False


def check_and_install_dependencies(method: str, format: str) -> bool:
    """Check if required dependencies are installed, and install if missing."""
    missing_packages = []
    needs_playwright_install = False
    
    # Check common dependencies
    try:
        import pptx
    except ImportError:
        missing_packages.append("python-pptx")
    
    try:
        import PIL
    except ImportError:
        missing_packages.append("pillow")
    
    try:
        import PyPDF2
    except ImportError:
        missing_packages.append("PyPDF2")
    
    try:
        import reportlab
    except ImportError:
        missing_packages.append("reportlab")
    
    # Check method-specific dependencies
    if method == "playwright":
        try:
            import playwright
        except ImportError:
            missing_packages.append("playwright")
        else:
            # Check if browsers are installed
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    try:
                        p.chromium.launch()
                    except Exception:
                        needs_playwright_install = True
            except Exception:
                needs_playwright_install = True
    
    elif method == "weasyprint":
        try:
            import weasyprint
        except ImportError:
            missing_packages.append("weasyprint")
        
        if format == "ppt":
            try:
                import pdf2image
            except ImportError:
                missing_packages.append("pdf2image")
    
    # If nothing is missing, return True
    if not missing_packages and not needs_playwright_install:
        return True
    
    # Ask user to install
    print("\n" + "="*60)
    print("Missing dependencies detected!")
    print("="*60)
    
    if missing_packages:
        print("\nMissing Python packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
    
    if needs_playwright_install:
        print("\nPlaywright browsers need to be installed")
    
    if method == "weasyprint" and format == "ppt":
        print("\nNote: WeasyPrint PPT conversion also requires poppler")
        print("Install with: brew install poppler (macOS)")
    
    print("\n" + "="*60)
    response = input("Would you like to install missing dependencies now? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Installation cancelled. Please install dependencies manually.")
        return False
    
    # Install missing packages
    print("\nInstalling dependencies...")
    for package in missing_packages:
        if not install_package(package):
            print(f"\nFailed to install {package}. Please install manually:")
            print(f"  pip install {package}")
            return False
    
    # Install Playwright browsers if needed
    if needs_playwright_install:
        if not install_playwright_browsers():
            print("\nFailed to install Playwright browsers. Please run manually:")
            print("  playwright install chromium")
            return False
    
    print("\n" + "="*60)
    print("✓ All dependencies installed successfully!")
    print("="*60 + "\n")
    
    return True
