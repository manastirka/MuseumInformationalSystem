# Museum Image Storage System

Complete guide for the universal image storage engine with local storage and server backup capability.

## Overview

The image storage system provides:
- **Local file storage** with organized directory structure
- **Automatic thumbnail generation** (small, medium, large)
- **Metadata management** with JSON database
- **Server backup capability** via REST API
- **Support for all museum databases** (collections, library, employees, etc.)
- **Image validation** and deduplication

## Architecture

### Components

1. **`image_storage_engine.py`** - Core storage engine
   - File management (upload, delete, retrieve)
   - Thumbnail generation (3 sizes)
   - Metadata tracking
   - Backup/restore functionality

2. **`image_api.py`** - Flask REST API
   - HTTP endpoints for image operations
   - Server-to-server backup
   - Storage statistics

3. **`database_migrations.py`** - Database migration tools
   - SQL migration generator
   - JSON schema updates
   - Automatic field addition

### Directory Structure

```
storage/
└── images/
    ├── originals/          # Original uploaded images
    ├── thumbnails/
    │   ├── small/          # 150x150px thumbnails
    │   ├── medium/         # 300x300px thumbnails
    │   └── large/          # 600x600px thumbnails
    ├── temp/               # Temporary upload storage
    ├── backups/            # Local backups
    └── metadata.json       # Image metadata database
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `Pillow>=10.0.0` - Image processing
- `requests>=2.31.0` - Server backup

### 2. Configure Environment

Add to `.env`:

```bash
# Image storage path (optional, default: ./storage/images)
IMAGE_STORAGE_PATH=./storage/images

# Server backup URL (optional)
IMAGE_BACKUP_SERVER_URL=https://backup.museum.rs
```

### 3. Run Database Migrations

For SQL databases:
```bash
python database_migrations.py --generate-sql --output ./data/migrations
# Review the generated SQL file, then execute it
mysql -u username -p database_name < ./data/migrations/add_image_support.sql
```

For JSON databases:
```bash
python database_migrations.py --apply-json --data-dir ./data
```

## Usage

### Python API

#### Initialize Storage Engine

```python
from image_storage_engine import get_image_storage

# Get singleton instance
storage = get_image_storage(
    base_path='./storage/images',
    server_url='https://backup.museum.rs'
)
```

#### Upload Image

```python
image_id = storage.store_image(
    file_path='/path/to/image.jpg',
    database='mineral',                    # Database name
    entity_type='collection_item',         # Entity type
    entity_id='MIN_12345',                 # Entity ID
    description='Образац кварца',          # Optional description
    metadata={                             # Optional custom metadata
        'photographer': 'Иван Петровић',
        'date_taken': '2025-10-01',
        'location': 'Терен Рудник'
    }
)

print(f"Image stored with ID: {image_id}")
# Output: mineral_collection_item_MIN_12345_20251003_093045_a1b2c3d4
```

#### Retrieve Image

```python
# Get original
original_path = storage.get_image_path(image_id, size='original')

# Get thumbnail
thumbnail_path = storage.get_image_path(image_id, size='medium')

# Get metadata
metadata = storage.get_image_metadata(image_id)
print(metadata)
# Output:
# {
#   'database': 'mineral',
#   'entity_type': 'collection_item',
#   'entity_id': 'MIN_12345',
#   'original_filename': 'quartz_specimen.jpg',
#   'description': 'Образац кварца',
#   'upload_date': '2025-10-03T09:30:45',
#   'file_size': 2458624,
#   'backed_up': False
# }
```

#### Get All Images for Entity

```python
images = storage.get_images_for_entity(
    database='mineral',
    entity_type='collection_item',
    entity_id='MIN_12345'
)

for img in images:
    print(f"{img['image_id']}: {img['description']}")
```

#### Delete Image

```python
success = storage.delete_image(image_id)
if success:
    print("Image deleted successfully")
```

#### Backup Operations

```python
# Create local backup
backup_path = storage.create_local_backup(backup_name='2025-10-03')
print(f"Backup created: {backup_path}")

