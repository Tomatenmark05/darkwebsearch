"""
Configuration settings for Dark Web Search Tool
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/darkweb_search.db')
    SEARCH_INDEX_DB = os.getenv('SEARCH_INDEX_DB', 'data/search_index.db')
    
    # Crawler settings
    CRAWLER_DELAY = float(os.getenv('CRAWLER_DELAY', 1.0))
    CRAWLER_MAX_RETRIES = int(os.getenv('CRAWLER_MAX_RETRIES', 3))
    CRAWLER_TIMEOUT = int(os.getenv('CRAWLER_TIMEOUT', 10))
    
    # Search settings
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', 50))
    SNIPPET_LENGTH = int(os.getenv('SNIPPET_LENGTH', 200))
    
    # Security settings
    ALLOWED_DOMAINS = os.getenv('ALLOWED_DOMAINS', '').split(',')
    ENABLE_RATE_LIMITING = os.getenv('ENABLE_RATE_LIMITING', 'True').lower() == 'true'
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

class DevelopmentConfig(Config):
    """Development environment configuration"""
    FLASK_DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production environment configuration"""
    FLASK_DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    SEARCH_INDEX_DB = ':memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}