"""
Flask Application Factory
"""

from flask import Flask


def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config['SECRET_KEY'] = 'fraud_detection_secret_key_2024'
    app.config['DEBUG'] = True
    
    return app
