"""
Vercel serverless entry point for the Glass Bead Game.

Vercel's Python runtime calls this module and expects a WSGI `app` object.
We import the Flask app from the parent directory and expose it.

Note: SocketIO (WebSocket) is not available on Vercel's serverless platform.
The dashboards still work via REST API polling — the live terminal and
real-time graph updates fall back to periodic fetches.

For full SocketIO real-time functionality, run locally:
    python app.py
"""
import sys
import os

# Add the project root to the Python path so imports work
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app import app

# Vercel expects a WSGI callable
handler = app