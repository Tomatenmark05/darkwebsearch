"""
Test configuration and utilities
"""

import pytest
import tempfile
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

@pytest.fixture
def sample_content():
    """Sample HTML content for testing"""
    return """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="A test page for the search engine">
        </head>
        <body>
            <h1>Welcome to Test Page</h1>
            <p>This is a sample paragraph with some <strong>important</strong> content.</p>
            <a href="http://example.com">External Link</a>
            <script>console.log('should be removed');</script>
        </body>
    </html>
    """

@pytest.fixture
def sample_parsed_content():
    """Sample parsed content for testing"""
    return {
        'url': 'http://test.com/page1',
        'title': 'Test Page',
        'content': 'Welcome to Test Page This is a sample paragraph with some important content.',
        'metadata': {
            'title': 'Test Page',
            'description': 'A test page for the search engine',
            'keywords': '',
            'language': ''
        }
    }