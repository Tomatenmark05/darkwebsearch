"""
Dark Web Search Tool - Main Application Entry Point
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route('/')
def index():
    """Main application homepage"""
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle search requests"""
    if request.method == 'POST':
        query = request.form.get('query', '')
        # TODO: Implement search functionality
        results = {
            'query': query,
            'results': [],
            'message': 'Search functionality not yet implemented'
        }
        return jsonify(results)
    
    return render_template('search.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Dark Web Search Tool is running'})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)