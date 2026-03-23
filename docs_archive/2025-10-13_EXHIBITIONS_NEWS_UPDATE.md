# Exhibitions and News Database Update

## Summary of Changes

Successfully separated **exhibitions** from **news** in the Museum Information System.

## What Was Done

### 1. Data Separation
- **Original data** (`exhibitions.json` with 115 items) → Moved to `news.json`
  - These were actually news articles about museum activities, not exhibitions themselves
  
- **New exhibitions database** (`exhibitions.json` with 20 items) → Created with actual museum exhibitions
  - Includes both permanent and temporary exhibitions
  - Contains real exhibition data with proper fields

### 2. New Module Added: "Музејске вести" (Museum News)
- **Module Key**: `news`
- **Access**: Public (everyone can view)
- **Icon**: `bi-newspaper`
- **Description**: "Вести и објаве о активностима музеја"

### 3. Database Structure

#### Exhibitions Database (`data/exhibitions.json`)
Contains 20 actual museum exhibitions:
- **Permanent Exhibitions** (Стална поставка):
  - Минерали Србије
  - Птице Србије
  - Фосили Србије - Прозори у прошлост
  - Српска флора - Ботаничко благо
  - Инсекти Србије - Мали велики свет
  - Сисари Србије

- **Temporary Exhibitions** (Привремена изложба):
  - Ајкуле - Господари океана (Active)
  - Еволуција - Од молекула до човека
  - Кавијар - Црно злато
  - 6 ногу - Свет инсеката
  - Пази, отровно!
  - Пут на Месец
  - And more...

#### News Database (`data/news.json`)
Contains 115 news articles about:
- Exhibition openings
- Museum events
- Anniversary celebrations
- Visitor programs
- Staff achievements
- Special announcements

### 4. Code Changes

#### app.py
1. Added `news` module to `MODULE_ACCESS` configuration
2. Created `load_news_data()` function
3. Created `NEWS_DATABASE` dictionary with articles
4. Added `/admin/news` route handler

#### New Template
- Created `templates/admin_news.html`:
  - Clean, searchable news feed
  - Card-based layout
  - Date display
  - Curator information
  - Links to original sources
  - Responsive design

### 5. Key Distinctions

| Database | Purpose | Example |
|----------|---------|---------|
| **Exhibitions** (изложба) | Actual museum exhibitions with specimens | "Ајкуле - Господари океана" exhibition with 45 specimens |
| **Exhibits** (експонат) | Physical museum objects/artifacts | "Скелет степског мамута" artifact in permanent collection |
| **News** (вести) | News articles and announcements | "Отварање изложбе 'Пут на Месец'" article about opening event |

## Navigation Access

### Exhibitions Database
- **Route**: `/admin/exhibitions_database`
- **Access**: Admin + draganav@nhmbeo.rs
- **Content**: 20 museum exhibitions (permanent + temporary)

### News
- **Route**: `/admin/news`
- **Access**: Everyone (public)
- **Content**: 115 news articles about museum activities

## Benefits of This Change

1. **Clear Separation**: Exhibitions are now separate from news about exhibitions
2. **Better Organization**: Actual exhibitions with proper metadata (specimens, curators, visitor counts)
3. **Public Access**: News is now accessible to all users
4. **Accurate Data**: Exhibition database contains only real museum exhibitions
5. **Scalability**: Easy to add new exhibitions or news articles

## Files Modified

- `data/exhibitions.json` - Replaced with 20 actual exhibitions
- `data/news.json` - Created with 115 news articles (old exhibitions data)
- `app.py` - Added news module and routes
- `templates/admin_news.html` - Created new news page template

## Testing

```bash
# Verify exhibitions count
python3 -c "import json; print(len(json.load(open('data/exhibitions.json'))))"
# Output: 20

# Verify news count
python3 -c "import json; print(len(json.load(open('data/news.json'))))"  
# Output: 115

# Test the application
python app.py
# Visit: http://localhost:5000/admin/exhibitions_database
# Visit: http://localhost:5000/admin/news
```

## Future Enhancements

1. Add ability to create/edit exhibitions through admin interface
2. Add ability to publish news articles
3. Add filtering by exhibition type (permanent/temporary/touring)
4. Add photo galleries to exhibitions
5. Add RSS feed for news
