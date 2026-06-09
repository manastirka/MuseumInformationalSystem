#!/usr/bin/env python3
"""
FastSAM Benchmark for Geological Map Segmentation
Compares FastSAM segmentation vs current geo_zone_processor on OGK map sheets.

Tests on RTX 2060 (6GB VRAM):
  - FastSAM-s (small) and FastSAM-x (large) models
  - Measures VRAM usage, inference time, segment count
  - Outputs visual comparison images
"""

import os
import sys
import time
import json
import logging
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
try:
    import torch
except ImportError:  # pragma: no cover
    import pytest
    pytest.skip('torch is not installed (GPU benchmark script)', allow_module_level=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KARTE_DIR = os.path.join(BASE_DIR, 'Karte', 'Final - Srbija')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'fastsam_test')
GEO_ZONES_DIR = os.path.join(BASE_DIR, 'data', 'geo_zones')

# Test sheets - diverse geological complexity
TEST_SHEETS = ['bor', 'beograd', 'cacak']


def get_gpu_info():
    """Get current GPU memory usage."""
    if not torch.cuda.is_available():
        return {'available': False}
    gpu = torch.cuda.get_device_properties(0)
    allocated = torch.cuda.memory_allocated(0) / 1024**2
    reserved = torch.cuda.memory_reserved(0) / 1024**2
    total = gpu.total_memory / 1024**2
    return {
        'available': True,
        'name': gpu.name,
        'total_mb': round(total),
        'allocated_mb': round(allocated),
        'reserved_mb': round(reserved),
        'free_mb': round(total - reserved),
    }


def load_existing_zones(sheet_name):
    """Load existing geo_zone_processor results for comparison."""
    meta_path = os.path.join(GEO_ZONES_DIR, sheet_name, 'zone_groups_meta.json')
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, 'r') as f:
        return json.load(f)


def run_fastsam_test(image_path, model, sheet_name, model_name, target_size=1024):
    """Run FastSAM on a geological map image and collect metrics."""
    logger.info(f"  [{model_name}] Processing {sheet_name} at {target_size}px...")

    # Clear GPU cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

    gpu_before = get_gpu_info()

    # Run inference
    t_start = time.time()
    results = model(
        image_path,
        imgsz=target_size,
        conf=0.4,
        iou=0.9,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        verbose=False,
    )
    t_inference = time.time() - t_start

    gpu_after = get_gpu_info()
    peak_mb = torch.cuda.max_memory_allocated(0) / 1024**2 if torch.cuda.is_available() else 0

    result = results[0]
    num_segments = len(result.masks) if result.masks is not None else 0

    metrics = {
        'model': model_name,
        'sheet': sheet_name,
        'target_size': target_size,
        'inference_time_s': round(t_inference, 3),
        'num_segments': num_segments,
        'peak_vram_mb': round(peak_mb),
        'vram_allocated_mb': gpu_after.get('allocated_mb', 0),
        'gpu': gpu_before.get('name', 'N/A'),
    }

    logger.info(f"  [{model_name}] {num_segments} segments in {t_inference:.2f}s | Peak VRAM: {peak_mb:.0f}MB")

    # Save segmentation visualization
    save_visualization(result, image_path, sheet_name, model_name, target_size)

    return metrics, result


