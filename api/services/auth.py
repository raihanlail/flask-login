from flask import jsonify
from http import HTTPStatus
from api.utils.firebase import auth, db
from api.models.user import User
from api.schemas.auth import LoginSchema, SignupSchema
import jwt
import datetime
from flask import current_app 
from pydantic import ValidationError

class AuthService:
    def login(self, data: dict) -> tuple[dict, int]:
        try:
            schema = LoginSchema(**data)
        except ValidationError as e:
            return jsonify({'status': 'error', 'message': e.errors()}), HTTPStatus.BAD_REQUEST
        
        try:
            user = auth.sign_in_with_email_and_password(
                schema.email, 
                schema.password,
            )
            user_id = user['localId']

            db.child("users").child(user_id).update({
            "last_login": {".sv": "timestamp"}
            })

            user_obj = User.get_by_id(user_id)
            
            if not user_obj:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found in database'
                }), HTTPStatus.NOT_FOUND
            
            token = jwt.encode({
                'user_id': user_id,
                'email': user_obj.email,
                'exp': datetime.datetime.now() + datetime.timedelta(days=1)
            }, current_app.config['SECRET_KEY'])
            
            return jsonify({
                'status': 'success',
                'data': {
                    'access_token': token,
                    'token_type': 'Bearer',
                    'user': {
                        'user_id': user_id,
                        'email': user_obj.email,
                        'username': user_obj.username,
                        'last_login': user_obj.last_login,

                    }
                }
            }), HTTPStatus.OK
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Invalid credentials'
            }), HTTPStatus.UNAUTHORIZED


    def signup(self, data: dict) -> tuple[dict, int]:
        try:
            schema = SignupSchema(**data)
        except ValidationError as e:
            return jsonify({'status': 'error', 'message': e.errors()}), HTTPStatus.BAD_REQUEST

        try:
            user = auth.create_user_with_email_and_password(
                schema.email, 
                schema.password,
            )
            user_id = user['localId']
            
            user_data = {
                "username": schema.username,
                "email": schema.email,
                "created_at": {".sv": "timestamp"},
                "last_login": {".sv": "timestamp"}
            }
            
            db.child("users").child(user_id).set(user_data)
            
            return jsonify({
                'status': 'success',
                'message': 'User created successfully'
            }), HTTPStatus.CREATED
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), HTTPStatus.BAD_REQUEST
        
    def get_current_user(self, token: str) -> tuple[dict, int]:
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.get_by_id(payload['user_id'])
            
            return jsonify({
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'history': user.search_history
                }
            }), HTTPStatus.OK
            
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
                

    def logout(self, token: str) -> tuple[dict, int]:
        try:
            return jsonify({
                'status': 'success',
                'message': 'Token invalidated successfully'
            }), HTTPStatus.OK
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Error during logout'
            }), HTTPStatus.BAD_REQUEST

    