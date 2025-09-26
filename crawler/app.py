from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
import os
import time
import threading
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import logging

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

# Crawler state
crawl_tasks = {}

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

def get_crawler_settings():
    """Get current crawler settings from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT setting_name, setting_value FROM crawler_settings")
        settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
        cursor.close()
        conn.close()
        
        # Convert string values to appropriate types
        settings['rate_limit_delay'] = float(settings.get('rate_limit_delay', 2))
        settings['max_depth'] = int(settings.get('max_depth', 3))
        settings['respect_robots_txt'] = settings.get('respect_robots_txt', 'true').lower() == 'true'
        settings['user_agent'] = settings.get('user_agent', 'DarkwebSearch-Crawler/1.0')
        
        return settings
    except Exception as e:
        logger.error(f"Error getting crawler settings: {e}")
        return {
            'rate_limit_delay': 2.0,
            'max_depth': 3,
            'respect_robots_txt': True,
            'user_agent': 'DarkwebSearch-Crawler/1.0'
        }

def create_driver():
    """Create a configured Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        logger.error(f"Error creating WebDriver: {e}")
        return None

def check_robots_txt(url, user_agent):
    """Check if crawling is allowed by robots.txt"""
    try:
        rp = RobotFileParser()
        robots_url = urljoin(url, '/robots.txt')
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logger.warning(f"Error checking robots.txt for {url}: {e}")
        return True  # Allow crawling if robots.txt check fails

def extract_text_content(html):
    """Extract clean text content from HTML"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text content: {e}")
        return ""

def extract_links(html, base_url):
    """Extract all links from HTML"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                if full_url.startswith(('http://', 'https://')):
                    links.append(full_url)
        
        return list(set(links))  # Remove duplicates
    except Exception as e:
        logger.error(f"Error extracting links: {e}")
        return []

def store_crawled_data(url, title, content):
    """Store crawled data in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO crawled_data (url, title, content, status)
            VALUES (%s, %s, %s, 'completed')
            ON DUPLICATE KEY UPDATE 
            title = VALUES(title),
            content = VALUES(content),
            status = VALUES(status),
            crawled_at = NOW()
        """, (url, title, content))
        
        crawled_data_id = cursor.lastrowid or cursor.execute("SELECT LAST_INSERT_ID()").fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        # Trigger analysis
        try:
            analysis_url = os.getenv('ANALYSIS_URL', 'http://localhost:5002')
            requests.post(f'{analysis_url}/analyze', json={'crawled_data_id': crawled_data_id}, timeout=10)
        except Exception as e:
            logger.warning(f"Failed to trigger analysis: {e}")
        
        return crawled_data_id
        
    except Exception as e:
        logger.error(f"Error storing crawled data: {e}")
        return None

def crawl_url(url, settings, visited_urls, depth=0):
    """Crawl a single URL"""
    if depth > settings['max_depth'] or url in visited_urls:
        return []
    
    visited_urls.add(url)
    
    # Check robots.txt if enabled
    if settings['respect_robots_txt'] and not check_robots_txt(url, settings['user_agent']):
        logger.info(f"Robots.txt disallows crawling {url}")
        return []
    
    # Rate limiting
    time.sleep(settings['rate_limit_delay'])
    
    driver = create_driver()
    if not driver:
        return []
    
    try:
        logger.info(f"Crawling: {url} (depth {depth})")
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get page source
        html = driver.page_source
        title = driver.title
        
        # Extract content and links
        content = extract_text_content(html)
        links = extract_links(html, url)
        
        # Store data
        if content.strip():
            store_crawled_data(url, title, content)
            logger.info(f"Stored data for {url}")
        
        return links
        
    except Exception as e:
        logger.error(f"Error crawling {url}: {e}")
        return []
    finally:
        driver.quit()

def crawl_worker(task_id, start_urls, settings):
    """Worker function for crawling task"""
    try:
        crawl_tasks[task_id]['status'] = 'running'
        crawl_tasks[task_id]['progress'] = 0
        
        visited_urls = set()
        urls_to_crawl = list(start_urls)
        total_urls = len(urls_to_crawl)
        crawled_count = 0
        
        while urls_to_crawl and crawled_count < 50:  # Limit to 50 URLs per task
            current_url = urls_to_crawl.pop(0)
            
            if current_url in visited_urls:
                continue
            
            # Crawl the URL
            new_links = crawl_url(current_url, settings, visited_urls, depth=0)
            
            # Add new links to crawl queue (only from same domain for safety)
            current_domain = urlparse(current_url).netloc
            for link in new_links:
                link_domain = urlparse(link).netloc
                if link_domain == current_domain and link not in visited_urls:
                    urls_to_crawl.append(link)
            
            crawled_count += 1
            crawl_tasks[task_id]['progress'] = (crawled_count / min(total_urls + len(new_links), 50)) * 100
            crawl_tasks[task_id]['crawled_urls'] = list(visited_urls)
        
        crawl_tasks[task_id]['status'] = 'completed'
        crawl_tasks[task_id]['progress'] = 100
        
    except Exception as e:
        logger.error(f"Error in crawl worker: {e}")
        crawl_tasks[task_id]['status'] = 'failed'
        crawl_tasks[task_id]['error'] = str(e)

@app.route('/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'crawler',
        'active_tasks': len([t for t in crawl_tasks.values() if t['status'] == 'running'])
    })

@app.route('/crawl', methods=['POST'])
def start_crawl():
    """Start a new crawl task"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # For demo purposes, we'll use some test URLs
    # In a real implementation, you'd have a way to convert queries to starting URLs
    test_urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/robots.txt',
        'https://example.com'
    ]
    
    # Create task
    task_id = f"crawl_{int(time.time())}"
    crawl_tasks[task_id] = {
        'id': task_id,
        'query': query,
        'status': 'pending',
        'progress': 0,
        'created_at': time.time(),
        'crawled_urls': []
    }
    
    # Get current settings
    settings = get_crawler_settings()
    
    # Start crawling in background thread
    thread = threading.Thread(target=crawl_worker, args=(task_id, test_urls, settings))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message': 'Crawl task started',
        'task_id': task_id,
        'query': query
    })

@app.route('/tasks')
def list_tasks():
    """List all crawl tasks"""
    return jsonify({'tasks': list(crawl_tasks.values())})

@app.route('/tasks/<task_id>')
def get_task(task_id):
    """Get specific task details"""
    if task_id not in crawl_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(crawl_tasks[task_id])

@app.route('/settings', methods=['GET'])
def get_settings():
    """Get current crawler settings"""
    settings = get_crawler_settings()
    return jsonify(settings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)