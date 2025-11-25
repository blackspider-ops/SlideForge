# HTML Slides Converter

Convert HTML slides to PowerPoint (PPT) or PDF format with full styling preserved. This CLI tool automatically handles dependencies, creates template slides, and provides robust error handling.

## Features

✨ **Smart Dependency Management** - Automatically detects and installs missing dependencies  
🎨 **Perfect Rendering** - Preserves all fonts, styles, layouts, and visual design  
📝 **Template Generation** - Creates template HTML slides if none exist  
🛡️ **Robust Error Handling** - Gracefully handles edge cases and partial failures  
🚀 **Two Conversion Methods** - Choose between Playwright (best quality) or WeasyPrint (pure Python)  
📦 **Auto File Extension** - Automatically adds .pdf or .pptx extensions  
⚠️ **Overwrite Protection** - Asks before overwriting existing files  

## Quick Start

1. **Navigate to src folder:**
```bash
cd src
```

2. **Create virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Run the converter** (dependencies will auto-install):
```bash
# Convert to PDF
python converter.py --format pdf

# Convert to PowerPoint
python converter.py --format ppt
```

That's it! The script will:
- Detect missing dependencies and ask to install them
- Check for HTML slides in `../slides` folder
- Offer to create template slides if none exist
- Convert and save to `../output` folder

## Installation Methods

### Method 1: Automatic (Recommended)
Just run the converter - it will detect and install missing dependencies automatically:
```bash
python converter.py --format pdf
# When prompted, type 'y' to install dependencies
```

### Method 2: Manual Installation

#### Playwright (Recommended - Best Quality)
```bash
pip install playwright python-pptx pillow PyPDF2
playwright install chromium
```
- **Best rendering quality**
- Preserves all fonts, styles, layouts, and visual design
- Works for both PDF and PPT
- Requires Chromium browser (auto-installed)

#### WeasyPrint (Pure Python Alternative)
```bash
pip install weasyprint python-pptx PyPDF2 pdf2image
brew install poppler  # macOS (required for PPT conversion)
```
- No browser needed
- Pure Python solution
- May not render some fonts/styles perfectly
- Requires poppler for PPT conversion

## Usage Examples

### Basic Usage
```bash
# Convert to PDF (uses Playwright by default)
python converter.py --format pdf

# Convert to PowerPoint (uses Playwright by default)
python converter.py --format ppt
```

### Custom Output Names
```bash
# Short form with -o
python converter.py --format pdf -o presentation

# Long form with --output
python converter.py --format ppt --output my-slides.pptx

# Extensions are added automatically if missing
python converter.py --format pdf -o myfile  # Creates myfile.pdf
```

### Using WeasyPrint Method
```bash
# Convert to PDF with WeasyPrint
python converter.py --format pdf --method weasyprint

# Convert to PowerPoint with WeasyPrint
python converter.py --format ppt --method weasyprint
```

### Custom Directories
```bash
# Specify custom slides and output directories
python converter.py --format ppt --slides-dir ./my-slides --output-dir ./exports

# Use absolute paths
python converter.py --format pdf --slides-dir /path/to/slides --output-dir /path/to/output
```

### Complete Example
```bash
python converter.py \
  --format ppt \
  --method playwright \
  -o final-presentation \
  --slides-dir ../slides \
  --output-dir ../output
```

## Template Slide Generation

If the slides folder doesn't exist or is empty, the converter will offer to create template HTML slides:

```bash
python converter.py --format pdf

# Output:
# No HTML files found in: /path/to/slides
# Would you like to create template HTML slides? (y/n): y
# How many HTML slides do you need? 5
# Creating 5 template HTML slides...
# ✓ Created 5 template slides in /path/to/slides
```

Template slides include:
- Proper HTML5 structure
- Google Fonts (Montserrat, Inter)
- Material Icons support
- Responsive 1280x720 dimensions
- Basic styling and placeholder content
- Ready to edit and customize

## Method Comparison

| Feature | Playwright | WeasyPrint |
|---------|-----------|------------|
| **PDF Support** | ✓ Excellent | ✓ Good |
| **PPT Support** | ✓ Excellent | ✓ Good |
| **Rendering Quality** | Excellent | Good |
| **Font Support** | Perfect | May vary |
| **Google Fonts** | ✓ Full support | Limited |
| **Material Icons** | ✓ Full support | Limited |
| **Complex CSS** | ✓ Full support | Partial |
| **Dependencies** | Chromium browser | Poppler (for PPT) |
| **Installation** | Auto-install | Manual (poppler) |
| **Speed** | Fast | Fast |
| **Pure Python** | ✗ | ✓ |

**Recommendation:** Use Playwright for best results. It perfectly preserves all styling, fonts, and layouts.

## Command-Line Options

| Option | Short | Required | Default | Description |
|--------|-------|----------|---------|-------------|
| `--format` | - | ✓ | - | Output format: `pdf` or `ppt` |
| `--method` | - | ✗ | `playwright` | Conversion method: `playwright` or `weasyprint` |
| `--output` | `-o` | ✗ | `slides.pdf` or `slides.pptx` | Custom output filename |
| `--slides-dir` | - | ✗ | `../slides` | Directory containing HTML slides |
| `--output-dir` | - | ✗ | `../output` | Output directory for converted files |

