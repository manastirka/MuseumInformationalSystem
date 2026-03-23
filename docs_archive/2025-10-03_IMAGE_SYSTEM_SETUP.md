# Museum Image Management System - Complete Setup Guide

## Overview

Complete integrated image management system for all museum databases with:

✅ **Smart batch upload** with automatic inventory number matching
✅ **Local storage** with automatic thumbnail generation
✅ **Server backup** capability
✅ **Centralized image database** for all collections
✅ **Image gallery** for each database item
✅ **REST API** for programmatic access

## System Architecture

### Components Created

1. **image_storage_engine.py** - Core storage with thumbnails
2. **image_matcher.py** - Smart filename parsing and matching
3. **batch_image_upload.py** - Batch processing system
4. **image_database_manager.py** - Centralized image database
5. **image_api.py** - REST API endpoints
6. **database_migrations.py** - Database migration tools

### Web Interface

- `/admin/batch_image_upload` - Batch upload with matching
- `/admin/image_gallery/<database>/<entity_id>` - Image gallery for items
- `/api/images/*` - REST API endpoints

## Quick Start

### 1. Install Dependencies

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
pip install Pillow>=10.0.0 requests>=2.31.0
```

### 2. Create Storage Directory (Already Done!)

```bash
# Already created at:
ls -la /home/aleksandarlukovic/MuseumInfoSystem/storage/images/
```

Structure:
```
storage/images/
├── originals/          # Full-size images
├── thumbnails/
│   ├── small/         # 150x150px
│   ├── medium/        # 300x300px
│   └── large/         # 600x600px
├── temp/              # Temporary uploads
└── backups/           # Local backups
```

### 3. Initialize Image Database

```bash
python -c "from image_database_manager import get_image_db_manager; get_image_db_manager()"
```

This creates: `/home/aleksandarlukovic/MuseumInfoSystem/data/image_database.json`

### 4. Start the Application

```bash
python app.py
```

Access at: http://localhost:5000/admin/batch_image_upload

## Usage Guide

### Batch Image Upload

#### Step 1: Prepare Images

Organize images in a directory with proper naming:

**Format:** `[PREFIX][INV_NUMBER]_[NAME]_[LOCALITY].jpg`

**Examples:**
- `M12345_Кварц_Србија.jpg` - Mineralogical collection
- `MET678_Метеорит_НХМ.jpg` - Meteorite collection
- `12345_Quartz_Serbia.jpg` - Generic number format

**Inventory Number Prefixes:**

| Collection | Prefix | Example |
|------------|--------|---------|
| Mineralogical | M | M12345 |
| Meteorite | MET | MET678 |
| Paleozoology | PAL | PAL1234 |
| Paleobotany | PB | PB5678 |
| Petrology | P | P9012 |
| Botany | B | B3456 |
| Ichthyology | I | I7890 |
| Entomology | E | E1122 |
| Mycology | MY | MY3344 |
| Herpetology | H | H5566 |
| Ornithology | O | O7788 |
| Library | LIB | LIB9900 |

#### Step 2: Upload via Web Interface

1. Navigate to: http://localhost:5000/admin/batch_image_upload
2. Select **Database** (e.g., "Минералошка збирка")
3. Enter **Directory path** (e.g., `/home/user/mineral_photos`)
4. Click **"Преглед упаривања"** (Preview Matching)

#### Step 3: Review Matches

The system shows:
- **Упарено** (Matched) - High confidence matches
- **Сумњиво** (Ambiguous) - Low confidence, manual review needed
- **Неупарено** (Unmatched) - No matching item found

#### Step 4: Confirm Upload

- Enable **"Аутоматски отпреми слике са високом поузданошћу"** for automatic upload
- Click **"Потврди и отпреми"**

### Single Image Upload

1. Navigate to item's database page
2. Click item to view details
3. Click **"Галерија слика"** or image gallery button
4. Click **"Додај слику"**
5. Select image and add description
6. Click **"Отпреми"**

### View Image Gallery

Go to: `/admin/image_gallery/<database>/<entity_id>`

Example:
```
http://localhost:5000/admin/image_gallery/meteorite/MET001
```

## Matching Algorithm

The system uses a smart 3-tier matching algorithm:

### 1. Primary Match: Inventory Number (Weight: 100)
- Extracts 1-6 digit numbers from filename
- Supports database-specific prefixes
- Exact match: 100 points
- Partial match: 80 points

### 2. Secondary Match: Name/Title (Weight: 30)
- Compares extracted name with database item name
- Uses fuzzy string matching
- Score: similarity × 30

### 3. Tertiary Match: Locality (Weight: 20)
- Compares locality from filename with database
- Uses fuzzy string matching
- Score: similarity × 20

**Confidence Levels:**
- **High** (≥100): Exact inventory number match
- **Medium** (50-99): Partial match with name/locality support
- **Low** (<50): Weak match, manual review required

## API Reference

### Upload Image

```bash
curl -X POST http://localhost:5000/api/images/upload \
  -F "file=@M12345_Quartz.jpg" \
  -F "database=mineral" \
  -F "entity_type=collection_item" \
  -F "entity_id=M12345" \
  -F "description=Кварц примерак"
