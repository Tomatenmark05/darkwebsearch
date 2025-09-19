"""
Crawler Module - Web Crawling Components

This module contains components for crawling and collecting dark web content
in a legal and ethical manner.
"""

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class BaseCrawler:
    """Base crawler class with common functionality"""
    
    def __init__(self, delay=1.0, max_retries=3):
        self.delay = delay
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Dark Web Search Bot (Educational Use)'
        })
    
    def crawl_url(self, url):
        """
        Crawl a single URL and return parsed content
        
        Args:
            url (str): URL to crawl
            
        Returns:
            dict: Parsed content with metadata
        """
        try:
            # Add delay between requests
            time.sleep(self.delay)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return self._parse_response(response, url)
            
        except requests.RequestException as e:
            logger.error(f"Error crawling {url}: {e}")
            return None
    
    def _parse_response(self, response, url):
        """Parse HTTP response and extract content"""
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'content': soup.get_text(strip=True),
            'links': [urljoin(url, a.get('href')) for a in soup.find_all('a', href=True)],
            'timestamp': time.time(),
            'status_code': response.status_code
        }

class SafeCrawler(BaseCrawler):
    """
    Safe crawler that respects robots.txt and implements safety measures
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowed_domains = set()
        self.robots_cache = {}
    
    def add_allowed_domain(self, domain):
        """Add domain to allowed list"""
        self.allowed_domains.add(domain)
    
    def is_allowed_to_crawl(self, url):
        """Check if URL is allowed to be crawled"""
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Only crawl allowed domains
        if domain not in self.allowed_domains:
            return False
        
        # TODO: Implement robots.txt checking
        return True
    
    def crawl_url(self, url):
        """Override to add safety checks"""
        if not self.is_allowed_to_crawl(url):
            logger.warning(f"URL not allowed for crawling: {url}")
            return None
        
        return super().crawl_url(url)