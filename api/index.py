"""
Vercel serverless function entry point
Wraps the Flask app for Vercel deployment
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Disable database for serverless (use in-memory or disable)
os.environ['DISABLE_DATABASE'] = '1'

from app import app

# Vercel WSGI handler
def handler(event, context):
    return app(event, context)

