"""
Simple Web Server for Dark Web Search Tool
Using only Python built-in modules for demonstration
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from search import SimpleSearchEngine
from simple_parser import SimpleContentParser

class SearchHandler(BaseHTTPRequestHandler):
    
    search_engine = None
    parser = None
    
    @classmethod
    def init_shared_resources(cls):
        if cls.search_engine is None:
            cls.search_engine = SimpleSearchEngine('data/search_index.db')
            cls.parser = SimpleContentParser()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_home()
        elif self.path.startswith('/search'):
            self.serve_search_page()
        elif self.path.startswith('/static/'):
            self.serve_static()
        elif self.path == '/api/health':
            self.serve_health_check()
        else:
            self.serve_404()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/search':
            self.handle_search()
        else:
            self.serve_404()
    
    def serve_home(self):
        """Serve the homepage"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Web Search Tool</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; margin-bottom: 10px; }
        .header p { color: #666; }
        .search-box { margin: 20px 0; }
        .search-box input { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px; }
        .search-box button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature { padding: 20px; border: 1px solid #eee; border-radius: 8px; }
        .feature h3 { color: #333; margin-top: 0; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dark Web Search Tool</h1>
            <p>A clear text search tool for dark web content analysis - Educational Project</p>
        </div>
        
        <div class="search-box">
            <form action="/search" method="get">
                <input type="text" name="q" placeholder="Enter search terms..." required>
                <button type="submit">Search</button>
            </form>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🔍 Search</h3>
                <p>Search through indexed dark web content using our clear text search engine.</p>
            </div>
            <div class="feature">
                <h3>📊 Analytics</h3>
                <p>View analytics and insights about dark web content patterns and trends.</p>
                <p><em>Coming Soon</em></p>
            </div>
            <div class="feature">
                <h3>📚 Documentation</h3>
                <p>Learn about the project, its methodology, and how to contribute.</p>
            </div>
        </div>
        
        <div class="warning">
            <h4>⚠️ Educational Use Only</h4>
            <p>This tool is designed for educational and research purposes. Please ensure all usage complies with applicable laws and ethical guidelines.</p>
        </div>
        
        <div class="footer">
            <p>Dark Web Search Tool - School Project by 4 Team Members</p>
        </div>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_search_page(self):
        """Serve the search page"""
        query = ""
        if '?' in self.path:
            params = urllib.parse.parse_qs(self.path.split('?')[1])
            query = params.get('q', [''])[0]
        
        results_html = ""
        if query:
            results = SearchHandler.search_engine.search(query, limit=10)
            if results:
                results_html = f"<h3>Search Results for '{query}'</h3>"
                for result in results:
                    results_html += f"""
                    <div style="border: 1px solid #eee; padding: 15px; margin: 10px 0; border-radius: 8px;">
                        <h4><a href="{result['url']}" target="_blank" style="color: #1a73e8; text-decoration: none;">{result['title']}</a></h4>
                        <div style="color: #006621; font-size: 14px;">{result['url']}</div>
                        <p style="color: #4d5156; margin: 5px 0;">{result['snippet']}</p>
                        <small style="color: #999;">Score: {result['score']:.2f}</small>
                    </div>
                    """
            else:
                results_html = f"<div style='background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;'><h3>No results found for '{query}'</h3><p>Try different keywords or check our sample data.</p></div>"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search - Dark Web Search Tool</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .search-box {{ margin: 20px 0; }}
        .search-box input {{ width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px; }}
        .search-box button {{ padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        .nav {{ margin-bottom: 20px; }}
        .nav a {{ color: #007bff; text-decoration: none; margin-right: 20px; }}
        .tips {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">← Home</a>
            <a href="/search">Search</a>
        </div>
        
        <div class="header">
            <h2>Search Dark Web Content</h2>
            <p>Enter your search query to find relevant content from indexed sources.</p>
        </div>
        
        <div class="search-box">
            <form action="/search" method="get">
                <input type="text" name="q" value="{query}" placeholder="Enter search terms..." required>
                <button type="submit">Search</button>
            </form>
        </div>
        
        {results_html}
        
        <div class="tips">
            <h4>Search Tips:</h4>
            <ul>
                <li>Use specific keywords for better results</li>
                <li>Try different variations of your search terms</li>
                <li>Search results are limited to legally accessible content</li>
                <li>All searches are logged for educational analysis</li>
            </ul>
        </div>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_search(self):
        """Handle search POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        
        query = params.get('query', [''])[0]
        results = SearchHandler.search_engine.search(query, limit=10)
        
        response = {
            'query': query,
            'results': results,
            'count': len(results)
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def serve_health_check(self):
        """Serve health check endpoint"""
        response = {'status': 'healthy', 'message': 'Dark Web Search Tool is running'}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def serve_404(self):
        """Serve 404 page"""
        html = """
        <html><body>
        <h1>404 - Page Not Found</h1>
        <p><a href="/">Return to Homepage</a></p>
        </body></html>
        """
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_static(self):
        """Serve static files (placeholder)"""
        self.serve_404()

def main():
    """Start the web server"""
    # Initialize with some sample data
    print("Initializing search engine with sample data...")
    search_engine = SimpleSearchEngine('data/search_index.db')
    
    # Add some sample documents
    sample_docs = [
        {
            'url': 'http://example.onion/crypto',
            'title': 'Cryptocurrency Basics',
            'content': 'Learn about Bitcoin, Ethereum, and other cryptocurrencies. Digital currency, blockchain technology, and decentralized finance.'
        },
        {
            'url': 'http://example.onion/privacy',
            'title': 'Privacy and Security Guide',
            'content': 'Protecting your online privacy with VPN, Tor browser, encryption, and secure communication methods.'
        },
        {
            'url': 'http://example.onion/markets',
            'title': 'Digital Markets Research',
            'content': 'Academic research on digital marketplaces, economic models, and trade patterns in online environments.'
        },
        {
            'url': 'http://example.onion/tech',
            'title': 'Technology and Programming',
            'content': 'Programming tutorials, web development, Python, JavaScript, and cybersecurity fundamentals.'
        }
    ]
    
    for doc in sample_docs:
        search_engine.index_document(doc['url'], doc['title'], doc['content'])
    
    print("Sample data indexed successfully!")
    
    # Start server
    SearchHandler.init_shared_resources()
    port = int(os.getenv('PORT', 8000))
    server = HTTPServer(('localhost', port), SearchHandler)
    print(f"Server starting on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped")
        server.server_close()

if __name__ == '__main__':
    main()