"""
Vercel serverless function entry point
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Disable database for serverless
os.environ['DISABLE_DATABASE'] = '1'

# Import the Flask app
from app import app

# This is the WSGI application Vercel will use
# No need for a handler function - just export app directly
app = app

