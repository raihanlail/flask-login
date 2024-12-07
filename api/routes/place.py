from flask import Blueprint, request, jsonify
from typing import Tuple, Dict, List
from http import HTTPStatus
from api.services.places import PlacesService

places_bp = Blueprint('places', __name__)
places_service = PlacesService()

@places_bp.route('/<string:place_id>', methods=['GET'])
def get_place(place_id: str):
    return places_service.get_place_by_id(place_id)

@places_bp.route('/', methods=['GET'])
def get_all_places():
    return jsonify(places_service.get_places())

@places_bp.route('/category/<string:category>', methods=['GET'])
def get_places_by_category(category: str):
    return jsonify(places_service.get_places_by_category(category))