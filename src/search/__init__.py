"""
Search Module - Search Engine Implementation

This module provides search functionality for indexed dark web content.
"""

import sqlite3
import re
from collections import defaultdict
import math
import logging

logger = logging.getLogger(__name__)

class SimpleSearchEngine:
    """Simple search engine implementation with TF-IDF scoring"""
    
    def __init__(self, db_path='data/search_index.db'):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Setup SQLite database for search index"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Documents table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE NOT NULL,
                        title TEXT,
                        content TEXT,
                        metadata TEXT,
                        indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Terms table for inverted index
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS terms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        term TEXT UNIQUE NOT NULL,
                        document_frequency INTEGER DEFAULT 0
                    )
                ''')
                
                # Term-document relationships with TF scores
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS term_documents (
                        term_id INTEGER,
                        document_id INTEGER,
                        term_frequency INTEGER,
                        FOREIGN KEY (term_id) REFERENCES terms (id),
                        FOREIGN KEY (document_id) REFERENCES documents (id),
                        PRIMARY KEY (term_id, document_id)
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_terms_term ON terms (term)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_url ON documents (url)')
                
                conn.commit()
                logger.info("Search database initialized successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Database setup error: {e}")
    
    def index_document(self, url, title, content, metadata=None):
        """
        Index a document for search
        
        Args:
            url (str): Document URL
            title (str): Document title
            content (str): Document content
            metadata (dict): Additional metadata
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert or update document
                cursor.execute('''
                    INSERT OR REPLACE INTO documents (url, title, content, metadata)
                    VALUES (?, ?, ?, ?)
                ''', (url, title, content, str(metadata) if metadata else ''))
                
                document_id = cursor.lastrowid
                
                # Tokenize and index content
                tokens = self._tokenize(f"{title} {content}")
                term_frequencies = self._calculate_term_frequencies(tokens)
                
                # Remove old term associations for this document
                cursor.execute('DELETE FROM term_documents WHERE document_id = ?', (document_id,))
                
                # Insert terms and term-document relationships
                for term, frequency in term_frequencies.items():
                    # Insert or get term
                    cursor.execute('INSERT OR IGNORE INTO terms (term) VALUES (?)', (term,))
                    cursor.execute('SELECT id FROM terms WHERE term = ?', (term,))
                    term_id = cursor.fetchone()[0]
                    
                    # Insert term-document relationship
                    cursor.execute('''
                        INSERT INTO term_documents (term_id, document_id, term_frequency)
                        VALUES (?, ?, ?)
                    ''', (term_id, document_id, frequency))
                
                # Update document frequencies
                self._update_document_frequencies(cursor)
                
                conn.commit()
                logger.info(f"Indexed document: {url}")
                
        except sqlite3.Error as e:
            logger.error(f"Error indexing document {url}: {e}")
    
    def search(self, query, limit=10):
        """
        Search for documents matching the query
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results
            
        Returns:
            list: Search results with scores
        """
        try:
            query_terms = self._tokenize(query)
            if not query_terms:
                return []
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total document count
                cursor.execute('SELECT COUNT(*) FROM documents')
                total_docs = cursor.fetchone()[0]
                
                if total_docs == 0:
                    return []
                
                # Calculate TF-IDF scores for each document
                document_scores = defaultdict(float)
                
                for term in query_terms:
                    # Get term information
                    cursor.execute('''
                        SELECT t.id, t.document_frequency
                        FROM terms t
                        WHERE t.term = ?
                    ''', (term,))
                    
                    term_result = cursor.fetchone()
                    if not term_result:
                        continue
                    
                    term_id, doc_frequency = term_result
                    
                    # Calculate IDF
                    idf = math.log(total_docs / max(doc_frequency, 1))
                    
                    # Get documents containing this term
                    cursor.execute('''
                        SELECT td.document_id, td.term_frequency
                        FROM term_documents td
                        WHERE td.term_id = ?
                    ''', (term_id,))
                    
                    for doc_id, term_freq in cursor.fetchall():
                        # Calculate TF-IDF score
                        tf = 1 + math.log(term_freq) if term_freq > 0 else 0
                        tfidf = tf * idf
                        document_scores[doc_id] += tfidf
                
                # Get top documents
                top_docs = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
                
                # Fetch document details
                results = []
                for doc_id, score in top_docs:
                    cursor.execute('''
                        SELECT url, title, content
                        FROM documents
                        WHERE id = ?
                    ''', (doc_id,))
                    
                    doc_result = cursor.fetchone()
                    if doc_result:
                        url, title, content = doc_result
                        
                        # Generate snippet
                        snippet = self._generate_snippet(content, query_terms)
                        
                        results.append({
                            'url': url,
                            'title': title,
                            'snippet': snippet,
                            'score': score
                        })
                
                return results
                
        except sqlite3.Error as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _tokenize(self, text):
        """Tokenize text into searchable terms"""
        if not text:
            return []
        
        # Convert to lowercase and split by non-alphanumeric characters
        text = text.lower()
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text)  # Only words with 3+ characters
        
        # Remove common stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        tokens = [token for token in tokens if token not in stop_words]
        
        return tokens
    
    def _calculate_term_frequencies(self, tokens):
        """Calculate term frequencies from tokens"""
        frequencies = defaultdict(int)
        for token in tokens:
            frequencies[token] += 1
        return dict(frequencies)
    
    def _update_document_frequencies(self, cursor):
        """Update document frequencies for all terms"""
        cursor.execute('''
            UPDATE terms
            SET document_frequency = (
                SELECT COUNT(DISTINCT document_id)
                FROM term_documents
                WHERE term_documents.term_id = terms.id
            )
        ''')
    
    def _generate_snippet(self, content, query_terms, max_length=200):
        """Generate a snippet highlighting query terms"""
        if not content or not query_terms:
            return content[:max_length] + '...' if len(content) > max_length else content
        
        # Find the first occurrence of any query term
        content_lower = content.lower()
        best_position = len(content)
        
        for term in query_terms:
            position = content_lower.find(term.lower())
            if position != -1 and position < best_position:
                best_position = position
        
        # If no terms found, return beginning of content
        if best_position == len(content):
            return content[:max_length] + '...' if len(content) > max_length else content
        
        # Generate snippet around the found term
        start = max(0, best_position - max_length // 2)
        end = min(len(content), start + max_length)
        
        snippet = content[start:end]
        if start > 0:
            snippet = '...' + snippet
        if end < len(content):
            snippet = snippet + '...'
        
        return snippet