# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-24

### Added
- Initial release
- HTML to PDF conversion using Playwright
- HTML to PPT conversion using Playwright
- HTML to PDF conversion using WeasyPrint
- HTML to PPT conversion using WeasyPrint
- Automatic dependency detection and installation
- Template HTML slide generation
- Automatic file extension handling
- Overwrite protection for existing files
- Comprehensive error handling
- Modular architecture with clean separation of concerns
- CLI with argument parsing
- Support for custom output names and directories
- Graceful handling of corrupted or missing HTML files
- Cleanup of temporary files
- Progress indicators during conversion
- Detailed documentation

### Features
- Two conversion methods (Playwright and WeasyPrint)
- Auto-install missing dependencies
- Create template slides if none exist
- Convert to PDF or PowerPoint
- Preserve all styling, fonts, and layouts
- Handle partial conversions gracefully
- 30-second timeout per slide
- Keyboard interrupt handling

## [1.3.0] - 2024-11-24

### Added
- `--version` flag to show version information
- `--list` command to preview all slides before converting
- `--dry-run` flag to preview conversion without creating files
- `--range` option to convert specific slides (e.g., 1-5 or 1,3,5)
- Version module (`src/version.py`) for centralized version management
- Range parsing with support for ranges (1-5) and comma-separated values (1,3,5)

### Improved
- Better workflow with preview and dry-run capabilities
- More control over which slides to convert
- Enhanced user experience with list and version commands

## [1.2.0] - 2024-11-24

### Added
- `--clean` command to delete all slides with double confirmation
- OS-aware usage messages (shows correct command for Windows/Mac/Linux)
- chmod instructions in README for macOS/Linux users

### Changed
- Renamed `slideforge.py` to `src/main.py` for better organization
- Updated all launchers to use `src/main.py`
- Simplified Quick Start guide with platform-specific instructions
- Updated project structure documentation
- All examples now use `.sh` or `.bat` files instead of Python directly

### Improved
- Better project organization with main.py in src folder
- Clearer documentation for first-time users
- More intuitive command structure

## [1.1.0] - 2024-11-24

### Added
- Cross-platform launcher scripts (slideforge.sh, slideforge.bat)
- Automatic virtual environment creation
- Automatic dependency installation
- venv module detection and installation (Linux)
- Natural sorting for HTML files (fixes page1, page10, page2 issue)

### Fixed
- File sorting now works numerically (page1, page2, ... page9, page10)
- Virtual environment Python verification before installing dependencies
- Requirements.txt path detection (checks root and src folders)

### Changed
- Moved requirements.txt to project root (standard convention)
- Added slides/ folder to .gitignore
- Improved launcher with better error messages and progress indicators

## [1.4.0] - 2024-11-24

### Added
- **Config file support** - Save preferences in `~/.slideforge/config.json`
- `--show-config` - Display current configuration
- `--set-config KEY VALUE` - Set configuration values
- `--batch` - Convert to both PDF and PPT at once
- `--quiet` / `-q` - Minimal output for automation
- `--verbose` / `-v` - Detailed logging
- `--watch` - Auto-convert when HTML files change (requires watchdog)
- `--dimensions` - Custom slide dimensions (e.g., 1920x1080)
- `--merge-pdf` - Merge with another PDF file
- Progress bar support with tqdm (optional)
- Watch mode with watchdog (optional)

### Improved
- Configuration management system
- Better output control (quiet/verbose modes)
- Workflow automation with watch mode
- Batch processing for multiple formats

### Dependencies
- Added optional: tqdm (progress bars)
- Added optional: watchdog (watch mode)

## [1.5.0] - 2024-11-24

### Added
- **Parallel processing** - `--parallel` flag for faster conversions
- `--workers N` - Control number of parallel workers (default: 4)
- Multi-threaded conversion for Playwright method
- Progress bars with tqdm during parallel conversion
- Automatic temp file cleanup

### Improved
- Significantly faster conversion for large slide decks
- Better resource utilization with parallel workers
- Real-time progress tracking

### Performance
- Up to 4x faster conversion with 4 workers
- Scales with number of CPU cores

## [1.5.1] - 2024-11-24

### Added
- **Smart format detection** - Just type `pdf` or `ppt` without `--format`
- **Short aliases** for all commands:
  - `-f` for `--format`
  - `-m` for `--method`
  - `-o` for `--output`
  - `-s` for `--slides-dir`
  - `-d` for `--output-dir`
  - `-l` for `--list`
  - `-c` for `--clean`
  - `-n` for `--dry-run`
  - `-V` for `--version`
  - `-r` for `--range`
  - `-q` for `--quiet`
  - `-v` for `--verbose`
  - `-b` for `--batch`
  - `-w` for `--watch`
  - `-p` for `--parallel`

### Improved
- Simpler command syntax
- Faster typing with short aliases
- More intuitive usage

## [1.6.0] - 2024-11-24

### Added
- **PDF to PPT conversion** - `--convert-from pdf --input file.pdf --format ppt`
- **PPT to PDF conversion** - `--convert-from ppt --input file.pptx --format pdf`
- `--input` / `-i` flag for specifying input files
- Format converter module for file format conversions
- LibreOffice integration for high-quality PPT to PDF (optional)

### Improved
- Extended SlideForge beyond HTML conversion
- Support for converting existing presentations
- Flexible input/output workflows

## [2.0.0] - 2024-11-25

### Added
- **PDF to PNG conversion** - `--convert-from pdf --input file.pdf --format png`
- `-C` short alias for `--convert-from`
- High-resolution PNG export (300 DPI)
- Each PDF page becomes a separate PNG image
- Automatic PNG file naming (filename_page1.png, filename_page2.png, etc.)

### Fixed
- HTML to PDF conversion now ensures each slide fits on one page
- Optimized HTML slide layouts to prevent content overflow
- Fixed multi-page PDF generation for tall content
- Improved PPT to PDF conversion with better image extraction
- Fixed blank PDF output in format conversion

### Improved
- Better handling of HTML content that exceeds 720px height
- Reduced padding and margins in HTML templates for better fit
- Enhanced format conversion reliability
- More robust error handling in conversion workflows

### Changed
- Updated description to include PNG format support
- Improved format conversion error messages

## [Unreleased]

### Planned
- Docker support
- GitHub Actions workflow
- Unit tests
- Integration tests
- Web UI