## Project Structure

```
project/
├── src/
│   ├── converter.py              # Main entry point
│   ├── cli.py                    # CLI logic and workflow
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                 # This file
│   │
│   ├── converters/               # Conversion implementations
│   │   ├── __init__.py
│   │   ├── playwright_converter.py
│   │   └── weasyprint_converter.py
│   │
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── dependencies.py       # Dependency management
│       └── file_utils.py         # File operations
│
├── slides/                       # HTML slides (auto-created if missing)
│   ├── page1.html
│   ├── page2.html
│   └── ...
│
└── output/                       # Converted files (auto-created)
    ├── slides.pdf
    └── slides.pptx
```

### Modular Architecture

The project uses a clean, modular architecture for maintainability and extensibility:

- **converter.py** - Entry point with error handling
- **cli.py** - Command-line interface and workflow orchestration
- **converters/** - Pluggable conversion methods (Playwright, WeasyPrint)
- **utils/** - Reusable utilities (dependencies, file operations)

## Error Handling

The converter includes comprehensive error handling:

✓ **Missing Dependencies** - Auto-detects and offers to install  
✓ **Missing Slides Folder** - Offers to create template slides  
✓ **Empty Slides Folder** - Offers to create template slides  
✓ **Missing Output Folder** - Auto-creates on conversion  
✓ **Corrupted HTML Files** - Skips and continues with others  
✓ **File Permission Issues** - Clear error messages  
✓ **Existing Output Files** - Asks before overwriting  
✓ **Partial Conversions** - Completes with warnings  
✓ **Network Timeouts** - 30-second timeout per slide  
✓ **Keyboard Interrupts** - Clean exit on Ctrl+C  

## Troubleshooting

### Dependencies Won't Install
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Then try again
python converter.py --format pdf
```

### Playwright Browser Issues
```bash
# Manually install Chromium
playwright install chromium

# Or reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium
```

### WeasyPrint PPT Conversion Fails
```bash
# Install poppler (required for pdf2image)
brew install poppler  # macOS
sudo apt-get install poppler-utils  # Linux
```

### Permission Denied Errors
```bash
# Make sure you have write permissions
chmod +w ../output

# Or specify a different output directory
python converter.py --format pdf --output-dir ~/Documents/output
```

### HTML Files Not Found
```bash
# Check slides directory path
ls ../slides

# Or specify custom path
python converter.py --format pdf --slides-dir /path/to/your/slides
```

## Advanced Usage

### Batch Processing
```bash
# Process multiple formats
python converter.py --format pdf
python converter.py --format ppt

# With different methods
python converter.py --format pdf --method playwright -o high-quality
python converter.py --format pdf --method weasyprint -o fast-version
```

### Custom Slide Dimensions
Edit the HTML template or existing slides to change dimensions:
```css
.slide {
    width: 1920px;   /* Change width */
    min-height: 1080px;  /* Change height */
}
```

### Integration with Scripts
```bash
#!/bin/bash
# Build and convert slides

# Generate slides from markdown or other sources
# ... your slide generation code ...

# Convert to both formats
python src/converter.py --format pdf -o presentation
python src/converter.py --format ppt -o presentation

echo "Conversion complete!"
```

## Requirements

- **Python**: 3.7 or higher
- **Operating System**: macOS, Linux, or Windows
- **Disk Space**: ~200MB for Chromium browser (Playwright)
- **Internet**: Required for initial dependency installation and font loading

## Development

### Project Architecture

This project follows a modular architecture with clear separation of concerns:

- **Entry Point**: `converter.py` 
- **CLI Logic**: `cli.py` 
- **Converters**: Separate modules for each conversion method
- **Utilities**: Reusable components for dependencies and file operations

Each module is focused, testable, and production-ready. See `PROJECT_STRUCTURE.md` for details.

### Adding New Converters

To add a new conversion method:

1. Create `converters/your_method_converter.py`
2. Implement conversion functions
3. Export in `converters/__init__.py`
4. Add dependency checks in `utils/dependencies.py`
5. Update CLI routing in `cli.py`

### Code Quality

- **Modular Design**: ~150 lines per module (manageable size)
- **Error Handling**: Comprehensive try-except with cleanup
- **Type Hints**: Used throughout for clarity
- **Documentation**: Docstrings for all functions
- **Production Ready**: Robust error handling and edge case coverage

## License

This project is open source and available for personal and commercial use.

## Support

For issues, questions, or contributions:
1. Check the Troubleshooting section above
2. Review error messages carefully - they include helpful hints
3. Ensure all dependencies are properly installed
4. Try both conversion methods to compare results

## Tips for Best Results

1. **Use Playwright** for production-quality conversions
2. **Test with one slide first** before converting large presentations
3. **Keep HTML files simple** for better compatibility
4. **Use web-safe fonts** or include font files locally
5. **Optimize images** in HTML for faster processing
6. **Check output** after conversion to ensure quality
7. **Use templates** as starting points for consistent styling
