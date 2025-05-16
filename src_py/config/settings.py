"""
Configuration settings for the AgentVerse platform.
"""
import os

# Application configuration
APP_CONFIG = {
    'title': 'AI Agent Bounty Platform',
    'icon': '🤖',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'version': '0.1.0',
    'name': 'AgentVerse',
    'description': 'A decentralized marketplace for AI agents',
    'year': '2024',
}

# User interface configuration
UI_CONFIG = {
    'css': """
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-radius: 4px 4px 0 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .bounty-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        color: #721c24;
        margin: 1rem 0;
    }
    </style>
    """,
    'colors': {
        'primary': '#4CAF50',
        'secondary': '#2196F3',
        'accent': '#FF9800',
        'success': '#4CAF50',
        'warning': '#FFC107',
        'error': '#F44336',
        'text': '#212121',
        'background': '#FFFFFF',
    }
}

# Model rewards configuration
MODEL_REWARDS = {
    "Microsoft Phi-3-mini (3.8B)": 100,
    "Microsoft Phi-3-small (7B)": 80,
    "Google Gemma 2B": 120,
    "Google Gemma 7B": 70,
    "Mistral 7B": 70,
    "StableLM 2B": 120,
    "StableLM 3B": 100,
    "Qwen 0.5B": 150,
    "Qwen 1.5B": 130,
    "Qwen 4B": 90,
    "Qwen 7B": 70,
}

# Reward categories
REWARD_CATEGORIES = {
    "0.5B-2B": (120, 150),
    "3B-4B": (90, 100),
    "7B": (70, 80),
}

# Environment variables (managed by dotenv in app.py)
def get_env_var(name, default=None):
    """Get environment variable with optional default value"""
    return os.environ.get(name, default) 