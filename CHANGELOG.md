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

## [Unreleased]

### Planned
- Batch processing mode
- Configuration file support
- Custom slide dimensions
- Progress bar for large conversions
- Parallel processing for faster conversions
- Docker support
- GitHub Actions workflow
- Unit tests
- Integration tests
