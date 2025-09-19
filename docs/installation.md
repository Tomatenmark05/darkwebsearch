# Installation Guide

This guide will help you set up the Dark Web Search Tool on your local machine.

## Prerequisites

Before installing the Dark Web Search Tool, ensure you have the following installed:

- **Python 3.8 or higher**
- **Git**
- **pip** (Python package manager)
- **Virtual environment support** (venv or virtualenv)

### Checking Prerequisites

```bash
# Check Python version
python --version
# or
python3 --version

# Check pip
pip --version

# Check git
git --version
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Tomatenmark05/darkwebsearch.git
cd darkwebsearch
```

### 2. Run the Setup Script

The project includes an automated setup script:

```bash
python scripts/setup.py
```

This script will:
- Create necessary directories
- Install Python dependencies
- Set up the database
- Create configuration files

### 3. Manual Setup (Alternative)

If you prefer manual setup or the script fails:

#### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Create Configuration

```bash
# Copy environment configuration
cp config/.env.example .env

# Edit .env file with your settings
# Use your preferred text editor
nano .env
```

#### Initialize Database

```bash
python -c "
import sys
sys.path.append('src')
from search import SimpleSearchEngine
engine = SimpleSearchEngine('data/search_index.db')
print('Database initialized')
"
```

### 4. Verify Installation

Run the application to verify everything is working:

```bash
python src/app.py
```

You should see output similar to:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000
```

Open your web browser and navigate to `http://localhost:5000`. You should see the Dark Web Search Tool homepage.

## Configuration

### Environment Variables

Edit the `.env` file to customize your configuration:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
PORT=5000

# Database Configuration
DATABASE_URL=sqlite:///data/darkweb_search.db
SEARCH_INDEX_DB=data/search_index.db

# Crawler Configuration
CRAWLER_DELAY=1.0
CRAWLER_MAX_RETRIES=3
CRAWLER_TIMEOUT=10

# Security Configuration
ALLOWED_DOMAINS=example.com,test.local
ENABLE_RATE_LIMITING=True
```

### Important Security Notes

- Change the `SECRET_KEY` to a secure random string in production
- Set `FLASK_DEBUG=False` in production environments
- Configure `ALLOWED_DOMAINS` to restrict crawling to specific domains
- Review all security settings before deployment

## Troubleshooting

### Common Issues

#### Python Version Error
```
Error: Python 3.8+ required
```
**Solution**: Install Python 3.8 or higher from [python.org](https://python.org)

#### Permission Denied
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: 
- On Windows: Run command prompt as administrator
- On macOS/Linux: Use `sudo` if necessary or check file permissions

#### Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: 
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

#### Database Connection Error
```
sqlite3.OperationalError: unable to open database file
```
**Solution**:
- Ensure `data/` directory exists
- Check file permissions
- Run setup script again

#### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution**:
- Change port in `.env` file: `PORT=5001`
- Or kill process using the port: `lsof -ti:5000 | xargs kill`

### Getting Help

If you encounter issues not covered here:

1. Check the [troubleshooting section](troubleshooting.md)
2. Search existing [GitHub issues](https://github.com/Tomatenmark05/darkwebsearch/issues)
3. Create a new issue with:
   - Your operating system
   - Python version
   - Error message (full stack trace)
   - Steps to reproduce

## Next Steps

After successful installation:

1. Read the [User Guide](user_guide.md) to learn how to use the tool
2. Review [Development Setup](development.md) if you plan to contribute
3. Check [Architecture Overview](architecture.md) to understand the system

## Uninstallation

To remove the Dark Web Search Tool:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
rm -rf darkwebsearch

# Remove any global configurations (if any)
```