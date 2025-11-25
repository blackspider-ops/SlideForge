"""Command-line interface for SlideForge."""

import sys
import argparse
from pathlib import Path

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
  python converter.py --format pdf
  python converter.py --format ppt
  python converter.py --format pdf --method weasyprint --output my-slides.pdf
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


def run_converter():
    """Main converter logic."""
    args = parse_arguments()
    
    # Check and install dependencies if needed
    if not check_and_install_dependencies(args.method, args.format):
        sys.exit(1)
    
    # Get script directory
    script_dir = Path(__file__).parent
    slides_dir = (script_dir / args.slides_dir).resolve()
    output_dir = (script_dir / args.output_dir).resolve()
    
    # Check if slides directory exists and has files
    if not slides_dir.exists() or not get_html_files(str(slides_dir)):
        handle_missing_slides(slides_dir)
    
    # Get HTML files
    html_files = get_html_files(str(slides_dir))
    print(f"Found {len(html_files)} HTML slides")
    
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
