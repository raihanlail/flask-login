from functools import wraps
from flask import request, jsonify
from http import HTTPStatus
import jwt
from flask import current_app

def verify_token():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            auth_header = request.headers.get('Authorization')
            
            if auth_header:
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({
                        'status': 'error',
                        'message': 'Invalid token format'
                    }), HTTPStatus.UNAUTHORIZED
                    
            if not token:
                return jsonify({
                    'status': 'error',
                    'message': 'Token is missing'
                }), HTTPStatus.UNAUTHORIZED
                
            try:
                jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                
            except jwt.ExpiredSignatureError:
                return jsonify({
                    'status': 'error',
                    'message': 'Token has expired'
                }), HTTPStatus.UNAUTHORIZED
            except jwt.InvalidTokenError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid token'
                }), HTTPStatus.UNAUTHORIZED
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
