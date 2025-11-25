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

## [Unreleased]

### Planned
- Docker support
- GitHub Actions workflow
- Unit tests
- Integration tests
- Web UI
