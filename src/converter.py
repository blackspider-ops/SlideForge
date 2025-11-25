#!/usr/bin/env python3
"""
SlideForge - HTML Slides Converter CLI
Forge your HTML slides into PowerPoint or PDF format
"""

import sys
from cli import run_converter


def main():
    """Main entry point with error handling."""
    try:
        run_converter()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
