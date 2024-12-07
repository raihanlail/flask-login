from flask import jsonify
from http import HTTPStatus
from api.utils.firebase import auth, db
from api.models.ratings import Ratings
from api.models.places import Places
from api.models.user import User
from api.middlewares.auth import verify_token
import jwt
from flask import current_app 

class RatingsService:
    def get_rating_by_place_id(self, place_id: str) -> tuple[dict, int]:
        ratings = Ratings.get_rating_by_place_id(place_id)
        if not ratings:
            return jsonify({
                'status': 'error',
                'message': 'Ratings not found'
            }), HTTPStatus.NOT_FOUND
        if ratings:
            return jsonify({
                'status': 'success',
                'data': {
                    'ratings': ratings
                }
            }), HTTPStatus.OK
        return None

    def add_rating(self, token: str, place_id: str, rating: int) -> tuple[dict, int]:
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Token is missing'
            }), HTTPStatus.UNAUTHORIZED

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']    
            name = payload.get('name', 'Anonymous')  # Gunakan default jika name tidak ada
            username = payload.get('username', 'anonymous')    
            add_ratings = Ratings.add_rating(place_id, user_id, name, username, rating) 
            if not add_ratings:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to add rating'
                }), HTTPStatus.INTERNAL_SERVER_ERROR
            if add_ratings:
                 return jsonify({
                    'status': 'success',
                    'message': 'Rating added successfully'
                 }), HTTPStatus.CREATED
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