"""File handling utilities."""

import os
import glob
from pathlib import Path
from typing import List


def get_html_files(slides_dir: str) -> List[Path]:
    """Get all HTML files from slides directory, sorted numerically."""
    import re
    
    pattern = os.path.join(slides_dir, "*.html")
    files = glob.glob(pattern)
    
    def natural_sort_key(path):
        """Extract numbers from filename for natural sorting."""
        # Extract all numbers from the filename
        numbers = re.findall(r'\d+', os.path.basename(path))
        if numbers:
            # Convert first number to int for proper sorting
            return (int(numbers[0]), path)
        return (float('inf'), path)  # Files without numbers go last
    
    # Sort naturally (page1, page2, ... page9, page10)
    files_sorted = sorted(files, key=natural_sort_key)
    return [Path(f) for f in files_sorted]


def create_template_slide(file_path: Path, slide_number: int):
    """Create a template HTML slide."""
    try:
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide {slide_number}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            color: #101828;
            overflow: hidden;
        }}
        .slide {{
            width: 1280px;
            min-height: 720px;
            position: relative;
            background-color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 50px;
        }}
        .title {{
            font-family: 'Montserrat', sans-serif;
            font-size: 48px;
            font-weight: 700;
            color: #101828;
            margin-bottom: 30px;
            text-align: center;
        }}
        .content {{
            font-size: 24px;
            line-height: 1.6;
            color: #4b5563;
            text-align: center;
            max-width: 900px;
        }}
        .highlight {{
            color: #1D9BF0;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="slide">
        <h1 class="title">Slide {slide_number}</h1>
        <div class="content">
            <p>Edit this HTML file to add your content.</p>
            <p>You can add text, images, and <span class="highlight">custom styling</span>.</p>
        </div>
    </div>
</body>
</html>"""
    
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        print(f"Warning: Failed to create {file_path}: {e}")
        raise
