#!/usr/bin/env python3
"""
Creates a professional museum control center icon
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_museum_icon(output_path, size=256):
    """Create a museum control center icon"""
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Color scheme - museum/professional theme
    primary_color = (41, 128, 185)  # Professional blue
    secondary_color = (52, 73, 94)   # Dark slate
    accent_color = (231, 76, 60)     # Red accent
    white = (255, 255, 255)
    
    # Padding
    padding = size // 8
    
    # Draw background circle with gradient effect
    circle_center = size // 2
    circle_radius = (size - padding * 2) // 2
    
    # Outer glow
    for i in range(5, 0, -1):
        alpha = 30 * i
        draw.ellipse(
            [padding - i*2, padding - i*2, 
             size - padding + i*2, size - padding + i*2],
            fill=(*primary_color, alpha)
        )
    
    # Main circle
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=primary_color,
        outline=secondary_color,
        width=size//32
    )
    
    # Draw museum building icon (simplified Greek temple style)
    building_width = size // 2
    building_height = size // 3
    building_x = (size - building_width) // 2
    building_y = (size - building_height) // 2
    
    # Roof/pediment (triangle)
    roof_height = building_height // 3
    roof_points = [
        (building_x - building_width//6, building_y + roof_height),  # Left
        (size // 2, building_y),  # Top center
        (building_x + building_width + building_width//6, building_y + roof_height)  # Right
    ]
    draw.polygon(roof_points, fill=white, outline=secondary_color, width=2)
    
    # Columns (3 columns)
    column_width = building_width // 12
    column_height = building_height - roof_height
    column_spacing = building_width // 4
    
    for i in range(3):
        col_x = building_x + i * column_spacing
        # Column
        draw.rectangle(
            [col_x, building_y + roof_height, 
             col_x + column_width, building_y + roof_height + column_height],
            fill=white,
            outline=secondary_color,
            width=1
        )
    
    # Base
    base_height = size // 20
    draw.rectangle(
        [building_x - building_width//8, building_y + building_height - base_height//2,
         building_x + building_width + building_width//8, building_y + building_height + base_height//2],
        fill=white,
        outline=secondary_color,
        width=2
    )
    
    # Add control/settings gear icon in corner
    gear_size = size // 5
    gear_x = size - padding - gear_size + size//16
    gear_y = size - padding - gear_size + size//16
    
    # Draw simplified gear
    gear_center_x = gear_x + gear_size // 2
    gear_center_y = gear_y + gear_size // 2
    gear_outer = gear_size // 2
    gear_inner = gear_size // 4
    
    # Gear teeth (8 teeth)
    import math
    num_teeth = 8
    for i in range(num_teeth):
        angle1 = (i * 2 * math.pi / num_teeth) - math.pi/16
        angle2 = (i * 2 * math.pi / num_teeth) + math.pi/16
        
        points = [
            (gear_center_x + gear_inner * math.cos(angle1),
             gear_center_y + gear_inner * math.sin(angle1)),
            (gear_center_x + gear_outer * math.cos(angle1),
             gear_center_y + gear_outer * math.sin(angle1)),
            (gear_center_x + gear_outer * math.cos(angle2),
             gear_center_y + gear_outer * math.sin(angle2)),
            (gear_center_x + gear_inner * math.cos(angle2),
             gear_center_y + gear_inner * math.sin(angle2))
        ]
        draw.polygon(points, fill=accent_color, outline=secondary_color, width=1)
    
    # Gear center hole
    draw.ellipse(
        [gear_center_x - gear_inner//2, gear_center_y - gear_inner//2,
         gear_center_x + gear_inner//2, gear_center_y + gear_inner//2],
        fill=primary_color,
        outline=secondary_color,
        width=1
    )
    
    return img

def main():
    """Generate icons in multiple sizes"""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create multiple sizes for different uses
    sizes = {
        'icon_256.png': 256,  # Desktop icon
        'icon_128.png': 128,  # Toolbar
        'icon_64.png': 64,    # Small icon
        'icon_48.png': 48,    # Taskbar
    }
    
    for filename, size in sizes.items():
        output_path = os.path.join(output_dir, filename)
        icon = create_museum_icon(output_path, size)
        icon.save(output_path, 'PNG')
        print(f"✅ Created {filename} ({size}x{size})")
    
    # Create .ico file for Windows compatibility (contains multiple sizes)
    ico_path = os.path.join(output_dir, 'museum_control.ico')
    icon_256 = Image.open(os.path.join(output_dir, 'icon_256.png'))
    icon_128 = Image.open(os.path.join(output_dir, 'icon_128.png'))
    icon_64 = Image.open(os.path.join(output_dir, 'icon_64.png'))
    icon_48 = Image.open(os.path.join(output_dir, 'icon_48.png'))
    
    icon_256.save(
        ico_path,
        format='ICO',
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48)]
    )
    print(f"✅ Created museum_control.ico (multi-size)")
    
    print(f"\n🎨 Museum Control Center icons created successfully!")
    print(f"📁 Location: {output_dir}")

if __name__ == '__main__':
    main()
