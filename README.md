# SlideForge

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Forge your HTML slides into PowerPoint or PDF with perfect styling preservation. A production-ready CLI tool with automatic dependency management and robust error handling.

![Demo](https://via.placeholder.com/800x400/1D9BF0/ffffff?text=SlideForge)

## ✨ Features

- 🎨 **Perfect Rendering** - Preserves all fonts, styles, layouts, and visual design
- 🤖 **Smart Dependencies** - Automatically detects and installs missing packages
- 📝 **Template Generation** - Creates starter HTML slides if none exist
- 🛡️ **Robust Error Handling** - Gracefully handles edge cases and partial failures
- 🚀 **Two Methods** - Playwright (best quality) or WeasyPrint (pure Python)
- 📦 **Auto Extensions** - Automatically adds .pdf or .pptx extensions
- ⚠️ **Overwrite Protection** - Asks before overwriting existing files
- 🏗️ **Modular Architecture** - Clean, maintainable, production-ready code
- 🔢 **Smart Sorting** - Correctly orders slides numerically (page1, page2... page10)
- 🖥️ **Cross-Platform** - Works on macOS, Linux, and Windows with simple launchers

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/blackspider-ops/SlideForge.git
cd SlideForge

# Run SlideForge
# macOS/Linux:
./slideforge.sh --format pdf

# Windows:
slideforge.bat --format pdf

# Or use Python directly (works everywhere):
python slideforge.py --format pdf
```

That's it! The launcher will:
- ✅ Check Python version
- ✅ Create virtual environment automatically
- ✅ Install dependencies if needed
- ✅ Run the converter

### Alternative: Direct Usage

```bash
# Navigate to src folder
cd src

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the converter
python converter.py --format pdf
```

## 📖 Usage

### Basic Commands

**macOS/Linux:**
```bash
# Convert to PDF (uses Playwright by default)
./slideforge.sh --format pdf

# Convert to PowerPoint
./slideforge.sh --format ppt

# Use WeasyPrint method
./slideforge.sh --format pdf --method weasyprint
```

**Windows:**
```cmd
# Convert to PDF (uses Playwright by default)
slideforge.bat --format pdf

# Convert to PowerPoint
slideforge.bat --format ppt

# Use WeasyPrint method
slideforge.bat --format pdf --method weasyprint
```

**Cross-platform (Python):**
```bash
python slideforge.py --format pdf
python slideforge.py --format ppt
```

### Custom Output

**macOS/Linux:**
```bash
./slideforge.sh --format pdf -o presentation
./slideforge.sh --format ppt --output my-slides.pptx
```

**Windows:**
```cmd
slideforge.bat --format pdf -o presentation
slideforge.bat --format ppt --output my-slides.pptx
```

### Custom Directories

**macOS/Linux:**
```bash
./slideforge.sh --format ppt \
  --slides-dir ./my-slides \
  --output-dir ./exports
```

**Windows:**
```cmd
slideforge.bat --format ppt --slides-dir ./my-slides --output-dir ./exports
```

## 📋 Requirements

- Python 3.7+
- macOS, Linux, or Windows
- ~200MB disk space (for Chromium browser if using Playwright)

## 🎯 Use Cases

- **Presentations** - Convert web-based slides to PowerPoint
- **Documentation** - Generate PDF documentation from HTML
- **Archiving** - Save HTML presentations in portable formats
- **Batch Processing** - Convert multiple slide decks automatically
- **CI/CD** - Integrate into build pipelines

## 🔧 Installation Methods

### Method 1: Automatic (Recommended)
Just run the converter - it detects and installs dependencies automatically:
```bash
python converter.py --format pdf
# Type 'y' when prompted to install dependencies
```

### Method 2: Manual
```bash
# For Playwright (best quality)
pip install playwright python-pptx pillow PyPDF2
playwright install chromium

# For WeasyPrint (pure Python)
pip install weasyprint python-pptx PyPDF2 pdf2image
brew install poppler  # macOS only, for PPT conversion
```

## 📊 Method Comparison

| Feature | Playwright | WeasyPrint |
|---------|-----------|------------|
| PDF Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| PPT Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Google Fonts | ✅ Full | ⚠️ Limited |
| Complex CSS | ✅ Full | ⚠️ Partial |
| Dependencies | Chromium | Poppler (PPT only) |
| Pure Python | ❌ | ✅ |

**Recommendation:** Use Playwright for production-quality conversions.

## Tips for Best Results

1. **Use Playwright** for production-quality conversions
2. **Test with one slide first** before converting large presentations
3. **Keep HTML files simple** for better compatibility
4. **Use web-safe fonts** or include font files locally
5. **Optimize images** in HTML for faster processing
6. **Check output** after conversion to ensure quality
7. **Use templates** as starting points for consistent styling


## 🏗️ Project Structure

```
slideforge/
├── src/
│   ├── converter.py              # Entry point
│   ├── cli.py                    # CLI logic
│   ├── requirements.txt          # Dependencies
│   ├── README.md                 # Documentation
│   ├── converters/               # Conversion methods
│   │   ├── playwright_converter.py
│   │   └── weasyprint_converter.py
│   └── utils/                    # Utilities
│       ├── dependencies.py
│       └── file_utils.py
├── slides/                       # HTML slides (auto-created)
├── output/                       # Converted files (auto-created)
├── LICENSE
└── README.md                     # This file
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Adding New Converters

To add a new conversion method:

1. Create `src/converters/your_method_converter.py`
2. Implement `convert_to_pdf_yourmethod()` and/or `convert_to_ppt_yourmethod()`
3. Export functions in `src/converters/__init__.py`
4. Add dependency checks in `src/utils/dependencies.py`
5. Update CLI routing in `src/cli.py`

## 🐛 Troubleshooting

### Dependencies Won't Install
```bash
pip install --upgrade pip setuptools wheel
python converter.py --format pdf
```

### Playwright Browser Issues
```bash
playwright install chromium
```

### WeasyPrint PPT Fails
```bash
brew install poppler  # macOS
sudo apt-get install poppler-utils  # Linux
```

### Permission Errors
```bash
chmod +w ../output
# Or specify different directory
python converter.py --format pdf --output-dir ~/Documents/output
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [WeasyPrint](https://weasyprint.org/) - HTML to PDF conversion
- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint generation
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF manipulation

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/blackspider-ops/SlideForge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/blackspider-ops/SlideForge/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

Made with ❤️ by [blackspider-ops](https://github.com/blackspider-ops)
