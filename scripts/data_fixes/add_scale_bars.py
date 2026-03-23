#!/usr/bin/env python3
"""
Add scale bars (razmernik) to mineral specimen photos.
Uses EXIF metadata (focal length, sensor size) and FOV calculation
to determine real-world dimensions in each photo.

Camera distance D is calibrated per camera using the known 35cm postament.
Formula: visible_width_cm = D_mm * effective_sensor_mm / focal_length_mm / 10
         px_per_cm = image_width_px / visible_width_cm
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import os
import sys

BASE = "/home/aleksandarlukovic/Desktop/DokumentacijaNovaZgrada/Stalna postavka/Geologija/Predlozi eksponata zaposlenih u geoloskom odeljenju/Aleksandar"
OUTPUT_DIR = os.path.join(BASE, "Slike sa razmernikom")
POSTAMENT_WIDTH_CM = 35.0

# Camera sensor specs (width x height in mm, native resolution w x h)
CAMERA_SENSORS = {
    'NIKON Z 6_2': {
        'sensor_w_mm': 35.9,
        'sensor_h_mm': 23.9,
        'native_w': 6048,
        'native_h': 4024,
        # Calibrated distance: camera on tripod above postament
        # D chosen so that at 24mm full-frame, postament (35cm) ≈ 50% of visible width
        # visible_width = D * 35.9 / 24 / 10; 35 = 0.50 * visible_width
        # D = 35*10 / (0.50 * 35.9/24) = 350 / 0.748 = 468mm
        'distance_mm': 468,
    },
    'COOLPIX L120': {
        'sensor_w_mm': 6.17,
        'sensor_h_mm': 4.55,
        'native_w': 4320,
        'native_h': 3240,
        # Exhibition photos, handheld, further from specimen
        # At 7.3mm FL, specimen ~35cm fills ~55% of frame
        # visible_width = D * 6.17 / 7.3 / 10; 35 = 0.55 * visible_width
        # D = 350 / (0.55 * 6.17/7.3) = 350 / 0.465 = 753mm
        'distance_mm': 753,
    },
}


def get_exif_data(pil_img):
    """Extract relevant EXIF fields from a PIL image."""
    exif = pil_img._getexif()
    if not exif:
        return {}

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'FocalLength':
            data['focal_length'] = float(value)
        elif tag == 'Make':
            data['make'] = str(value).strip()
        elif tag == 'Model':
            data['model'] = str(value).strip()
        elif tag == 'FocalLengthIn35mmFilm':
            data['focal_length_35mm'] = int(value)
    return data


def compute_scale_fov(img_width, img_height, focal_length_mm, camera_model):
    """Compute px_per_cm using FOV calculation from EXIF metadata.

    Uses: visible_width_cm = D * effective_sensor_w / focal_length / 10
          px_per_cm = image_width / visible_width_cm

    The effective sensor width accounts for in-camera or post-processing crops.
    """
    sensor = CAMERA_SENSORS.get(camera_model)
    if not sensor:
        return None, f"unknown camera: {camera_model}"

    # Effective sensor width accounts for crop (image may be smaller than native)
    crop_ratio_w = img_width / sensor['native_w']
    crop_ratio_h = img_height / sensor['native_h']
    # Use the larger ratio to handle asymmetric crops correctly
    crop_ratio = max(crop_ratio_w, crop_ratio_h)
    # But cap at 1.0 (can't exceed native sensor)
    crop_ratio = min(crop_ratio, 1.0)

    effective_sensor_w = sensor['sensor_w_mm'] * crop_ratio
    D = sensor['distance_mm']

    # Visible width in the image plane
    visible_width_mm = D * effective_sensor_w / focal_length_mm
    visible_width_cm = visible_width_mm / 10.0

    px_per_cm = img_width / visible_width_cm

    debug = (f"FL={focal_length_mm}mm crop={crop_ratio:.3f} "
             f"eff_sensor={effective_sensor_w:.1f}mm "
             f"visible={visible_width_cm:.1f}cm "
             f"D={D}mm")
    return px_per_cm, debug


def draw_scale_bar(img, px_per_cm, position='bottom_right'):
    """Draw a professional scale bar on the image."""
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Pick a nice round cm value for the bar (target ~18% of image width)
    target_px = w * 0.18
    target_cm = target_px / px_per_cm

    nice_values = [1, 2, 3, 5, 10, 15, 20, 25, 30]
    bar_cm = min(nice_values, key=lambda v: abs(v - target_cm))
    bar_px = int(bar_cm * px_per_cm)

    # Ensure bar isn't too big or too small
    if bar_px > w * 0.4:
        bar_cm = max(1, int(target_cm))
        bar_px = int(bar_cm * px_per_cm)
    if bar_px < w * 0.05:
        bar_cm = nice_values[-1]
        bar_px = int(bar_cm * px_per_cm)

    bar_height = max(8, int(h * 0.007))
    margin = int(w * 0.03)

    if position == 'bottom_right':
        bar_x = w - margin - bar_px
        bar_y = h - margin - bar_height - 30
    elif position == 'bottom_left':
        bar_x = margin
        bar_y = h - margin - bar_height - 30
    else:
        bar_x = (w - bar_px) // 2
        bar_y = h - margin - bar_height - 30

    # Background for contrast
    pad = 12
    bg_rect = [bar_x - pad, bar_y - pad - 5,
               bar_x + bar_px + pad, bar_y + bar_height + 28 + pad]
    draw.rectangle(bg_rect, fill=(0, 0, 0, 180))

    # Alternating segments
    num_segments = bar_cm if bar_cm <= 10 else max(2, bar_cm // 5)
    seg_px = bar_px / num_segments
    for i in range(num_segments):
        color = 'white' if i % 2 == 0 else (180, 180, 180)
        x1 = bar_x + int(i * seg_px)
        x2 = bar_x + int((i + 1) * seg_px)
        draw.rectangle([x1, bar_y, x2, bar_y + bar_height], fill=color)

    # Outline and ticks
    draw.rectangle([bar_x, bar_y, bar_x + bar_px, bar_y + bar_height],
                   outline='white', width=1)
    tick_h = bar_height + 6
    draw.line([(bar_x, bar_y - 3), (bar_x, bar_y + tick_h)],
              fill='white', width=2)
    draw.line([(bar_x + bar_px, bar_y - 3), (bar_x + bar_px, bar_y + tick_h)],
              fill='white', width=2)

    # Label
    label = f"{bar_cm} cm"
    try:
        font_size = max(16, int(h * 0.018))
        font = ImageFont.truetype(
            "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), label, font=font)
    text_w = bbox[2] - bbox[0]
    text_x = bar_x + (bar_px - text_w) // 2
    text_y = bar_y + bar_height + 4

    # Text with outline
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx or dy:
                draw.text((text_x + dx, text_y + dy), label,
                          fill='black', font=font)
    draw.text((text_x, text_y), label, fill='white', font=font)

    return img


def process_images():
    """Process all images using EXIF + FOV scale calculation."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    folders = [
        "Ostale slike za stalnu postavku",
        "Ostale fotke za stalnu",
        "Nove slike Trepca/JPG",
        "Nove slike Trepca/Trepca sa izlozbe",
    ]

    processed = 0
    errors = 0
    no_exif = 0

    for folder_name in folders:
        folder_path = os.path.join(BASE, folder_name)
        if not os.path.exists(folder_path):
            print(f"SKIP: {folder_name} not found")
            continue

        print(f"\n{'='*70}")
        print(f"Processing: {folder_name}")
        print(f"{'='*70}")

        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs
                       if d not in ('SlikeSkalirane', 'Slike sa razmernikom')]

            for filename in sorted(files):
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue

                filepath = os.path.join(root, filename)

                try:
                    pil_img = Image.open(filepath)
                    w, h = pil_img.size

                    # Get EXIF
                    exif = get_exif_data(pil_img)
                    fl = exif.get('focal_length')
                    model = exif.get('model', '')

                    if not fl or not model:
                        print(f"  SKIP {filename[:50]:50s} no EXIF focal_length/model")
                        no_exif += 1
                        continue

                    # Compute scale using FOV
                    px_per_cm, debug = compute_scale_fov(w, h, fl, model)

                    if px_per_cm is None:
                        print(f"  SKIP {filename[:50]:50s} {debug}")
                        no_exif += 1
                        continue

                    # Create output
                    out_img = pil_img.copy()
                    if out_img.mode != 'RGB':
                        out_img = out_img.convert('RGB')

                    out_img = draw_scale_bar(out_img, px_per_cm)

                    # Preserve folder structure in output
                    rel_path = os.path.relpath(root, BASE)
                    out_dir = os.path.join(OUTPUT_DIR, rel_path)
                    os.makedirs(out_dir, exist_ok=True)

                    out_path = os.path.join(out_dir, filename)
                    out_img.save(out_path, quality=95, subsampling=0)

                    short = filename[:50]
                    print(f"  OK  {short:50s} {w}x{h} "
                          f"scale={px_per_cm:.1f}px/cm [{debug}]")
                    processed += 1

                except Exception as e:
                    print(f"  ERR {filename[:50]:50s} {e}")
                    errors += 1

    print(f"\n{'='*70}")
    print(f"Done! Processed: {processed}, Errors: {errors}, No EXIF: {no_exif}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == '__main__':
    process_images()
