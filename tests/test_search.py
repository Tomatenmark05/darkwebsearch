"""
Tests for the search module
"""

import pytest
import tempfile
import os
from search import SimpleSearchEngine

class TestSimpleSearchEngine:
    
    def test_setup_database(self, temp_db):
        """Test database setup"""
        engine = SimpleSearchEngine(temp_db)
        
        # Check if database file exists and tables are created
        assert os.path.exists(temp_db)
    
    def test_index_document(self, temp_db):
        """Test document indexing"""
        engine = SimpleSearchEngine(temp_db)
        
        # Index a test document
        engine.index_document(
            url="http://test.com/page1",
            title="Test Page",
            content="This is a test document with some important content about search engines."
        )
        
        # Verify document was indexed by searching
        results = engine.search("test document")
        assert len(results) > 0
        assert results[0]['url'] == "http://test.com/page1"
    
    def test_search_functionality(self, temp_db):
        """Test search functionality"""
        engine = SimpleSearchEngine(temp_db)
        
        # Index multiple documents
        documents = [
            {
                'url': 'http://test.com/page1',
                'title': 'Python Programming',
                'content': 'Python is a powerful programming language used for web development.'
            },
            {
                'url': 'http://test.com/page2', 
                'title': 'Web Development',
                'content': 'Web development involves creating websites and web applications.'
            },
            {
                'url': 'http://test.com/page3',
                'title': 'Search Engines',
                'content': 'Search engines help users find relevant information quickly.'
            }
        ]
        
        for doc in documents:
            engine.index_document(doc['url'], doc['title'], doc['content'])
        
        # Test search queries
        results = engine.search("python programming")
        assert len(results) > 0
        assert "Python Programming" in [r['title'] for r in results]
        
        results = engine.search("web development")
        assert len(results) > 0
        assert any("web" in r['title'].lower() for r in results)
        
        results = engine.search("search engines")
        assert len(results) > 0
        assert any("search" in r['title'].lower() for r in results)
    
    def test_tokenize(self, temp_db):
        """Test text tokenization"""
        engine = SimpleSearchEngine(temp_db)
        
        text = "This is a TEST with Special-Characters and numbers123!"
        tokens = engine._tokenize(text)
        
        assert "test" in tokens
        assert "special" in tokens
        assert "characters" in tokens
        assert "numbers" in tokens
        assert "the" not in tokens  # Stop word should be removed
        assert len([t for t in tokens if len(t) < 3]) == 0  # No short tokens
    
    def test_calculate_term_frequencies(self, temp_db):
        """Test term frequency calculation"""
        engine = SimpleSearchEngine(temp_db)
        
        tokens = ["test", "document", "test", "search", "test"]
        frequencies = engine._calculate_term_frequencies(tokens)
        
        assert frequencies["test"] == 3
        assert frequencies["document"] == 1
        assert frequencies["search"] == 1
    
    def test_generate_snippet(self, temp_db):
        """Test snippet generation"""
        engine = SimpleSearchEngine(temp_db)
        
        content = "This is a long document with many words. The important keyword appears here in the middle of the text. There is more content after the keyword to test snippet generation."
        query_terms = ["keyword"]
        
        snippet = engine._generate_snippet(content, query_terms, max_length=50)
        
        assert "keyword" in snippet
        assert len(snippet) <= 60  # Account for ellipsis
    
    def test_empty_search(self, temp_db):
        """Test search with empty database"""
        engine = SimpleSearchEngine(temp_db)
        
        results = engine.search("any query")
        assert results == []
    
    def test_search_no_results(self, temp_db):
        """Test search with no matching results"""
        engine = SimpleSearchEngine(temp_db)
        
        # Index a document
        engine.index_document("http://test.com", "Test", "Some content here")
        
        # Search for non-existent terms
        results = engine.search("nonexistent terms")
        assert results == []