from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import mysql.connector
import requests
import os
import json
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'darkweb_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'darkweb_pass'),
    'database': os.getenv('MYSQL_DATABASE', 'darkwebsearch')
}

# Service URLs
CRAWLER_URL = os.getenv('CRAWLER_URL', 'http://localhost:5001')
ANALYSIS_URL = os.getenv('ANALYSIS_URL', 'http://localhost:5002')

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

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Darkwebsearch Manager</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            .service-status { display: flex; gap: 20px; margin: 20px 0; }
            .service { border: 1px solid #ddd; padding: 15px; border-radius: 5px; flex: 1; }
            .online { border-color: #4CAF50; }
            .offline { border-color: #f44336; }
            button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .search-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            input[type="text"] { width: 300px; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            .results { margin-top: 20px; }
            .result-item { border: 1px solid #eee; padding: 10px; margin: 5px 0; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕸️ Darkwebsearch Manager Dashboard</h1>
            
            <div class="service-status">
                <div class="service" id="manager-status">
                    <h3>Manager Service</h3>
                    <p>Status: <span style="color: #4CAF50;">●</span> Online</p>
                    <p>Port: 5000</p>
                </div>
                
                <div class="service" id="crawler-status">
                    <h3>Crawler Service</h3>
                    <p>Status: <span id="crawler-dot">●</span> <span id="crawler-text">Checking...</span></p>
                    <p>Port: 5001</p>
                    <button onclick="window.open('/crawler-settings', '_blank')">Crawler Settings</button>
                </div>
                
                <div class="service" id="analysis-status">
                    <h3>Data Analysis Service</h3>
                    <p>Status: <span id="analysis-dot">●</span> <span id="analysis-text">Checking...</span></p>
                    <p>Port: 5002</p>
                    <button onclick="window.open('/analysis-settings', '_blank')">Analysis Settings</button>
                </div>
                
                <div class="service" id="gui-status">
                    <h3>SvelteKit GUI</h3>
                    <p>Status: <span style="color: #4CAF50;">●</span> Available</p>
                    <p>Port: 3000</p>
                    <button onclick="window.open('http://localhost:3000', '_blank')">Open GUI</button>
                </div>
            </div>
            
            <div class="search-section">
                <h2>Search Management</h2>
                <input type="text" id="searchQuery" placeholder="Enter search query...">
                <button onclick="performSearch()">Search</button>
                <button onclick="startCrawl()">Start Crawl</button>
                
                <div class="results" id="searchResults"></div>
            </div>
            
            <div class="search-section">
                <h2>Recent Activity</h2>
                <div id="recentActivity">Loading...</div>
            </div>
        </div>
        
        <script>
            // Check service status
            async function checkServices() {
                try {
                    const crawlerResponse = await fetch('/api/crawler/status');
                    if (crawlerResponse.ok) {
                        document.getElementById('crawler-dot').style.color = '#4CAF50';
                        document.getElementById('crawler-text').textContent = 'Online';
                    } else {
                        document.getElementById('crawler-dot').style.color = '#f44336';
                        document.getElementById('crawler-text').textContent = 'Offline';
                    }
                } catch (e) {
                    document.getElementById('crawler-dot').style.color = '#f44336';
                    document.getElementById('crawler-text').textContent = 'Offline';
                }
                
                try {
                    const analysisResponse = await fetch('/api/analysis/status');
                    if (analysisResponse.ok) {
                        document.getElementById('analysis-dot').style.color = '#4CAF50';
                        document.getElementById('analysis-text').textContent = 'Online';
                    } else {
                        document.getElementById('analysis-dot').style.color = '#f44336';
                        document.getElementById('analysis-text').textContent = 'Offline';
                    }
                } catch (e) {
                    document.getElementById('analysis-dot').style.color = '#f44336';
                    document.getElementById('analysis-text').textContent = 'Offline';
                }
            }
            
            async function performSearch() {
                const query = document.getElementById('searchQuery').value;
                if (!query) return;
                
                const resultsDiv = document.getElementById('searchResults');
                resultsDiv.innerHTML = 'Searching...';
                
                try {
                    const response = await fetch('/api/search', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    });
                    const data = await response.json();
                    
                    if (data.results && data.results.length > 0) {
                        resultsDiv.innerHTML = data.results.map(result => 
                            `<div class="result-item">
                                <h4>${result.title || 'No title'}</h4>
                                <p><a href="${result.url}" target="_blank">${result.url}</a></p>
                                <p>${result.content ? result.content.substring(0, 200) + '...' : 'No content'}</p>
                                <small>Crawled: ${result.crawled_at}</small>
                            </div>`
                        ).join('');
                    } else {
                        resultsDiv.innerHTML = '<p>No results found. Try starting a crawl first.</p>';
                    }
                } catch (e) {
                    resultsDiv.innerHTML = 'Error performing search: ' + e.message;
                }
            }
            
            async function startCrawl() {
                const query = document.getElementById('searchQuery').value;
                if (!query) {
                    alert('Please enter a search query first');
                    return;
                }
                
                try {
                    const response = await fetch('/api/crawl/start', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    });
                    const data = await response.json();
                    alert('Crawl started: ' + data.message);
                } catch (e) {
                    alert('Error starting crawl: ' + e.message);
                }
            }
            
            async function loadRecentActivity() {
                try {
                    const response = await fetch('/api/recent-activity');
                    const data = await response.json();
                    
                    const activityDiv = document.getElementById('recentActivity');
                    if (data.activity && data.activity.length > 0) {
                        activityDiv.innerHTML = data.activity.map(item => 
                            `<div class="result-item">
                                <strong>${item.type}</strong> - ${item.description}
                                <small style="float: right;">${item.timestamp}</small>
                            </div>`
                        ).join('');
                    } else {
                        activityDiv.innerHTML = '<p>No recent activity</p>';
                    }
                } catch (e) {
                    document.getElementById('recentActivity').innerHTML = 'Error loading activity';
                }
            }
            
            // Initialize
            checkServices();
            loadRecentActivity();
            setInterval(checkServices, 30000); // Check every 30 seconds
        </script>
    </body>
    </html>
    ''')

@app.route('/api/search', methods=['POST'])
def search():
    """Handle search requests from GUI"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        # Check cache first
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT results FROM search_queries WHERE query_text = %s AND created_at > DATE_SUB(NOW(), INTERVAL 1 HOUR)",
            (query,)
        )
        cached_result = cursor.fetchone()
        
        if cached_result:
            return jsonify({'results': json.loads(cached_result['results']), 'cached': True})
        
        # Search in crawled data
        cursor.execute("""
            SELECT cd.url, cd.title, cd.content, cd.crawled_at, ar.tags, ar.category
            FROM crawled_data cd
            LEFT JOIN analysis_results ar ON cd.id = ar.crawled_data_id
            WHERE cd.title LIKE %s OR cd.content LIKE %s
            ORDER BY cd.crawled_at DESC
            LIMIT 20
        """, (f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        
        # Cache the results
        cursor.execute(
            "INSERT INTO search_queries (query_text, results) VALUES (%s, %s) ON DUPLICATE KEY UPDATE results = VALUES(results), updated_at = NOW()",
            (query, json.dumps(results, default=str))
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({'results': results, 'cached': False})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crawl/start', methods=['POST'])
def start_crawl():
    """Start crawling process"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    try:
        response = requests.post(f'{CRAWLER_URL}/crawl', json={'query': query}, timeout=10)
        if response.status_code == 200:
            return jsonify({'message': 'Crawl started successfully', 'task_id': response.json().get('task_id')})
        else:
            return jsonify({'error': 'Failed to start crawl'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Crawler service unavailable: {str(e)}'}), 503

@app.route('/api/crawler/status')
def crawler_status():
    """Check crawler service status"""
    try:
        response = requests.get(f'{CRAWLER_URL}/status', timeout=5)
        return jsonify({'status': 'online', 'details': response.json()})
    except requests.exceptions.RequestException:
        return jsonify({'status': 'offline'}), 503

@app.route('/api/analysis/status')
def analysis_status():
    """Check analysis service status"""
    try:
        response = requests.get(f'{ANALYSIS_URL}/status', timeout=5)
        return jsonify({'status': 'online', 'details': response.json()})
    except requests.exceptions.RequestException:
        return jsonify({'status': 'offline'}), 503

@app.route('/api/recent-activity')
def recent_activity():
    """Get recent system activity"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get recent crawls
        cursor.execute("""
            SELECT 'Crawl' as type, CONCAT('Crawled: ', title) as description, crawled_at as timestamp
            FROM crawled_data 
            ORDER BY crawled_at DESC 
            LIMIT 10
        """)
        
        activity = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'activity': activity})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/crawler-settings')
def crawler_settings():
    """Embedded crawler settings GUI"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crawler Settings</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .setting { margin: 15px 0; }
            .setting label { display: inline-block; width: 200px; }
            .setting input, .setting select { width: 200px; padding: 5px; }
            button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin: 5px; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>🕷️ Crawler Settings</h1>
        <form id="settingsForm">
            <div class="setting">
                <label>Rate Limit Delay (seconds):</label>
                <input type="number" id="rate_limit_delay" min="1" max="10" step="0.5">
            </div>
            <div class="setting">
                <label>Max Crawl Depth:</label>
                <input type="number" id="max_depth" min="1" max="10">
            </div>
            <div class="setting">
                <label>Respect robots.txt:</label>
                <select id="respect_robots_txt">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            <div class="setting">
                <label>User Agent:</label>
                <input type="text" id="user_agent" style="width: 300px;">
            </div>
            <button type="submit">Save Settings</button>
            <button type="button" onclick="loadSettings()">Load Current Settings</button>
        </form>
        
        <script>
            async function loadSettings() {
                try {
                    const response = await fetch('/api/crawler/settings');
                    const settings = await response.json();
                    
                    Object.keys(settings).forEach(key => {
                        const element = document.getElementById(key);
                        if (element) {
                            element.value = settings[key];
                        }
                    });
                } catch (e) {
                    alert('Error loading settings: ' + e.message);
                }
            }
            
            document.getElementById('settingsForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const settings = {
                    rate_limit_delay: document.getElementById('rate_limit_delay').value,
                    max_depth: document.getElementById('max_depth').value,
                    respect_robots_txt: document.getElementById('respect_robots_txt').value,
                    user_agent: document.getElementById('user_agent').value
                };
                
                try {
                    const response = await fetch('/api/crawler/settings', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(settings)
                    });
                    
                    if (response.ok) {
                        alert('Settings saved successfully!');
                    } else {
                        alert('Error saving settings');
                    }
                } catch (e) {
                    alert('Error saving settings: ' + e.message);
                }
            };
            
            // Load settings on page load
            loadSettings();
        </script>
    </body>
    </html>
    ''')

@app.route('/analysis-settings')
def analysis_settings():
    """Embedded analysis settings GUI"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analysis Settings</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .setting { margin: 15px 0; }
            .setting label { display: inline-block; width: 250px; }
            .setting input, .setting select { width: 200px; padding: 5px; }
            button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin: 5px; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>📊 Data Analysis Settings</h1>
        <form id="settingsForm">
            <div class="setting">
                <label>Minimum Content Length:</label>
                <input type="number" id="min_content_length" min="50" max="1000">
            </div>
            <div class="setting">
                <label>Enable Sentiment Analysis:</label>
                <select id="enable_sentiment_analysis">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            <div class="setting">
                <label>Enable Categorization:</label>
                <select id="enable_categorization">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            <div class="setting">
                <label>Language Detection:</label>
                <select id="language_detection">
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </div>
            <button type="submit">Save Settings</button>
            <button type="button" onclick="loadSettings()">Load Current Settings</button>
        </form>
        
        <script>
            async function loadSettings() {
                try {
                    const response = await fetch('/api/analysis/settings');
                    const settings = await response.json();
                    
                    Object.keys(settings).forEach(key => {
                        const element = document.getElementById(key);
                        if (element) {
                            element.value = settings[key];
                        }
                    });
                } catch (e) {
                    alert('Error loading settings: ' + e.message);
                }
            }
            
            document.getElementById('settingsForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const settings = {
                    min_content_length: document.getElementById('min_content_length').value,
                    enable_sentiment_analysis: document.getElementById('enable_sentiment_analysis').value,
                    enable_categorization: document.getElementById('enable_categorization').value,
                    language_detection: document.getElementById('language_detection').value
                };
                
                try {
                    const response = await fetch('/api/analysis/settings', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(settings)
                    });
                    
                    if (response.ok) {
                        alert('Settings saved successfully!');
                    } else {
                        alert('Error saving settings');
                    }
                } catch (e) {
                    alert('Error saving settings: ' + e.message);
                }
            };
            
            // Load settings on page load
            loadSettings();
        </script>
    </body>
    </html>
    ''')

@app.route('/api/crawler/settings', methods=['GET', 'POST'])
def crawler_settings_api():
    """Handle crawler settings"""
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT setting_name, setting_value FROM crawler_settings")
            settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
            cursor.close()
            conn.close()
            return jsonify(settings)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            settings = request.get_json()
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for key, value in settings.items():
                cursor.execute(
                    "INSERT INTO crawler_settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)",
                    (key, value)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Settings saved successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/settings', methods=['GET', 'POST'])
def analysis_settings_api():
    """Handle analysis settings"""
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT setting_name, setting_value FROM analysis_settings")
            settings = {row['setting_name']: row['setting_value'] for row in cursor.fetchall()}
            cursor.close()
            conn.close()
            return jsonify(settings)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            settings = request.get_json()
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for key, value in settings.items():
                cursor.execute(
                    "INSERT INTO analysis_settings (setting_name, setting_value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)",
                    (key, value)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Settings saved successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)