from flask import Flask
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from api.routes.auth import auth_bp
from api.routes.profile import profile_bp
from api.routes.place import places_bp
from api.routes.ratings import ratings_bp
from flask_cors import CORS

session = Session()

def create_app(config_file: str = '../config.py') -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile(config_file)
    app.secret_key = app.config['SECRET_KEY']
    
    session.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(places_bp, url_prefix='/places') 
    app.register_blueprint(ratings_bp, url_prefix='/ratings')

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    return app
