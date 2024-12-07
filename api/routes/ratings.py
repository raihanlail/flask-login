
from flask import Blueprint, request, jsonify
from typing import Tuple, Dict
from http import HTTPStatus
from api.services.ratings import RatingsService
from api.middlewares.auth import verify_token
from api.models.ratings import Ratings

ratings_bp = Blueprint('ratings', __name__)
ratings_service = RatingsService()

@ratings_bp.route('/details/<string:place_id>', methods=['GET'])
def get_rating_by_place_id(place_id: str) -> Tuple[Dict, HTTPStatus]:
    return ratings_service.get_rating_by_place_id(place_id)

@ratings_bp.route('/<string:place_id>', methods=['POST'])
@verify_token()
def add_rating(place_id: str) -> Tuple[Dict, HTTPStatus]:
    token = request.headers.get('Authorization').split(" ")[1]
    rating = request.json.get('rating')
    return ratings_service.add_rating(token, place_id, rating)