from flask import Flask
from flask_caching import Cache
from config import Config

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    cache.init_app(app)
    
    with app.app_context():
        # Import routes or other modules here
        from . import routes
    return app