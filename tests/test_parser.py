"""
Tests for the parser module
"""

import pytest
from parser import ContentParser, LanguageDetector

class TestContentParser:
    
    def test_parse_content_basic(self, sample_content):
        """Test basic content parsing"""
        parser = ContentParser()
        result = parser.parse_content(sample_content, 'http://test.com')
        
        assert result is not None
        assert result['metadata']['title'] == 'Test Page'
        assert result['metadata']['description'] == 'A test page for the search engine'
        assert 'Welcome to Test Page' in result['clean_text']
        assert 'should be removed' not in result['clean_text']  # Script content removed
        assert result['word_count'] > 0
        assert result['url'] == 'http://test.com'
    
    def test_extract_metadata(self, sample_content):
        """Test metadata extraction"""
        parser = ContentParser()
        result = parser.parse_content(sample_content)
        
        metadata = result['metadata']
        assert metadata['title'] == 'Test Page'
        assert metadata['description'] == 'A test page for the search engine'
    
    def test_extract_links(self, sample_content):
        """Test link extraction"""
        parser = ContentParser()
        result = parser.parse_content(sample_content, 'http://test.com')
        
        links = result['links']
        assert len(links) > 0
        assert any(link['url'] == 'http://example.com' for link in links)
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        parser = ContentParser()
        
        dirty_text = "  This   has    multiple   spaces  \n\n and  &amp;  entities  "
        clean_text = parser._clean_text(dirty_text)
        
        assert clean_text == "This has multiple spaces and & entities"

class TestLanguageDetector:
    
    def test_detect_english(self):
        """Test English language detection"""
        detector = LanguageDetector()
        
        english_text = "The quick brown fox jumps over the lazy dog and runs in the park"
        result = detector.detect_language(english_text)
        
        assert result == 'en'
    
    def test_detect_unknown(self):
        """Test unknown language detection"""
        detector = LanguageDetector()
        
        unknown_text = "xyz abc def ghi jkl mno pqr stu vwx"
        result = detector.detect_language(unknown_text)
        
        assert result in ['unknown', 'en']  # Might default to en with low confidence
    
    def test_empty_text(self):
        """Test empty text handling"""
        detector = LanguageDetector()
        
        result = detector.detect_language("")
        assert result == 'unknown'