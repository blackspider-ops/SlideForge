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
- 🗑️ **Clean Command** - Safely delete all slides with double confirmation for fresh start
- 📋 **List Slides** - Preview all slides before converting
- 🎯 **Range Selection** - Convert only specific slides (e.g., 1-5 or 1,3,5)
- 🔍 **Dry Run** - Preview conversion without creating files
- 📌 **Version Info** - Check current version with `--version`
- ⚙️ **Config File** - Save preferences in `~/.slideforge/config.json`
- 🔄 **Batch Mode** - Convert to both PDF and PPT at once
- 🤫 **Quiet Mode** - Minimal output for automation
- 📢 **Verbose Mode** - Detailed logging for debugging
- 👀 **Watch Mode** - Auto-convert when files change
- 📏 **Custom Dimensions** - Override default slide size
- 📎 **Merge PDFs** - Combine multiple PDF outputs
- ⚡ **Parallel Processing** - Up to 4x faster with multi-threading
- 🚀 **Scalable Workers** - Control parallel workers for optimal performance
- 🔄 **Format Conversion** - Convert PDF ↔ PPT (NEW in v1.6.0!)

## 🚀 Quick Start

### macOS/Linux

```bash
# Clone the repository
git clone https://github.com/blackspider-ops/SlideForge.git
cd SlideForge

# Make the launcher executable (first time only)
chmod +x slideforge.sh

# Run SlideForge
./slideforge.sh --format pdf
```

### Windows

```cmd
# Clone the repository
git clone https://github.com/blackspider-ops/SlideForge.git
cd SlideForge

# Run SlideForge (no setup needed)
slideforge.bat --format pdf
```

That's it! The launcher will:
- ✅ Check Python version
- ✅ Create virtual environment automatically
- ✅ Install dependencies if needed
- ✅ Run the converter

### Troubleshooting First Run

**macOS/Linux - Permission Denied:**
```bash
# If you get "Permission denied" error
chmod +x slideforge.sh
./slideforge.sh --format pdf
```

**Windows - Script Execution Policy:**
```powershell
# If you get execution policy error in PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
slideforge.bat --format pdf
```

### Advanced: Direct Python Usage

```bash
# If you prefer to use Python directly
python src/main.py --format pdf

# Or activate venv and use converter directly
cd src
source venv/bin/activate  # On Windows: venv\Scripts\activate
python converter.py --format pdf
```

## 📖 Usage

### Basic Commands

**macOS/Linux:**
```bash
# Smart format detection (NEW in v1.5.1!)
./slideforge.sh pdf                       # Convert to PDF
./slideforge.sh ppt                       # Convert to PowerPoint

# Short aliases (NEW in v1.5.1!)
./slideforge.sh pdf -m weasyprint         # Use WeasyPrint
./slideforge.sh ppt -o presentation       # Custom output
./slideforge.sh pdf -r 1-5                # Range selection
./slideforge.sh pdf -p -w 8               # Parallel with 8 workers

# Traditional syntax (still works)
./slideforge.sh --format pdf
./slideforge.sh --format ppt

# List all slides
./slideforge.sh --list                    # or -l

# Dry run (preview without converting)
./slideforge.sh pdf --dry-run             # or -n

# Convert specific slides only
./slideforge.sh pdf --range 1-5           # or -r 1-5
./slideforge.sh ppt -r 1,3,5,7

# Clean slides directory
./slideforge.sh --clean                   # or -c

# Show version
./slideforge.sh --version                 # or -V

# Configuration
./slideforge.sh --show-config
./slideforge.sh --set-config method playwright

# Batch mode (convert to both formats)
./slideforge.sh --batch                   # or -b

# Quiet mode (minimal output)
./slideforge.sh pdf --quiet               # or -q

# Verbose mode (detailed logging)
./slideforge.sh pdf --verbose             # or -v

# Watch mode (auto-convert on changes)
./slideforge.sh pdf --watch               # or -w

# Parallel processing (faster)
./slideforge.sh pdf --parallel            # or -p
./slideforge.sh pdf -p --workers 8

# Format conversion (NEW in v1.6.0!)
./slideforge.sh --convert-from pdf --input presentation.pdf --format ppt
./slideforge.sh --convert-from ppt --input slides.pptx --format pdf -o output.pdf
```

**Windows:**
```cmd
# Smart format detection (NEW in v1.5.1!)
slideforge.bat pdf                        # Convert to PDF
slideforge.bat ppt                        # Convert to PowerPoint

# Short aliases (NEW in v1.5.1!)
slideforge.bat pdf -m weasyprint          # Use WeasyPrint
slideforge.bat ppt -o presentation        # Custom output
slideforge.bat pdf -r 1-5                 # Range selection

# Traditional syntax (still works)
slideforge.bat --format pdf
slideforge.bat --format ppt

# All other commands work the same as macOS/Linux
slideforge.bat --list                     # or -l
slideforge.bat pdf --dry-run              # or -n
slideforge.bat --clean                    # or -c
slideforge.bat --version                  # or -V
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

## 📐 HTML Slide Guidelines

**Important:** For best results, your HTML slides should fit within **1280x720px** dimensions.

### Quick Tips

1. **Use fixed height** - Set `.slide { height: 720px; }` not `min-height`
2. **Keep padding moderate** - Header: ~35px top, Content: ~25px bottom
3. **Use appropriate font sizes** - Title: 36-40px, Body: 16-18px
4. **Test problematic slides** - Use `--range` flag to test specific slides

### Common Issues

**Content cut off at bottom?**
- Reduce header/content padding
- Decrease font sizes slightly
- Reduce margins between elements

**Slide spans multiple pages?**
- Total content height exceeds 720px
- See [FORMAT.md](FORMAT.md) for detailed fixes

📖 **See [FORMAT.md](FORMAT.md) for complete HTML formatting guidelines and troubleshooting**

## Tips for Best Results

1. **Use Playwright** for production-quality conversions
2. **Follow HTML guidelines** in [FORMAT.md](FORMAT.md) to avoid layout issues
3. **Test with one slide first** before converting large presentations
4. **Keep HTML files simple** for better compatibility
5. **Use web-safe fonts** or include font files locally
6. **Optimize images** in HTML for faster processing
7. **Check output** after conversion to ensure quality
8. **Use templates** as starting points for consistent styling


## 🏗️ Project Structure

```
slideforge/
├── slideforge.sh                 # macOS/Linux launcher
├── slideforge.bat                # Windows launcher
├── src/
│   ├── main.py                   # Main launcher script
│   ├── converter.py              # Converter entry point
│   ├── cli.py                    # CLI logic
│   ├── converters/               # Conversion methods
│   │   ├── playwright_converter.py
│   │   └── weasyprint_converter.py
│   └── utils/                    # Utilities
│       ├── dependencies.py
│       └── file_utils.py
├── slides/                       # HTML slides (auto-created)
├── output/                       # Converted files (auto-created)
├── requirements.txt              # Python dependencies
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
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
