#!/usr/bin/env python3
"""
Script to run the Home Evaluator web application
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Home Evaluator Web Application")
    print("=" * 60)
    print()
    print("Starting server on http://127.0.0.1:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