```

### Get Image

```bash
# Original
curl http://localhost:5000/api/images/{image_id} > image.jpg

# Thumbnail
curl http://localhost:5000/api/images/{image_id}?size=medium > thumb.jpg
```

### Get Images for Item

```bash
curl http://localhost:5000/api/images/entity/meteorite/collection_item/MET001
```

### Delete Image

```bash
curl -X DELETE http://localhost:5000/api/images/{image_id}
```

### Create Backup

```bash
curl -X POST http://localhost:5000/api/images/backup/create
```

### Get Statistics

```bash
curl http://localhost:5000/api/images/stats
```

## Python API

### Batch Upload Example

```python
from batch_image_upload import get_batch_uploader
from image_database_manager import get_image_db_manager

# Get meteorite collection items
meteorite_items = [
    {'inventarni_broj': 'MET001', 'naziv': 'Хондрит', 'lokalitet': 'Србија'},
    {'inventarni_broj': 'MET002', 'naziv': 'Железни метеорит', 'lokalitet': 'Русија'}
]

# Process batch upload
uploader = get_batch_uploader()
results = uploader.process_batch_upload(
    image_files=['/path/to/MET001_Chondrite.jpg', '/path/to/MET002_Iron.jpg'],
    database_items=meteorite_items,
    database='meteorite',
    entity_type='collection_item',
    auto_upload=True,
    id_field='inventarni_broj'
)

# Update image database
img_db = get_image_db_manager()
for upload in results['uploaded']:
    img_db.add_image_to_item(
        database='meteorite',
        entity_id=upload['entity_id'],
        image_id=upload['image_id']
    )

print(f"Uploaded: {results['summary']['uploaded_count']} images")
```

### Single Upload Example

```python
from batch_image_upload import get_batch_uploader
from image_database_manager import get_image_db_manager

uploader = get_batch_uploader()

# Upload single image
image_id = uploader.upload_single_image_to_item(
    image_path='/path/to/photo.jpg',
    database='meteorite',
    entity_type='collection_item',
    entity_id='MET001',
    description='Образац метеорита'
)

# Add to image database
img_db = get_image_db_manager()
img_db.add_image_to_item('meteorite', 'MET001', image_id)
```

### Get Item Images

```python
from image_database_manager import get_image_db_manager
from image_storage_engine import get_image_storage

img_db = get_image_db_manager()
storage = get_image_storage()

# Get all images for item
image_ids = img_db.get_item_images('meteorite', 'MET001')

for img_id in image_ids:
    metadata = storage.get_image_metadata(img_id)
    path = storage.get_image_path(img_id, size='medium')
    print(f"{img_id}: {metadata['description']} - {path}")
