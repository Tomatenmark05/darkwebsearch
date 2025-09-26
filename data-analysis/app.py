from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import json
import re
import time
import threading
from collections import Counter
import logging

# ML and NLP imports
import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'darkweb_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'darkweb_pass'),
    'database': os.getenv('MYSQL_DATABASE', 'darkwebsearch')
}

# Analysis tasks
analysis_tasks = {}

def get_db_connection():
    """Get database connection with retry logic"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2)

def get_analysis_settings():
    """Get current analysis settings from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT setting_name, setting_value FROM analysis_settings")
        settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
        cursor.close()
        conn.close()
        
        # Convert string values to appropriate types
        settings['min_content_length'] = int(settings.get('min_content_length', 100))
        settings['enable_sentiment_analysis'] = settings.get('enable_sentiment_analysis', 'true').lower() == 'true'
        settings['enable_categorization'] = settings.get('enable_categorization', 'true').lower() == 'true'
        settings['language_detection'] = settings.get('language_detection', 'true').lower() == 'true'
        
        return settings
    except Exception as e:
        logger.error(f"Error getting analysis settings: {e}")
        return {
            'min_content_length': 100,
            'enable_sentiment_analysis': True,
            'enable_categorization': True,
            'language_detection': True
        }

def clean_text(text):
    """Clean and preprocess text for analysis"""
    if not text:
        return ""
    
    # Remove extra whitespace and special characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = text.strip().lower()
    
    return text

