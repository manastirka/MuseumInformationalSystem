-- News/Exhibitions Articles Table
-- Phase 3B: News and Events database
-- Migrated from data/news.json (115 articles)

CREATE TABLE IF NOT EXISTS news_articles (
    id SERIAL PRIMARY KEY,
    original_id INTEGER, -- From JSON file
    title TEXT NOT NULL,
    title_en TEXT,
    type TEXT, -- 'Изложба', 'Догађај', etc.
    status TEXT, -- 'Историјска', 'Актуелна', etc.
    category TEXT, -- 'gallery', 'touring', etc.
    start_date DATE,
    end_date DATE,
    location TEXT,
    curator TEXT,
    co_curator TEXT,
    specimens_count INTEGER DEFAULT 0,
    species_count INTEGER DEFAULT 0,
    boxes_count INTEGER DEFAULT 0,
    illustrations_count INTEGER DEFAULT 0,
    visitor_count INTEGER DEFAULT 0,
    description TEXT,
    description_en TEXT,
    target_audience TEXT,
    educational_programs TEXT,
    guided_tours TEXT,
    catalog_available TEXT,
    keywords TEXT,
    source_link TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_news_type ON news_articles(type);
CREATE INDEX IF NOT EXISTS idx_news_status ON news_articles(status);
CREATE INDEX IF NOT EXISTS idx_news_category ON news_articles(category);
CREATE INDEX IF NOT EXISTS idx_news_start_date ON news_articles(start_date);
CREATE INDEX IF NOT EXISTS idx_news_curator ON news_articles(curator);

-- Full-text search index for Serbian Cyrillic content
CREATE INDEX IF NOT EXISTS idx_news_title_search ON news_articles USING gin(to_tsvector('simple', title));
CREATE INDEX IF NOT EXISTS idx_news_description_search ON news_articles USING gin(to_tsvector('simple', description));

COMMENT ON TABLE news_articles IS 'Phase 3B: News and exhibition articles - Migrated from news.json';
