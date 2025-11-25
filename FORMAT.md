# HTML Slide Format Guidelines

This document provides guidelines for creating HTML slides that convert properly to PDF and PowerPoint formats.

## Recommended Slide Dimensions

- **Width:** 1280px
- **Height:** 720px (16:9 aspect ratio)
- **Important:** Keep total content height at or below 720px to avoid multi-page PDFs

## HTML Structure

### Basic Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Slide Title</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Inter', sans-serif;
            overflow: hidden;
        }
        .slide {
            width: 1280px;
            height: 720px;  /* Use height, not min-height */
            position: relative;
            background-color: #ffffff;
        }
    </style>
</head>
<body>
    <div class="slide">
        <!-- Your content here -->
    </div>
</body>
</html>
```

## CSS Best Practices

### 1. Use Fixed Height, Not Min-Height

❌ **Don't:**
```css
.slide {
    min-height: 720px;  /* Allows content to overflow */
}
```

✅ **Do:**
```css
.slide {
    height: 720px;  /* Enforces exact height */
    overflow: hidden;  /* Prevents overflow */
}
```

### 2. Recommended Padding Values

For slides to fit within 720px:

```css
.header {
    padding: 35px 70px 20px;  /* Top, sides, bottom */
}

.content {
    padding: 0 70px 25px;  /* No top padding, moderate bottom */
}

.footer {
    padding: 15px 70px;  /* Minimal padding */
}
```

### 3. Font Size Guidelines

| Element | Recommended Size | Max Size |
|---------|-----------------|----------|
| Main Title | 36-40px | 44px |
| Section Headers | 22-24px | 28px |
| Body Text | 16-18px | 20px |
| Small Text/Captions | 14-16px | 18px |

### 4. Spacing Guidelines

```css
/* Margins between elements */
.section {
    margin-bottom: 20-25px;  /* Between major sections */
}

.item {
    margin-bottom: 12-15px;  /* Between list items */
}

/* Gaps in flexbox/grid */
.container {
    gap: 15-20px;  /* Between columns/items */
}
```

## Common Issues and Fixes

### Issue 1: Content Cut Off at Bottom

**Symptom:** Footer or bottom content doesn't appear in PDF

**Causes:**
- Total content height exceeds 720px
- Too much padding/margins
- Font sizes too large

**Solutions:**

1. **Reduce header padding:**
```css
.header {
    padding: 35px 70px 20px;  /* Instead of 50px 70px 30px */
}
```

2. **Reduce content padding:**
```css
.content {
    padding: 0 70px 25px;  /* Instead of 0 70px 50px */
}
```

3. **Reduce font sizes:**
```css
.title {
    font-size: 36px;  /* Instead of 40px */
}
.body-text {
    font-size: 16px;  /* Instead of 20px */
}
```

4. **Reduce spacing between items:**
```css
.item {
    margin-bottom: 12px;  /* Instead of 20px */
}
```

### Issue 2: Content Spans Multiple Pages

**Symptom:** One HTML slide creates 2+ PDF pages

**Solution:** Apply all fixes from Issue 1, plus:

```css
.slide {
    height: 720px;  /* Change from min-height */
    max-height: 720px;
    overflow: hidden;
}
```

### Issue 3: Text Too Small After Fixes

**Symptom:** Content fits but is hard to read

**Solution:** Reduce content amount instead of font size. Consider:
- Splitting into multiple slides
- Using bullet points instead of paragraphs
- Removing less important information

## Testing Your Slides

### Quick Test

```bash
# Test a single slide
./slideforge.sh pdf --range 1

# Test specific problematic slides
./slideforge.sh pdf --range 5,7,9
```

### Check for Issues

1. **Open the PDF** - Each HTML file should be exactly 1 page
2. **Check bottom content** - Footer should be fully visible
3. **Check text size** - Should be readable at normal zoom
4. **Check layout** - No weird spacing or overlaps

## Troubleshooting Checklist

When a slide doesn't convert properly:

- [ ] Is `.slide` using `height: 720px` (not `min-height`)?
- [ ] Is header padding ≤ 35px top?
- [ ] Is content bottom padding ≤ 30px?
- [ ] Are font sizes within recommended ranges?
- [ ] Are margins between items ≤ 20px?
- [ ] Is total vertical space used < 720px?

## Advanced: Calculating Total Height

To ensure your slide fits:

```
Total Height = 
  Header padding-top (35px)
  + Title height (~50px with 40px font)
  + Header padding-bottom (20px)
  + Content items (varies)
  + Content padding-bottom (25px)
  + Footer height (~50px)
  
Should be ≤ 720px
```

## External Resources

### Recommended Fonts

Google Fonts work well:
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
```

### Icons

Material Icons are supported:
```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

## Examples

See the `slides/` directory for working examples of properly formatted slides.

## Need Help?

If your slides still don't convert properly after following these guidelines:

1. Check the PDF output to identify which slides have issues
2. Use `--range` flag to test specific slides
3. Gradually reduce padding/font sizes until content fits
4. Consider splitting complex slides into multiple simpler slides
