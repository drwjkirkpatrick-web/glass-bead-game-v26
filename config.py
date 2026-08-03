"""Glass Bead Game v26 — Configuration"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'glass-bead-castalian-secret'
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'

    # SocketIO — use threading for Vercel/serverless compatibility,
    # eventlet for localhost long-running server
    IS_VERCEL = os.environ.get('VERCEL') is not None
    ASYNC_MODE = 'threading' if IS_VERCEL else 'eventlet'

    # Game settings
    GAME_NAME = 'Modern Glass Bead Game'
    GAME_VERSION = 'v26'
    
    # Domains / Disciplines
    DOMAINS = [
        'musica',
        'mathematica',
        'historia',
        'natura',
        'lingua',
        'philosophia',
        'technologia',
        'medicina',
        'coda',
    ]
    
    # Bead types (Magister roles)
    BEAD_TYPES = {
        'musica': {'name': 'Magister Musicae', 'color': '#00e5ff', 'icon': '♪'},
        'mathematica': {'name': 'Magister Mathematicae', 'color': '#ff00ff', 'icon': '∑'},
        'historia': {'name': 'Magister Historiae', 'color': '#ffd700', 'icon': '⌛'},
        'natura': {'name': 'Magister Naturae', 'color': '#00ff7f', 'icon': '⚛'},
        'lingua': {'name': 'Magister Linguae', 'color': '#ff6b6b', 'icon': '✎'},
        'philosophia': {'name': 'Magister Philosophiae', 'color': '#9370db', 'icon': '◊'},
        'technologia': {'name': 'Magister Technologiae', 'color': '#ffa500', 'icon': '⚙'},
        'medicina': {'name': 'Magister Medicinae', 'color': '#ff69b4', 'icon': '✚'},
        'coda': {'name': 'Magister Codae', 'color': '#39ff14', 'icon': '⌘'},
    }
    
    # Ranks
    RANKS = ['Novice', 'Adept', 'Scholar', 'Magister Ludi']
    
    # Scoring weights
    ELEGANCE_WEIGHT = 0.30
    FERTILITY_WEIGHT = 0.25
    SURPRISE_WEIGHT = 0.25
    RECURSION_WEIGHT = 0.20
    
    # Audio
    BASE_BPM = 60
    SEMITONE_BASE = 12
    
    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')
