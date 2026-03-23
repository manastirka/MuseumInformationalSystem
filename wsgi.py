#!/usr/bin/env python3
"""
WSGI entry point for Museum Information System
Production server configuration
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import create_app

# This is what gunicorn looks for
application = create_app()

if __name__ == "__main__":
    application.run()