# Restore from backup
storage.restore_from_backup('./storage/images/backups/2025-10-03')

# Backup to server (single image)
storage.backup_to_server(image_id)

# Backup all images to server
storage.backup_to_server()
```

#### Storage Statistics

```python
stats = storage.get_storage_stats()
print(stats)
# Output:
# {
#   'total_images': 1247,
#   'total_size_mb': 2847.35,
#   'backed_up_count': 1100,
#   'storage_path': '/home/museum/storage/images',
#   'databases': ['mineral', 'library', 'employees', 'botany']
# }
```

### REST API

#### Upload Image

```bash
curl -X POST http://localhost:5000/api/images/upload \
  -F "file=@specimen.jpg" \
  -F "database=mineral" \
  -F "entity_type=collection_item" \
  -F "entity_id=MIN_12345" \
  -F "description=Образац кварца"
```

Response:
```json
{
  "success": true,
  "image_id": "mineral_collection_item_MIN_12345_20251003_093045_a1b2c3d4",
  "message": "Image uploaded successfully"
}
```

#### Get Image

```bash
# Original
curl http://localhost:5000/api/images/{image_id} > image.jpg

# Thumbnail
curl http://localhost:5000/api/images/{image_id}?size=medium > thumb.jpg
```

#### Get Image Metadata

```bash
curl http://localhost:5000/api/images/{image_id}/metadata
```

#### Get Images for Entity

```bash
curl http://localhost:5000/api/images/entity/mineral/collection_item/MIN_12345
```

Response:
```json
{
  "success": true,
  "count": 3,
  "images": [
    {
      "image_id": "mineral_collection_item_MIN_12345_20251003_093045_a1b2c3d4",
      "description": "Образац кварца",
      "upload_date": "2025-10-03T09:30:45"
    }
  ]
}
```

#### Delete Image

```bash
curl -X DELETE http://localhost:5000/api/images/{image_id}
```

#### Create Backup

```bash
# Local backup
curl -X POST http://localhost:5000/api/images/backup/create \
  -H "Content-Type: application/json" \
  -d '{"backup_name": "2025-10-03"}'

# Server backup
curl -X POST http://localhost:5000/api/images/backup/server
```

#### Storage Statistics

```bash
curl http://localhost:5000/api/images/stats
```

### Database Integration

#### SQL Databases

After running migrations, each table has an `image_ids` field:

```sql
SELECT image_ids FROM meteorite_collection WHERE id = 123;
-- Returns: ["mineral_collection_item_MIN_12345_20251003_093045_a1b2c3d4"]
```

Update image IDs:
```sql
UPDATE meteorite_collection
SET image_ids = '["img_id_1", "img_id_2", "img_id_3"]'
WHERE id = 123;
```

#### JSON Databases

After running migrations, each record has an `image_ids` field:

```json
{
  "id": "BOOK_001",
  "title": "Минералогија Србије",
  "author": "Др Петар Петровић",
  "image_ids": [
    "library_book_BOOK_001_20251003_093045_a1b2c3d4",
    "library_book_BOOK_001_20251003_093050_e5f6g7h8"
  ]
}
```

## Database Support

The system supports all museum databases:

### Collections
- Botany Collection (`botany`)
- Ichthyology Collection (`ichthyology`)
- Entomology Collection (`entomology`)
- Mycology Collection (`mycology`)
- Herpetology Collection (`herpetology`)
- Ornithology Collection (`ornithology`)
- Paleozoology Collection (`paleozoology`)
- Paleobotany Collection (`paleobotany`)
- Petrology Collection (`petrology`)
- Meteorite Collection (`meteorite`)
- Conservation Biology (`conservation`)
- General Zoology (`general_zoology`)
- Geology Conservation (`geology_conservation`)

### Other Databases
- Library Database (`library`)
- Employee Profiles (`employees`)
- Cultural Heritage (`cultural_heritage`)
- Exhibits (`exhibits`)
- Visitor Records (`visitors`)
- Research Projects (`research`)

## Image Specifications

### Supported Formats
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- BMP (`.bmp`)
- WebP (`.webp`)
- TIFF (`.tiff`)

### Size Limits
- Maximum file size: **10MB**
- Recommended resolution: **1920x1080** or higher

### Thumbnail Sizes
- **Small**: 150x150px (for lists, previews)
- **Medium**: 300x300px (for cards, galleries)
- **Large**: 600x600px (for detailed views)

## Server Backup Setup

### Backup Server Configuration

Deploy the backup receiver on your backup server:

```python
from flask import Flask
from image_api import init_image_api