def extract_keywords(text, num_keywords=10):
    """Extract important keywords from text using TF-IDF"""
    try:
        if not text or len(text) < 50:
            return []
        
        # Use TF-IDF to find important terms
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Get top keywords
        keyword_scores = list(zip(feature_names, tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        keywords = [kw[0] for kw in keyword_scores[:num_keywords] if kw[1] > 0]
        return keywords
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []

def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    try:
        if not text:
            return 0.0
        
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity  # Returns value between -1 and 1
        return round(sentiment, 2)
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return 0.0

def categorize_content(text, keywords):
    """Categorize content based on keywords and patterns"""
    try:
        if not text:
            return "unknown"
        
        text_lower = text.lower()
        categories = {
            'technology': ['software', 'computer', 'internet', 'tech', 'programming', 'code', 'api', 'database'],
            'security': ['security', 'password', 'encryption', 'hack', 'vulnerability', 'privacy', 'protection'],
            'business': ['business', 'company', 'market', 'finance', 'money', 'profit', 'service', 'customer'],
            'news': ['news', 'report', 'update', 'announcement', 'press', 'media', 'journalism'],
            'education': ['education', 'learning', 'school', 'university', 'course', 'tutorial', 'guide'],
            'health': ['health', 'medical', 'doctor', 'medicine', 'treatment', 'patient', 'hospital'],
            'entertainment': ['entertainment', 'movie', 'music', 'game', 'sport', 'fun', 'video']
        }
        
        category_scores = {}
        
        for category, category_keywords in categories.items():
            score = 0
            # Check in main text
            for keyword in category_keywords:
                score += text_lower.count(keyword)
            
            # Check in extracted keywords
            for keyword in keywords:
                if keyword.lower() in category_keywords:
                    score += 2  # Give more weight to TF-IDF keywords
            
            category_scores[category] = score
        
        # Return category with highest score, or 'general' if no clear category
        if max(category_scores.values()) > 0:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'general'
            
    except Exception as e:
        logger.error(f"Error categorizing content: {e}")
        return 'unknown'

def detect_language(text):
    """Detect language of text"""
    try:
        if not text:
            return 'unknown'
        
        blob = TextBlob(text)
        return blob.detect_language()
        
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return 'unknown'

def analyze_content(crawled_data_id, content, settings):
    """Perform comprehensive analysis on content"""
    try:
        results = {
            'crawled_data_id': crawled_data_id,
            'tags': [],
            'sentiment_score': 0.0,
            'category': 'unknown',
            'language': 'unknown',
            'keywords': []
        }
        
        if not content or len(content) < settings['min_content_length']:
            return results
        
        # Clean text
        clean_content = clean_text(content)
        
        # Extract keywords
        keywords = extract_keywords(clean_content)
        results['keywords'] = keywords
        
        # Analyze sentiment if enabled
        if settings['enable_sentiment_analysis']:
            results['sentiment_score'] = analyze_sentiment(content)
        
        # Categorize content if enabled
        if settings['enable_categorization']:
            results['category'] = categorize_content(content, keywords)
        
        # Detect language if enabled
        if settings['language_detection']:
            results['language'] = detect_language(content)
        
        # Create tags from keywords and analysis
        tags = keywords[:5]  # Top 5 keywords
        if results['category'] != 'unknown':
            tags.append(f"category:{results['category']}")
        if results['language'] != 'unknown':
            tags.append(f"lang:{results['language']}")
        if results['sentiment_score'] > 0.1:
            tags.append("sentiment:positive")
        elif results['sentiment_score'] < -0.1:
            tags.append("sentiment:negative")
        else:
            tags.append("sentiment:neutral")
        
        results['tags'] = tags
        
        return results
        
    except Exception as e:
        logger.error(f"Error analyzing content: {e}")
        return {
            'crawled_data_id': crawled_data_id,
            'tags': [],
            'sentiment_score': 0.0,
            'category': 'unknown'
        }

def store_analysis_results(results):
    """Store analysis results in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analysis_results (crawled_data_id, tags, sentiment_score, category)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            tags = VALUES(tags),
            sentiment_score = VALUES(sentiment_score),
            category = VALUES(category),
            analyzed_at = NOW()
        """, (
            results['crawled_data_id'],
            json.dumps(results['tags']),
            results['sentiment_score'],
            results['category']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Stored analysis results for crawled_data_id {results['crawled_data_id']}")
        return True
        
    except Exception as e:
        logger.error(f"Error storing analysis results: {e}")
        return False

@app.route('/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'data-analysis',
        'active_tasks': len([t for t in analysis_tasks.values() if t['status'] == 'running'])
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze crawled data"""
    data = request.get_json()
    crawled_data_id = data.get('crawled_data_id')
    
    if not crawled_data_id:
        return jsonify({'error': 'crawled_data_id is required'}), 400
    
    try:
        # Get crawled data from database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, content FROM crawled_data WHERE id = %s", (crawled_data_id,))
        crawled_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not crawled_data:
            return jsonify({'error': 'Crawled data not found'}), 404
        
        # Get analysis settings
        settings = get_analysis_settings()
        
        # Perform analysis
        results = analyze_content(crawled_data_id, crawled_data['content'], settings)
        
        # Store results
        if store_analysis_results(results):
            return jsonify({
                'message': 'Analysis completed successfully',
                'results': results
            })
        else:
            return jsonify({'error': 'Failed to store analysis results'}), 500
            
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple crawled data entries"""
    data = request.get_json()
    crawled_data_ids = data.get('crawled_data_ids', [])
    
    if not crawled_data_ids:
        return jsonify({'error': 'crawled_data_ids is required'}), 400
    
    # Create batch analysis task
    task_id = f"batch_analysis_{int(time.time())}"
    analysis_tasks[task_id] = {
        'id': task_id,
        'status': 'pending',
        'progress': 0,
        'total': len(crawled_data_ids),
        'completed': 0,
        'created_at': time.time()
    }
    
    # Start analysis in background thread
    def batch_worker():
        try:
            analysis_tasks[task_id]['status'] = 'running'
            settings = get_analysis_settings()
            
            for i, crawled_data_id in enumerate(crawled_data_ids):
                try:
                    # Get crawled data
                    conn = get_db_connection()
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT id, content FROM crawled_data WHERE id = %s", (crawled_data_id,))
                    crawled_data = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    
                    if crawled_data:
                        # Analyze and store
                        results = analyze_content(crawled_data_id, crawled_data['content'], settings)
                        store_analysis_results(results)
                    
                    analysis_tasks[task_id]['completed'] = i + 1
                    analysis_tasks[task_id]['progress'] = ((i + 1) / len(crawled_data_ids)) * 100
                    
                except Exception as e:
                    logger.error(f"Error analyzing crawled_data_id {crawled_data_id}: {e}")
            
            analysis_tasks[task_id]['status'] = 'completed'
            analysis_tasks[task_id]['progress'] = 100
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            analysis_tasks[task_id]['status'] = 'failed'
            analysis_tasks[task_id]['error'] = str(e)
    
    thread = threading.Thread(target=batch_worker)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message': 'Batch analysis started',
        'task_id': task_id,
        'total': len(crawled_data_ids)
    })

@app.route('/tasks')
def list_tasks():
    """List all analysis tasks"""
    return jsonify({'tasks': list(analysis_tasks.values())})

@app.route('/tasks/<task_id>')
def get_task(task_id):
    """Get specific task details"""
    if task_id not in analysis_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(analysis_tasks[task_id])

@app.route('/analytics')
def analytics():
    """Get analytics about analyzed data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get category distribution
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM analysis_results 
            WHERE category IS NOT NULL 
            GROUP BY category
        """)
        categories = cursor.fetchall()
        
        # Get sentiment distribution
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN sentiment_score > 0.1 THEN 'positive'
                    WHEN sentiment_score < -0.1 THEN 'negative'
                    ELSE 'neutral'
                END as sentiment,
                COUNT(*) as count
            FROM analysis_results 
            WHERE sentiment_score IS NOT NULL
            GROUP BY sentiment
        """)
        sentiments = cursor.fetchall()
        
        # Get recent analysis count
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM analysis_results 
            WHERE analyzed_at > DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        recent_count = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'categories': categories,
            'sentiments': sentiments,
            'recent_analyses': recent_count
        })
        
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/settings', methods=['GET'])
def get_settings():
    """Get current analysis settings"""
    settings = get_analysis_settings()
    return jsonify(settings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)