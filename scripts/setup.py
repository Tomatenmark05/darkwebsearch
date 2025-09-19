#!/usr/bin/env python3
"""
Setup script for Dark Web Search Tool

This script helps set up the development environment and initialize
the database structure.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'logs',
        'data/scraped',
        'data/samples'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def setup_database():
    """Initialize the database"""
    print("Setting up database...")
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    try:
        from search import SimpleSearchEngine
        
        # Create search index database
        engine = SimpleSearchEngine('data/search_index.db')
        print("Search database initialized!")
        
        return True
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

def create_env_file():
    """Create .env file from example"""
    env_file = Path('.env')
    env_example = Path('config/.env.example')
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("Created .env file from example")
        print("Please edit .env file to customize your configuration")
    else:
        print(".env file already exists or example not found")

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pytest', 'tests/', '-v'])
        print("All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Some tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up Dark Web Search Tool...")
    print("=" * 50)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Installing dependencies", install_dependencies),
        ("Setting up database", setup_database),
        ("Creating environment file", create_env_file),
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            if step_func():
                print(f"✓ {step_name} completed successfully")
                success_count += 1
            else:
                print(f"✗ {step_name} failed")
        except Exception as e:
            print(f"✗ {step_name} failed with error: {e}")
    
    print(f"\nSetup completed: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file to customize configuration")
        print("2. Run 'python src/app.py' to start the application")
        print("3. Visit http://localhost:5000 to use the search tool")
    else:
        print("\n⚠️ Setup completed with some errors. Please check the output above.")

if __name__ == "__main__":
    main()