app = Flask(__name__)

# Initialize with backup storage path
init_image_api(
    app,
    storage_path='/backup/museum-images',
    server_url=None  # This is the backup server
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

### Client Configuration

Configure clients to backup to the server:

```python
storage = get_image_storage(
    base_path='./storage/images',
    server_url='https://backup-server.museum.rs:5001'
)

# Backup will now be sent to the server
storage.backup_to_server()
```

## Maintenance

### Create Regular Backups

```bash
# Create daily backup
python -c "
from image_storage_engine import get_image_storage
from datetime import datetime

storage = get_image_storage()
backup_name = datetime.now().strftime('%Y-%m-%d')
storage.create_local_backup(backup_name)
"
```

### Monitor Storage

```bash
# Get statistics
curl http://localhost:5000/api/images/stats

# Check disk usage
du -sh ./storage/images/*
```

### Clean Old Backups

```bash
# Keep only last 30 days
find ./storage/images/backups/* -type d -mtime +30 -exec rm -rf {} +
```

## Security Considerations

1. **File Validation**: All uploads are validated for type and size
2. **Hash Verification**: SHA256 hashing prevents duplicates
3. **Path Security**: All file paths use `secure_filename()`
4. **Access Control**: Integrate with existing authentication system
5. **HTTPS Required**: Use HTTPS for server backup transfers

## Troubleshooting

### Issue: "Invalid image file"
- Check file format is supported
- Verify file is not corrupted
- Ensure file size is under 10MB

### Issue: "Server backup failed"
- Check `IMAGE_BACKUP_SERVER_URL` is correct
- Verify backup server is running
- Check network connectivity

### Issue: "Thumbnail generation failed"
- Install Pillow: `pip install Pillow`
- Check original image is valid
- Verify disk space available

## Examples

### Example 1: Upload Employee Photo

```python
from image_storage_engine import get_image_storage

storage = get_image_storage()

image_id = storage.store_image(
    file_path='/tmp/employee_photo.jpg',
    database='employees',
    entity_type='employee',
    entity_id='verica.stojanovic@nhmbeo.rs',
    description='Службена фотографија',
    metadata={'year': 2025}
)

# Update employee record with image ID
# (In your database: UPDATE employees SET image_ids = '["..."]')
```

### Example 2: Create Museum Collection Gallery

```python
from image_storage_engine import get_image_storage

storage = get_image_storage()

# Get all images for a meteorite
images = storage.get_images_for_entity(
    database='mineral',
    entity_type='meteorite',
    entity_id='METEOR_001'
)

# Display gallery
for img in images:
    thumb_path = storage.get_image_path(img['image_id'], size='medium')
    print(f"Display: {thumb_path} - {img['description']}")
```

### Example 3: Batch Upload

```python
import os
from image_storage_engine import get_image_storage

storage = get_image_storage()
image_dir = '/path/to/collection_photos'

for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        # Extract ID from filename (e.g., MIN_12345.jpg)
        item_id = filename.replace('.jpg', '')

        image_id = storage.store_image(
            file_path=os.path.join(image_dir, filename),
            database='mineral',
            entity_type='collection_item',
            entity_id=item_id,
            description=f'Фотографија примерка {item_id}'
        )
        print(f"Uploaded: {filename} -> {image_id}")
```

## API Reference

See inline documentation in:
- `image_storage_engine.py` - Core API
- `image_api.py` - REST endpoints
- `database_migrations.py` - Migration tools

## Support

For issues or questions, contact the museum IT department.