def save_visualization(result, image_path, sheet_name, model_name, target_size):
    """Save annotated image with segmentation overlay."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Move masks to CPU before plotting to avoid GPU OOM on visualization
    if result.masks is not None and len(result.masks) > 0:
        masks_cpu = result.masks.data.cpu().numpy()  # (N, H, W)
        h, w = masks_cpu.shape[1], masks_cpu.shape[2]

        # Create color-coded zone map (like geo_zone_processor output)
        zone_map = np.zeros((h, w), dtype=np.uint8)
        for i, mask in enumerate(masks_cpu):
            zone_id = (i % 254) + 1
            zone_map[mask > 0.5] = zone_id

        zone_img = Image.fromarray(zone_map)
        zone_path = os.path.join(OUTPUT_DIR, f'{sheet_name}_{model_name}_{target_size}_zones.png')
        zone_img.save(zone_path)
        logger.info(f"  Saved zone map: {zone_path}")

        # Create colorized overlay on original image (CPU-only)
        original = Image.open(image_path).convert('RGB')
        orig_w, orig_h = original.size
        # Resize zone_map to original image size
        zone_resized = np.array(Image.fromarray(zone_map).resize((orig_w, orig_h), Image.NEAREST))
        np.random.seed(42)
        palette = np.random.randint(60, 240, size=(256, 3), dtype=np.uint8)
        palette[0] = [0, 0, 0]
        overlay = palette[zone_resized]
        overlay_img = Image.fromarray(overlay)
        # Blend with original
        blended = Image.blend(original, overlay_img, alpha=0.4)
        out_path = os.path.join(OUTPUT_DIR, f'{sheet_name}_{model_name}_{target_size}.jpg')
        blended.save(out_path, quality=85)
        logger.info(f"  Saved overlay: {out_path}")
    else:
        logger.info(f"  No masks detected for {sheet_name}")


def create_comparison_image(image_path, sheet_name, all_results):
    """Create side-by-side comparison of original, existing zones, and FastSAM results."""
    original = Image.open(image_path).convert('RGB')
    thumb_size = (800, 800)
    original.thumbnail(thumb_size, Image.LANCZOS)
    w, h = original.size

    # Existing zone map
    existing_zone_path = os.path.join(GEO_ZONES_DIR, sheet_name, 'zone_group_map.png')
    panels = [('Original', original)]

    if os.path.exists(existing_zone_path):
        existing = Image.open(existing_zone_path).convert('L')
        existing = existing.resize((w, h), Image.NEAREST)
        # Colorize
        existing_color = colorize_zone_map(existing)
        panels.append(('Current (color-based)', existing_color))

    # FastSAM results
    for model_name, _, result in all_results:
        if result.masks is not None and len(result.masks) > 0:
            masks = result.masks.data.cpu().numpy()
            mh, mw = masks.shape[1], masks.shape[2]
            zone_map = np.zeros((mh, mw), dtype=np.uint8)
            for i, mask in enumerate(masks):
                zone_map[mask > 0.5] = (i % 254) + 1
            zone_img = Image.fromarray(zone_map).resize((w, h), Image.NEAREST)
            zone_color = colorize_zone_map(zone_img)
            panels.append((model_name, zone_color))

    # Compose side by side
    n_panels = len(panels)
    comp_w = w * n_panels + 10 * (n_panels - 1)
    comp_h = h + 40
    comp = Image.new('RGB', (comp_w, comp_h), (255, 255, 255))
    draw = ImageDraw.Draw(comp)

    x_offset = 0
    for label, panel_img in panels:
        comp.paste(panel_img, (x_offset, 30))
        draw.text((x_offset + 10, 5), label, fill=(0, 0, 0))
        x_offset += w + 10

    comp_path = os.path.join(OUTPUT_DIR, f'{sheet_name}_comparison.jpg')
    comp.save(comp_path, quality=90)
    logger.info(f"Comparison saved: {comp_path}")


def colorize_zone_map(zone_img):
    """Convert uint8 zone map to colorized RGB image."""
    arr = np.array(zone_img)
    # Generate random but consistent colors per zone ID
    np.random.seed(42)
    palette = np.random.randint(60, 240, size=(256, 3), dtype=np.uint8)
    palette[0] = [30, 30, 30]  # background

    rgb = palette[arr]
    return Image.fromarray(rgb)


def main():
    logger.info("=" * 70)
    logger.info("FastSAM Geological Map Segmentation Benchmark")
    logger.info("=" * 70)

    # GPU check
    gpu_info = get_gpu_info()
    if gpu_info['available']:
        logger.info(f"GPU: {gpu_info['name']} | Total: {gpu_info['total_mb']}MB | Free: {gpu_info['free_mb']}MB")
    else:
        logger.warning("No CUDA GPU detected! Running on CPU (will be slow).")

    # Import FastSAM
    try:
        from ultralytics import FastSAM
    except ImportError:
        logger.error("ultralytics not installed. Run: pip install ultralytics")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load models
    logger.info("\nDownloading/loading FastSAM-s model...")
    model_s = FastSAM('FastSAM-s.pt')

    all_metrics = []

    for sheet_name in TEST_SHEETS:
        karta_path = os.path.join(KARTE_DIR, sheet_name, f'{sheet_name} - karta.jpg')
        if not os.path.exists(karta_path):
            logger.warning(f"Skipping {sheet_name}: {karta_path} not found")
            continue

        img = Image.open(karta_path)
        logger.info(f"\n{'='*50}")
        logger.info(f"Sheet: {sheet_name} | Image size: {img.size[0]}x{img.size[1]}")
        logger.info(f"{'='*50}")

        # Load existing zone data for comparison
        existing = load_existing_zones(sheet_name)
        if existing:
            n_existing = len(existing.get('groups', existing.get('zone_groups', [])))
            logger.info(f"  Existing geo_zone_processor: {n_existing} zone groups")

        # Test at multiple resolutions
        sheet_results = []
        for target_size in [512, 1024]:
            metrics, result = run_fastsam_test(karta_path, model_s, sheet_name, 'FastSAM-s', target_size)
            all_metrics.append(metrics)
            sheet_results.append(('FastSAM-s @' + str(target_size), metrics, result))

        # Create comparison visualization
        create_comparison_image(karta_path, sheet_name, sheet_results)

    # Now try FastSAM-x if VRAM allows
    logger.info("\n" + "=" * 50)
    logger.info("Testing FastSAM-x (larger model)...")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    try:
        model_x = FastSAM('FastSAM-x.pt')
        # Test on first available sheet only (to save time)
        for sheet_name in TEST_SHEETS[:1]:
            karta_path = os.path.join(KARTE_DIR, sheet_name, f'{sheet_name} - karta.jpg')
            if os.path.exists(karta_path):
                metrics, result = run_fastsam_test(karta_path, model_x, sheet_name, 'FastSAM-x', 1024)
                all_metrics.append(metrics)
        del model_x
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception as e:
        logger.warning(f"FastSAM-x failed (likely OOM): {e}")
        all_metrics.append({'model': 'FastSAM-x', 'error': str(e)})

    # Print summary
    logger.info("\n" + "=" * 70)
    logger.info("BENCHMARK RESULTS SUMMARY")
    logger.info("=" * 70)
    logger.info(f"{'Model':<16} {'Sheet':<12} {'Size':<6} {'Time(s)':<9} {'Segments':<10} {'Peak VRAM':<10}")
    logger.info("-" * 70)
    for m in all_metrics:
        if 'error' in m:
            logger.info(f"{m['model']:<16} {'FAILED':<12} {m.get('error', '')}")
        else:
            logger.info(
                f"{m['model']:<16} {m['sheet']:<12} {m['target_size']:<6} "
                f"{m['inference_time_s']:<9} {m['num_segments']:<10} {m['peak_vram_mb']}MB"
            )

    # Save metrics to JSON
    metrics_path = os.path.join(OUTPUT_DIR, 'benchmark_results.json')
    with open(metrics_path, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    logger.info(f"\nMetrics saved: {metrics_path}")
    logger.info(f"Visualizations saved in: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
