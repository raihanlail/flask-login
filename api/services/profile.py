from flask import jsonify
from http import HTTPStatus
from api.utils.firebase import auth, db
from api.models.user import User
from api.schemas.profile import EditProfileSchema
import jwt
import datetime
from flask import current_app 
from pydantic import ValidationError

class ProfileService:
    def get_current_user(self, token: str) -> tuple[dict, int]:
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Token is missing'
            }), HTTPStatus.UNAUTHORIZED
            
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.get_by_id(payload['user_id'])
            
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), HTTPStatus.NOT_FOUND
            
            return jsonify({
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username,
                    
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
    
    def edit_user(self, token: str, data: dict) -> tuple[dict, int]:
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Token is missing'
            }), HTTPStatus.UNAUTHORIZED
            
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), HTTPStatus.BAD_REQUEST
            
        try:
            schema = EditProfileSchema(**data)
        except ValidationError as e:
            return jsonify({'status': 'error', 'message': str(e.errors())}), HTTPStatus.BAD_REQUEST
            
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            
            # Check if user exists
            existing_user = User.get_by_id(user_id)
            if not existing_user:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), HTTPStatus.NOT_FOUND
            
            edited_user = {
                'username': schema.username,
                'email': schema.email,
            }
            
            # Update user data in Firebase
            db.child("users").child(user_id).update(edited_user)
            
            # Get updated user
            updated_user = User.get_by_id(user_id)
            
            return jsonify({
                'status': 'success',
                'message': 'User updated successfully',
                'data': {
                    
                    'email': updated_user.email,
                    'username': updated_user.username
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
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), HTTPStatus.BAD_REQUEST