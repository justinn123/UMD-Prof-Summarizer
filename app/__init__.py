from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        # Import routes or other modules here
        from . import routes
    return app