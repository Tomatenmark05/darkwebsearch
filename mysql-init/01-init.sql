-- Database initialization for Darkwebsearch

USE darkwebsearch;

-- Crawler data table
CREATE TABLE IF NOT EXISTS crawled_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(2048) NOT NULL,
    title TEXT,
    content LONGTEXT,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    INDEX idx_url (url(255)),
    INDEX idx_status (status),
    INDEX idx_crawled_at (crawled_at)
);

-- Analysis results table
CREATE TABLE IF NOT EXISTS analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crawled_data_id INT NOT NULL,
    tags JSON,
    sentiment_score DECIMAL(3,2),
    category VARCHAR(100),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crawled_data_id) REFERENCES crawled_data(id) ON DELETE CASCADE,
    INDEX idx_category (category),
    INDEX idx_analyzed_at (analyzed_at)
);

-- Search queries table (for caching)
CREATE TABLE IF NOT EXISTS search_queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query_text VARCHAR(500) NOT NULL,
    results JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_query (query_text(255)),
    INDEX idx_created_at (created_at)
);

-- Crawler settings table
CREATE TABLE IF NOT EXISTS crawler_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Analysis settings table
CREATE TABLE IF NOT EXISTS analysis_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default settings
INSERT INTO crawler_settings (setting_name, setting_value) VALUES
('rate_limit_delay', '2'),
('max_depth', '3'),
('respect_robots_txt', 'true'),
('user_agent', 'DarkwebSearch-Crawler/1.0')
ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value);

INSERT INTO analysis_settings (setting_name, setting_value) VALUES
('min_content_length', '100'),
('enable_sentiment_analysis', 'true'),
('enable_categorization', 'true'),
('language_detection', 'true')
ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value);