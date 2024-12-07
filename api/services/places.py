from api.models.places import Places
from api.utils.firebase import db
from typing import List
from http import HTTPStatus
from flask import jsonify

class PlacesService:
    def get_places(self) -> List[dict]:
        places_data = Places.get_all()
        return [Places.to_dict(place) for place in places_data]

    def get_place_by_id(self, place_id: str) -> dict:
        place_data = Places.get_by_id(place_id)
        if not place_data:
            return jsonify({'message': 'Place not found'}), HTTPStatus.NOT_FOUND
        if place_data:
            return jsonify(Places.to_dict(place_data))
        return None
    
    def get_places_by_category(self, category:str) -> List[dict]:
        category_places = Places.get_places_by_category(category)
        if not category_places:
            return jsonify({'message': 'Places not found'}), HTTPStatus.NOT_FOUND
        if category_places:
             return [Places.to_dict(place) for place in category_places]