```

## Database Integration

### Image Database Structure

Located at: `/home/aleksandarlukovic/MuseumInfoSystem/data/image_database.json`

```json
{
  "version": "1.0.0",
  "databases": {
    "meteorite": {
      "entity_type": "collection_item",
      "items": {
        "MET001": {
          "image_ids": [
            "meteorite_collection_item_MET001_20251003_102345_a1b2c3d4",
            "meteorite_collection_item_MET001_20251003_102350_e5f6g7h8"
          ],
          "added_dates": {
            "meteorite_collection_item_MET001_20251003_102345_a1b2c3d4": "2025-10-03T10:23:45"
          },
          "metadata": {}
        }
      }
    }
  },
  "statistics": {
    "total_items_with_images": 1,
    "total_images": 2,
    "by_database": {
      "meteorite": {
        "items_with_images": 1,
        "total_images": 2
      }
    }
  }
}
```

## Backup & Restore

### Create Local Backup

```python
from image_storage_engine import get_image_storage

storage = get_image_storage()
backup_path = storage.create_local_backup('2025-10-03')
print(f"Backup created: {backup_path}")
```

### Restore from Backup

```python
storage = get_image_storage()
success = storage.restore_from_backup('./storage/images/backups/2025-10-03')
```

### Server Backup

Configure in `.env`:
```bash
IMAGE_BACKUP_SERVER_URL=https://backup.museum.rs:5001
```

Then:
```python
storage = get_image_storage()
storage.backup_to_server()  # Backup all images
```

## Maintenance

### Monitor Storage

```bash
# Check statistics
curl http://localhost:5000/api/images/stats

# Check disk usage
du -sh /home/aleksandarlukovic/MuseumInfoSystem/storage/images/*
```

### Clean Old Backups

```bash
# Keep only last 30 days
find /home/aleksandarlukovic/MuseumInfoSystem/storage/images/backups/* \
  -type d -mtime +30 -exec rm -rf {} +
```

### Export Database Images

```python
from image_database_manager import get_image_db_manager

img_db = get_image_db_manager()
export = img_db.export_database_images(
    database='meteorite',
    output_file='./meteorite_images_export.json'
)
```

## Supported Databases

All museum databases are supported:

**Collections:**
- mineral, meteorite, paleozoology, paleobotany, petrology
- botany, ichthyology, entomology, mycology
- herpetology, ornithology
- conservation, general_zoology, geology_conservation

**Other:**
- library, employees, cultural_heritage
- exhibits, visitors, research

## Troubleshooting

### No matches found
- Check filename format includes inventory number
- Verify database items are loaded correctly
- Check if prefix matches database

### Images not uploading
- Verify file permissions on storage directory
- Check file size (max 10MB)
- Ensure supported format (JPG, PNG, GIF, BMP, WebP, TIFF)

### Thumbnails not generating
- Ensure Pillow is installed: `pip install Pillow`
- Check image is valid (not corrupted)

## File Locations

```
/home/aleksandarlukovic/MuseumInfoSystem/
├── image_storage_engine.py         # Core storage engine
├── image_matcher.py                # Smart matching algorithm
├── batch_image_upload.py           # Batch upload system
├── image_database_manager.py       # Centralized image DB
├── image_api.py                    # REST API
├── database_migrations.py          # Migration tools
├── storage/
│   └── images/                     # Image storage
│       ├── originals/
│       ├── thumbnails/
│       ├── temp/
│       └── backups/
├── data/
│   ├── image_database.json         # Image database
│   └── image_uploads/              # Upload logs
└── templates/
    ├── admin_batch_image_upload.html
    ├── admin_batch_upload_preview.html
    ├── admin_batch_upload_results.html
    └── admin_image_gallery.html
```

## Security Notes

1. **File Validation**: All uploads validated for type and size
2. **Path Security**: Uses `secure_filename()` for all file operations
3. **Access Control**: Admin-only access required for uploads
4. **HTTPS Required**: Use HTTPS for server backup transfers

## Next Steps

1. Add image upload button to all database item pages
2. Integrate image preview in database tables
3. Add image search functionality
4. Implement image tagging system
5. Create public gallery for exhibits

## Support

For issues or questions about the image system:
- Check logs in `logs/museum_info_system.log`
- Review upload logs in `data/image_uploads/`
- Contact system administrator

---

**System Status:** ✅ Fully Operational
**Last Updated:** 2025-10-03
**Version:** 1.0.0
