"""
Parser Module - Content Parsing and Processing

This module handles parsing and processing of crawled content,
including text extraction, cleaning, and metadata extraction.
"""

import re
import html
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class ContentParser:
    """Main content parser for web pages"""
    
    def __init__(self):
        self.text_cleaners = [
            self._remove_scripts_and_styles,
            self._clean_whitespace,
            self._remove_special_chars,
            self._unescape_html
        ]
    
    def parse_content(self, raw_content, url=None):
        """
        Parse raw HTML content and extract clean text
        
        Args:
            raw_content (str): Raw HTML content
            url (str): Source URL for context
            
        Returns:
            dict: Parsed content with metadata
        """
        try:
            soup = BeautifulSoup(raw_content, 'html.parser')
            
            # Extract basic metadata
            metadata = self._extract_metadata(soup)
            
            # Extract and clean text content
            text_content = self._extract_text(soup)
            clean_text = self._clean_text(text_content)
            
            # Extract links and other elements
            links = self._extract_links(soup, url)
            
            return {
                'metadata': metadata,
                'clean_text': clean_text,
                'raw_text': text_content,
                'links': links,
                'word_count': len(clean_text.split()),
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error parsing content from {url}: {e}")
            return None
    
    def _extract_metadata(self, soup):
        """Extract metadata from HTML"""
        metadata = {}
        
        # Title
        title_tag = soup.find('title')
        metadata['title'] = title_tag.string.strip() if title_tag else ''
        
        # Meta description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        metadata['description'] = desc_tag.get('content', '') if desc_tag else ''
        
        # Meta keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        metadata['keywords'] = keywords_tag.get('content', '') if keywords_tag else ''
        
        # Language
        html_tag = soup.find('html')
        metadata['language'] = html_tag.get('lang', '') if html_tag else ''
        
        return metadata
    
    def _extract_text(self, soup):
        """Extract text content from soup"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        return text
    
    def _extract_links(self, soup, base_url=None):
        """Extract links from the page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            
            # Convert relative URLs to absolute if base_url provided
            if base_url and not href.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                href = urljoin(base_url, href)
            
            links.append({
                'url': href,
                'text': text,
                'title': link.get('title', '')
            })
        
        return links
    
    def _clean_text(self, text):
        """Apply text cleaning operations"""
        for cleaner in self.text_cleaners:
            text = cleaner(text)
        return text
    
    def _remove_scripts_and_styles(self, text):
        """Remove script and style content"""
        # This is handled in _extract_text, but keeping for consistency
        return text
    
    def _clean_whitespace(self, text):
        """Clean and normalize whitespace"""
        # Replace multiple whitespaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading and trailing whitespace
        text = text.strip()
        return text
    
    def _remove_special_chars(self, text):
        """Remove or replace special characters"""
        # Remove non-printable characters except basic punctuation
        text = re.sub(r'[^\w\s\.,!?;:\'"()-]', ' ', text)
        return text
    
    def _unescape_html(self, text):
        """Unescape HTML entities"""
        return html.unescape(text)

class LanguageDetector:
    """Simple language detection for content"""
    
    def __init__(self):
        # Simple keyword-based detection (can be improved with proper libraries)
        self.language_patterns = {
            'en': ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'],
            'de': ['der', 'die', 'das', 'und', 'oder', 'aber', 'in', 'an', 'zu'],
            'fr': ['le', 'la', 'les', 'et', 'ou', 'mais', 'dans', 'sur', 'à'],
            'es': ['el', 'la', 'los', 'las', 'y', 'o', 'pero', 'en', 'con']
        }
    
    def detect_language(self, text):
        """Detect language of text content"""
        if not text:
            return 'unknown'
        
        words = text.lower().split()[:100]  # Check first 100 words
        
        scores = {}
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for word in words if word in patterns)
            scores[lang] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'unknown'