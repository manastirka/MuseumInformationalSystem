#!/usr/bin/env python3
"""
Create placeholder images for museum specimen databases
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_specimen_placeholder(output_path, width=400, height=400):
    """Create a professional specimen placeholder image."""

    # Create image with light gray background
    img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)

    # Draw border
    border_color = '#dee2e6'
    draw.rectangle([(10, 10), (width-10, height-10)], outline=border_color, width=3)

    # Draw icon (simplified specimen/artifact icon)
    center_x, center_y = width // 2, height // 2

    # Draw a simple museum artifact icon
    icon_color = '#adb5bd'

    # Draw rectangle (like a display case)
    draw.rectangle(
        [(center_x - 80, center_y - 60), (center_x + 80, center_y + 60)],
        outline=icon_color,
        width=4
    )

    # Draw horizontal line (shelf)
    draw.line(
        [(center_x - 80, center_y), (center_x + 80, center_y)],
        fill=icon_color,
        width=4
    )

    # Draw circle (specimen)
    draw.ellipse(
        [(center_x - 30, center_y - 40), (center_x + 30, center_y - 10)],
        fill=icon_color
    )

    # Add text
    try:
        # Try to use a nice font, fall back to default if not available
        font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()

    text = "Нема слике"

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (width - text_width) // 2
    text_y = center_y + 80

    draw.text((text_x, text_y), text, fill='#6c757d', font=font)

    # Save image
    img.save(output_path, 'PNG', optimize=True)
    print(f"Created placeholder: {output_path}")


def create_thumbnail_placeholder(output_path, width=150, height=150):
    """Create a smaller thumbnail placeholder."""

    img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)

    # Draw border
    border_color = '#dee2e6'
    draw.rectangle([(5, 5), (width-5, height-5)], outline=border_color, width=2)

    # Draw simple icon
    center_x, center_y = width // 2, height // 2
    icon_color = '#adb5bd'

    # Simple artifact icon
    draw.rectangle(
        [(center_x - 30, center_y - 25), (center_x + 30, center_y + 25)],
        outline=icon_color,
        width=2
    )

    draw.ellipse(
        [(center_x - 15, center_y - 15), (center_x + 15, center_y - 5)],
        fill=icon_color
    )

    # Save
    img.save(output_path, 'PNG', optimize=True)
    print(f"Created thumbnail placeholder: {output_path}")


if __name__ == '__main__':
    base_path = '/home/aleksandarlukovic/MuseumInfoSystem/static/images'

    # Create main placeholder
    create_specimen_placeholder(os.path.join(base_path, 'specimen-placeholder.png'))

    # Create thumbnail placeholder
    create_thumbnail_placeholder(os.path.join(base_path, 'specimen-placeholder-thumb.png'))

    print("\nPlaceholder images created successfully!")
