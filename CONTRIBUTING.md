# Contributing to SlideForge

Thank you for considering contributing to SlideForge! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/blackspider-ops/SlideForge/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Error messages or logs

### Suggesting Features

1. Check [Issues](https://github.com/blackspider-ops/SlideForge/issues) for existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Keep functions focused and under 150 lines
   - Add docstrings to new functions
   - Handle errors gracefully

4. **Test your changes**
   ```bash
   # Test basic functionality
   python src/converter.py --format pdf
   python src/converter.py --format ppt
   
   # Test both methods
   python src/converter.py --format pdf --method playwright
   python src/converter.py --format pdf --method weasyprint
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
   
   Use conventional commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements
   - `Docs:` for documentation
   - `Refactor:` for code restructuring

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Explain what you changed and why

## Development Setup

```bash
# Clone your fork
git clone https://github.com/blackspider-ops/SlideForge.git
cd SlideForge

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd src
pip install -r requirements.txt
playwright install chromium
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions focused (single responsibility)
- Add docstrings to all functions
- Handle errors with try-except blocks
- Clean up resources in finally blocks

### Example Function

```python
def convert_to_format(html_files: List[Path], output_path: str) -> None:
    """Convert HTML files to specified format.
    
    Args:
        html_files: List of HTML file paths to convert
        output_path: Path where output file should be saved
        
    Raises:
        ValueError: If html_files is empty
        IOError: If output_path is not writable
    """
    if not html_files:
        raise ValueError("No HTML files provided")
    
    try:
        # Conversion logic here
        pass
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Cleanup code here
        pass
```

## Adding New Converters

To add a new conversion method:

1. **Create converter file**
   ```bash
   touch src/converters/your_method_converter.py
   ```

2. **Implement conversion functions**
   ```python
   def convert_to_pdf_yourmethod(html_files: List[Path], output_path: str):
       """Convert HTML slides to PDF using YourMethod."""
       # Implementation
       pass
   
   def convert_to_ppt_yourmethod(html_files: List[Path], output_path: str):
       """Convert HTML slides to PPT using YourMethod."""
       # Implementation
       pass
   ```

3. **Export in `converters/__init__.py`**
   ```python
   from .your_method_converter import convert_to_pdf_yourmethod, convert_to_ppt_yourmethod
   
   __all__ = [
       # ... existing exports
       'convert_to_pdf_yourmethod',
       'convert_to_ppt_yourmethod',
   ]
   ```

4. **Add dependency checks in `utils/dependencies.py`**
   ```python
   elif method == "yourmethod":
       try:
           import yourmethod_package
       except ImportError:
           missing_packages.append("yourmethod-package")
   ```

5. **Update CLI in `cli.py`**
   - Add method to choices in argument parser
   - Add routing in `run_conversion()` function

6. **Update documentation**
   - Add method to README.md
   - Update method comparison table

## Testing Checklist

Before submitting a PR, ensure:

- [ ] Code runs without errors
- [ ] Both PDF and PPT conversion work
- [ ] Both Playwright and WeasyPrint methods work
- [ ] Template generation works
- [ ] Dependency auto-install works
- [ ] Error handling works (test with invalid inputs)
- [ ] Documentation is updated
- [ ] No new warnings or errors

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in GitHub Discussions
- Reach out to maintainers

Thank you for contributing! 🎉
