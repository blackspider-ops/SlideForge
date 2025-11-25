"""Command-line interface for SlideForge."""

import sys
import argparse
from pathlib import Path
import time

from version import __version__, __author__, __description__
from config import load_config, show_config, set_config_value
from utils.dependencies import check_and_install_dependencies
from utils.file_utils import get_html_files, create_template_slide
from converters import (
    convert_to_pdf_playwright,
    convert_to_ppt_playwright,
    convert_to_pdf_weasyprint,
    convert_to_ppt_weasyprint,
)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert HTML slides to PPT or PDF using different methods',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Methods:
  1. playwright  - Best quality, requires browser (default)
  2. weasyprint  - Pure Python, no browser needed

Examples:
  ./slideforge.sh pdf                       # Smart format detection
  ./slideforge.sh ppt                       # Smart format detection
  ./slideforge.sh --format pdf              # Explicit format
  ./slideforge.sh -f pdf -m weasyprint      # Short aliases
  ./slideforge.sh pdf -o my-slides          # Combined
  ./slideforge.sh --clean                   # Delete all slides
        """
    )
    
    parser.add_argument(
        'format_arg',
        nargs='?',
        choices=['pdf', 'ppt', 'png'],
        help='Output format: pdf, ppt, or png (can be used without --format)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['pdf', 'ppt', 'png'],
        required=False,
        help='Output format: pdf, ppt, or png'
    )
    
    parser.add_argument(
        '--convert-from', '-C',
        choices=['pdf', 'ppt'],
        help='Convert from existing PDF or PPT file (use with --input and --format)'
    )
    
    parser.add_argument(
        '--input', '-i',
        help='Input file for format conversion (PDF or PPT)',
        default=None
    )
    
    parser.add_argument(
        '--method', '-m',
        choices=['playwright', 'weasyprint'],
        default=None,  # None means not specified, will use config or fallback
        help='Conversion method (default: playwright or from config)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename (default: slides.pdf or slides.pptx)',
        default=None
    )
    
    parser.add_argument(
        '--slides-dir', '-s',
        help='Directory containing HTML slides (default: ../slides)',
        default='../slides'
    )
    
    parser.add_argument(
        '--output-dir', '-d',
        help='Output directory (default: ../output)',
        default='../output'
    )
    
    parser.add_argument(
        '--clean', '-c',
        action='store_true',
        help='Delete all HTML files in slides directory (requires confirmation)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all HTML slides in the slides directory'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be converted without actually converting'
    )
    
    parser.add_argument(
        '--version', '-V',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--range', '-r',
        help='Convert only specific slides (e.g., 1-5 or 1,3,5)',
        default=None
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output (quiet mode)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Detailed output (verbose mode)'
    )
    
    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Convert to both PDF and PPT formats'
    )
    
    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Show current configuration'
    )
    
    parser.add_argument(
        '--set-config',
        nargs=2,
        metavar=('KEY', 'VALUE'),
        help='Set a configuration value (e.g., --set-config method playwright)'
    )
    
    parser.add_argument(
        '--watch', '-w',
        action='store_true',
        help='Watch slides directory and auto-convert on changes'
    )
    
    parser.add_argument(
        '--dimensions',
        help='Custom slide dimensions (e.g., 1920x1080)',
        default=None
    )
    
    parser.add_argument(
        '--merge-pdf',
        help='Merge with another PDF file',
        default=None
    )
    
    parser.add_argument(
        '--parallel', '-p',
        action='store_true',
        help='Use parallel processing for faster conversion'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    return parser.parse_args()


def handle_missing_slides(slides_dir: Path):
    """Handle missing or empty slides directory."""
    if not slides_dir.exists():
        print(f"\nSlides directory not found: {slides_dir}")
    else:
        print(f"\nNo HTML files found in: {slides_dir}")
    
    response = input("\nWould you like to create template HTML slides? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Operation cancelled.")
        sys.exit(1)
    
    # Ask how many slides
    while True:
        try:
            num_slides = int(input("How many HTML slides do you need? "))
            if num_slides > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Create slides directory if it doesn't exist
    slides_dir.mkdir(parents=True, exist_ok=True)
    
    # Create template HTML files
    print(f"\nCreating {num_slides} template HTML slides...")
    created_count = 0
    for i in range(1, num_slides + 1):
        try:
            create_template_slide(slides_dir / f"page{i}.html", i)
            created_count += 1
        except Exception as e:
            print(f"Failed to create slide {i}: {e}")
    
    if created_count == 0:
        print("Error: Failed to create any template slides")
        sys.exit(1)
    
    print(f"✓ Created {created_count} template slides in {slides_dir}")
    print("\nPlease edit the HTML files with your content, then run the converter again.")
    sys.exit(0)


def prepare_output_path(args, output_dir: Path) -> Path:
    """Prepare and validate output path."""
    # Determine output filename
    if args.output:
        output_filename = args.output
        # Add extension if missing
        if args.format == 'pdf':
            if not output_filename.lower().endswith('.pdf'):
                output_filename += '.pdf'
        else:  # ppt
            if not output_filename.lower().endswith('.pptx'):
                output_filename += '.pptx'
    else:
        output_filename = f"slides.pptx" if args.format == 'ppt' else "slides.pdf"
    
    output_path = output_dir / output_filename
    
    return output_path


def run_conversion(args, html_files, output_path: Path):
    """Execute the conversion based on format and method."""
    formats_to_convert = ['pdf', 'ppt'] if args.batch else [args.format]
    
    for fmt in formats_to_convert:
        if args.batch and not args.quiet:
            print(f"\n{'='*60}")
            print(f"Converting to {fmt.upper()}...")
            print(f"{'='*60}\n")
        
        # Adjust output path for current format
        if args.batch:
            ext = '.pptx' if fmt == 'ppt' else '.pdf'
            current_output = output_path.parent / (output_path.stem + ext)
        else:
            current_output = output_path
        
        # Convert with parallel processing if enabled
        if args.parallel and args.method == 'playwright':
            from converters.parallel_converter import (
                parallel_convert_to_pdf_playwright,
                parallel_convert_to_ppt_playwright
            )
            
            if fmt == 'pdf':
                parallel_convert_to_pdf_playwright(html_files, str(current_output), args.workers, args.quiet)
            else:  # ppt
                parallel_convert_to_ppt_playwright(html_files, str(current_output), args.workers, args.quiet)
        else:
            # Standard sequential conversion
            if fmt == 'pdf':
                if args.method == 'playwright':
                    convert_to_pdf_playwright(html_files, str(current_output))
                elif args.method == 'weasyprint':
                    convert_to_pdf_weasyprint(html_files, str(current_output))
            else:  # ppt
                if args.method == 'playwright':
                    convert_to_ppt_playwright(html_files, str(current_output))
                elif args.method == 'weasyprint':
                    convert_to_ppt_weasyprint(html_files, str(current_output))
        
        if not args.quiet and not args.parallel:
            print(f"\n✓ {fmt.upper()} saved to: {current_output}")


def clean_slides_directory(slides_dir: Path):
    """Delete all HTML files in slides directory with double confirmation."""
    if not slides_dir.exists():
        print(f"Slides directory not found: {slides_dir}")
        return
    
    html_files = get_html_files(str(slides_dir))
    
    if not html_files:
        print(f"No HTML files found in {slides_dir}")
        return
    
    print(f"\n{'='*60}")
    print("⚠️  WARNING: DELETE ALL SLIDES")
    print(f"{'='*60}")
    print(f"\nThis will permanently delete {len(html_files)} HTML file(s) from:")
    print(f"  {slides_dir}")
    print("\nFiles to be deleted:")
    for i, file in enumerate(html_files[:10], 1):  # Show first 10
        print(f"  {i}. {file.name}")
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
            html_file.unlink()
            deleted_count += 1
        except Exception as e:
            print(f"  Failed to delete {html_file.name}: {e}")
            failed_count += 1
    
    print(f"\n✓ Deleted {deleted_count} file(s)")
    if failed_count > 0:
        print(f"⚠ Failed to delete {failed_count} file(s)")
    
    print(f"\n{'='*60}")
    print("Slides directory cleaned successfully!")
    print(f"{'='*60}\n")


def show_version():
    """Show version information."""
    print(f"\nSlideForge v{__version__}")
    print(f"{__description__}")
    print(f"Author: {__author__}")
    print(f"GitHub: https://github.com/blackspider-ops/SlideForge\n")


def list_slides(slides_dir: Path):
    """List all HTML slides in the directory."""
    if not slides_dir.exists():
        print(f"Slides directory not found: {slides_dir}")
        return
    
    html_files = get_html_files(str(slides_dir))
    
    if not html_files:
        print(f"No HTML files found in {slides_dir}")
        return
    
    print(f"\n{'='*60}")
    print(f"Found {len(html_files)} HTML slide(s) in {slides_dir}")
    print(f"{'='*60}\n")
    
    for i, file in enumerate(html_files, 1):
        size = file.stat().st_size / 1024  # KB
        print(f"  {i:2d}. {file.name:<30} ({size:.1f} KB)")
    
    print(f"\n{'='*60}\n")


def parse_range(range_str: str, total_slides: int) -> list:
    """Parse range string into list of indices."""
    indices = []
    
    try:
        # Handle comma-separated values: 1,3,5
        if ',' in range_str:
            for part in range_str.split(','):
                idx = int(part.strip()) - 1  # Convert to 0-based
                if 0 <= idx < total_slides:
                    indices.append(idx)
        # Handle range: 1-5
        elif '-' in range_str:
            start, end = range_str.split('-')
            start_idx = int(start.strip()) - 1
            end_idx = int(end.strip())
            indices = list(range(max(0, start_idx), min(end_idx, total_slides)))
        # Handle single number: 3
        else:
            idx = int(range_str.strip()) - 1
            if 0 <= idx < total_slides:
                indices.append(idx)
    except ValueError:
        print(f"Invalid range format: {range_str}")
        print("Use formats like: 1-5, 1,3,5, or 3")
        sys.exit(1)
    
    return indices


def watch_directory(slides_dir: Path, args):
    """Watch slides directory for changes and auto-convert."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Error: watchdog not installed")
        print("Install with: pip install watchdog")
        sys.exit(1)
    
    class SlideHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_modified = {}
        
        def on_modified(self, event):
            if event.is_directory or not event.src_path.endswith('.html'):
                return
            
            # Debounce - ignore if modified within last 2 seconds
            now = time.time()
            if event.src_path in self.last_modified:
                if now - self.last_modified[event.src_path] < 2:
                    return
            
            self.last_modified[event.src_path] = now
            
            if not args.quiet:
                print(f"\n🔄 Detected change: {Path(event.src_path).name}")
                print("Converting...")
            
            # Trigger conversion
            try:
                html_files = get_html_files(str(slides_dir))
                output_dir = (slides_dir.parent / args.output_dir).resolve()
                output_dir.mkdir(parents=True, exist_ok=True)
                
                output_filename = f"slides.{args.format}x" if args.format == 'ppt' else "slides.pdf"
                output_path = output_dir / output_filename
                
                if args.format == 'pdf':
                    if args.method == 'playwright':
                        convert_to_pdf_playwright(html_files, str(output_path))
                    else:
                        convert_to_pdf_weasyprint(html_files, str(output_path))
                else:
                    if args.method == 'playwright':
                        convert_to_ppt_playwright(html_files, str(output_path))
                    else:
                        convert_to_ppt_weasyprint(html_files, str(output_path))
                
                if not args.quiet:
                    print(f"✓ Converted to {output_path}")
            except Exception as e:
                print(f"❌ Conversion failed: {e}")
    
    event_handler = SlideHandler()
    observer = Observer()
    observer.schedule(event_handler, str(slides_dir), recursive=False)
    observer.start()
    
    print(f"\n{'='*60}")
    print(f"👀 Watching {slides_dir} for changes...")
    print("Press Ctrl+C to stop")
    print(f"{'='*60}\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\n⚠ Watch mode stopped")
    
    observer.join()


