"""Command-line interface for SlideForge."""

import sys
import argparse
from pathlib import Path

from version import __version__, __author__, __description__
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
  ./slideforge.sh --format pdf              # macOS/Linux
  slideforge.bat --format ppt               # Windows
  ./slideforge.sh --format pdf --method weasyprint --output my-slides.pdf
  ./slideforge.sh --clean                   # Delete all slides (requires confirmation)
        """
    )
    
    parser.add_argument(
        '--format',
        choices=['pdf', 'ppt'],
        required=True,
        help='Output format: pdf or ppt'
    )
    
    parser.add_argument(
        '--method',
        choices=['playwright', 'weasyprint'],
        default='playwright',
        help='Conversion method (default: playwright)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename (default: slides.pdf or slides.pptx)',
        default=None
    )
    
    parser.add_argument(
        '--slides-dir',
        help='Directory containing HTML slides (default: ../slides)',
        default='../slides'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory (default: ../output)',
        default='../output'
    )
    
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Delete all HTML files in slides directory (requires confirmation)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all HTML slides in the slides directory'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be converted without actually converting'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )
    
    parser.add_argument(
        '--range',
        help='Convert only specific slides (e.g., 1-5 or 1,3,5)',
        default=None
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
    
    # Check if output file already exists
    if output_path.exists():
        response = input(f"\nOutput file already exists: {output_path}\nOverwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    return output_path


def run_conversion(args, html_files, output_path: Path):
    """Execute the conversion based on format and method."""
    if args.format == 'pdf':
        if args.method == 'playwright':
            convert_to_pdf_playwright(html_files, str(output_path))
        elif args.method == 'weasyprint':
            convert_to_pdf_weasyprint(html_files, str(output_path))
    else:  # ppt
        if args.method == 'playwright':
            convert_to_ppt_playwright(html_files, str(output_path))
        elif args.method == 'weasyprint':
            convert_to_ppt_weasyprint(html_files, str(output_path))


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


def run_converter():
    """Main converter logic."""
    args = parse_arguments()
    
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
