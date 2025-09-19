"""
Simple Parser Module - Basic Content Parsing without external dependencies

This module provides basic parsing functionality using only Python built-in modules.
"""

import re
import html
import logging

logger = logging.getLogger(__name__)

class SimpleContentParser:
    """Simple content parser using only built-in Python modules"""
    
    def __init__(self):
        self.tag_pattern = re.compile(r'<[^>]+>')
        self.script_pattern = re.compile(r'<script[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
        self.style_pattern = re.compile(r'<style[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE)
    
    def parse_content(self, html_content, url=None):
        """
        Parse HTML content and extract clean text
        
        Args:
            html_content (str): Raw HTML content
            url (str): Source URL for context
            
        Returns:
            dict: Parsed content with metadata
        """
        try:
            # Extract basic metadata
            metadata = self._extract_simple_metadata(html_content)
            
            # Extract and clean text content
            text_content = self._extract_simple_text(html_content)
            clean_text = self._clean_text(text_content)
            
            # Extract links
            links = self._extract_simple_links(html_content, url)
            
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
    
    def _extract_simple_metadata(self, html_content):
        """Extract metadata using regex"""
        metadata = {}
        
        # Title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        metadata['title'] = title_match.group(1).strip() if title_match else ''
        
        # Meta description
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
        metadata['description'] = desc_match.group(1) if desc_match else ''
        
        # Meta keywords
        keywords_match = re.search(r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
        metadata['keywords'] = keywords_match.group(1) if keywords_match else ''
        
        # Language
        lang_match = re.search(r'<html[^>]+lang=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
        metadata['language'] = lang_match.group(1) if lang_match else ''
        
        return metadata
    
    def _extract_simple_text(self, html_content):
        """Extract text content using regex"""
        # Remove script and style elements
        content = self.script_pattern.sub('', html_content)
        content = self.style_pattern.sub('', content)
        
        # Remove HTML tags
        text = self.tag_pattern.sub(' ', content)
        
        return text
    
    def _extract_simple_links(self, html_content, base_url=None):
        """Extract links using regex"""
        links = []
        link_pattern = re.compile(r'<a[^>]+href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
        
        for match in link_pattern.finditer(html_content):
            href = match.group(1)
            text = self.tag_pattern.sub('', match.group(2)).strip()
            
            # Convert relative URLs to absolute if base_url provided
            if base_url and not href.startswith(('http://', 'https://')):
                if href.startswith('/'):
                    # Get domain from base_url
                    domain_match = re.match(r'https?://[^/]+', base_url)
                    if domain_match:
                        href = domain_match.group(0) + href
                else:
                    # Relative path
                    if base_url.endswith('/'):
                        href = base_url + href
                    else:
                        href = base_url + '/' + href
            
            links.append({
                'url': href,
                'text': text,
                'title': ''
            })
        
        return links
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ''
        
        # Unescape HTML entities
        text = html.unescape(text)
        
        # Replace multiple whitespaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading and trailing whitespace
        text = text.strip()
        
        return text

class SimpleLanguageDetector:
    """Simple language detection"""
    
    def __init__(self):
        # Simple keyword-based detection
        self.language_patterns = {
            'en': ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'was', 'were'],
            'de': ['der', 'die', 'das', 'und', 'oder', 'aber', 'in', 'an', 'zu', 'ist', 'sind'],
            'fr': ['le', 'la', 'les', 'et', 'ou', 'mais', 'dans', 'sur', 'à', 'est', 'sont'],
            'es': ['el', 'la', 'los', 'las', 'y', 'o', 'pero', 'en', 'con', 'es', 'son']
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
        
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'unknown'

# Aliases for compatibility
ContentParser = SimpleContentParser
LanguageDetector = SimpleLanguageDetector