def run_converter():
    """Main converter logic."""
    args = parse_arguments()
    
    # Smart format detection - use positional arg if provided
    if args.format_arg:
        args.format = args.format_arg
    
    # Load config and apply defaults
    config = load_config()
    
    # Apply config defaults ONLY if args not explicitly provided
    if args.method is None:
        args.method = config.get('method', 'playwright')
    if args.slides_dir == '../slides':
        args.slides_dir = config.get('slides_dir', '../slides')
    if args.output_dir == '../output':
        args.output_dir = config.get('output_dir', '../output')
    
    # Handle show-config command
    if args.show_config:
        show_config()
        sys.exit(0)
    
    # Handle set-config command
    if args.set_config:
        key, value = args.set_config
        if set_config_value(key, value):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Handle version command
    if args.version:
        show_version()
        sys.exit(0)
    
    # Get script directory
    script_dir = Path(__file__).parent
    slides_dir = (script_dir / args.slides_dir).resolve()
    
    # Handle list command
    if args.list:
        list_slides(slides_dir)
        sys.exit(0)
    
    # Handle clean command
    if args.clean:
        clean_slides_directory(slides_dir)
        sys.exit(0)
    
    # Handle format conversion (PDF ↔ PPT)
    if args.convert_from:
        if not args.input:
            print("Error: --convert-from requires --input file")
            sys.exit(1)
        
        if not args.format:
            print("Error: --convert-from requires --format (target format)")
            sys.exit(1)
        
        # Check format conversion dependencies
        missing = []
        try:
            import reportlab
        except ImportError:
            missing.append("reportlab")
        
        if args.convert_from == 'pdf':
            try:
                import pdf2image
            except ImportError:
                missing.append("pdf2image")
        
        if missing:
            print(f"\n{'='*60}")
            print("Missing dependencies for format conversion!")
            print(f"{'='*60}\n")
            for pkg in missing:
                print(f"  - {pkg}")
            print(f"\n{'='*60}")
            response = input("Install missing dependencies? (y/n): ").strip().lower()
            if response == 'y':
                import subprocess
                for pkg in missing:
                    print(f"Installing {pkg}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                print("✓ Dependencies installed!\n")
            else:
                sys.exit(1)
        
        from converters.format_converter import convert_pdf_to_ppt, convert_ppt_to_pdf, convert_pdf_to_png
        
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}")
            sys.exit(1)
        
        # Determine output path
        output_dir = (script_dir / args.output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if args.output:
            output_filename = args.output
            ext = '.pptx' if args.format == 'ppt' else '.pdf'
            if not output_filename.lower().endswith(ext):
                output_filename += ext
        else:
            ext = '.pptx' if args.format == 'ppt' else '.pdf'
            output_filename = input_path.stem + '_converted' + ext
        
        output_path = output_dir / output_filename
        
        # Convert
        if args.convert_from == 'pdf' and args.format == 'ppt':
            convert_pdf_to_ppt(str(input_path), str(output_path), args.quiet)
        elif args.convert_from == 'pdf' and args.format == 'png':
            # For PNG, output_path is the directory
            output_dir = output_path.parent if args.output else output_dir
            convert_pdf_to_png(str(input_path), str(output_dir), args.quiet)
        elif args.convert_from == 'ppt' and args.format == 'pdf':
            convert_ppt_to_pdf(str(input_path), str(output_path), args.quiet)
        else:
            print(f"Error: Cannot convert {args.convert_from} to {args.format}")
            print("Supported conversions: PDF→PPT, PDF→PNG, PPT→PDF")
            sys.exit(1)
        
        sys.exit(0)
    
    # Validate format requirement (after smart detection)
    if not args.format and not args.batch:
        print("Error: Format is required. Use: pdf, ppt, --format pdf, or --batch")
        print("Examples:")
        print("  ./slideforge.sh pdf")
        print("  ./slideforge.sh --format ppt")
        print("  ./slideforge.sh --batch")
        sys.exit(1)
    
    # Handle watch mode
    if args.watch:
        if not args.format:
            print("Error: --watch requires a format")
            sys.exit(1)
        watch_directory(slides_dir, args)
        sys.exit(0)
    
    # Handle batch mode
    if args.batch:
        if not args.quiet:
            print("\n🔄 Batch mode: Converting to both PDF and PPT\n")
        
        # Set format to pdf for first conversion
        if not args.format:
            args.format = 'pdf'
        
        # We'll handle batch conversion by running twice
        # First conversion will happen below, then we'll do second format
    
    # Check and install dependencies if needed
    if not check_and_install_dependencies(args.method, args.format):
        sys.exit(1)
    
    # slides_dir already set above for clean command
    output_dir = (script_dir / args.output_dir).resolve()
    
    # Check if slides directory exists and has files
    if not slides_dir.exists() or not get_html_files(str(slides_dir)):
        handle_missing_slides(slides_dir)
    
    # Get HTML files
    all_html_files = get_html_files(str(slides_dir))
    
    # Handle range selection
    if args.range:
        indices = parse_range(args.range, len(all_html_files))
        if not indices:
            print("No valid slides in specified range")
            sys.exit(1)
        html_files = [all_html_files[i] for i in indices]
        print(f"Selected {len(html_files)} of {len(all_html_files)} slides (range: {args.range})")
    else:
        html_files = all_html_files
        print(f"Found {len(html_files)} HTML slides")
    
    # Handle dry run
    if args.dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - No files will be created")
        print(f"{'='*60}\n")
        print(f"Would convert {len(html_files)} slide(s):")
        for i, file in enumerate(html_files, 1):
            print(f"  {i}. {file.name}")
        print(f"\nOutput format: {args.format.upper()}")
        print(f"Method: {args.method}")
        print(f"Output directory: {output_dir}")
        if args.output:
            print(f"Output filename: {args.output}")
        print(f"\n{'='*60}")
        print("Run without --dry-run to perform actual conversion")
        print(f"{'='*60}\n")
        sys.exit(0)
    
    # Create output directory if it doesn't exist
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: Cannot create output directory {output_dir}: {e}")
        sys.exit(1)
    
    # Prepare output path
    output_path = prepare_output_path(args, output_dir)
    
    # Run conversion
    run_conversion(args, html_files, output_path)
    
    print(f"\n✓ Conversion complete!")
    print(f"Output saved to: {output_path}")
