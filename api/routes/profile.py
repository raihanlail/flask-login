from flask import Blueprint, request
from typing import Tuple, Dict
from api.services.profile import ProfileService

from api.middlewares.auth import verify_token

profile_bp = Blueprint('profile', __name__)
profile_service = ProfileService()
    
@profile_bp.route('/me', methods=['GET'])
@verify_token()
def get_current_user() -> Tuple[Dict, int]:
    token = request.headers.get('Authorization').split(" ")[1]
    return profile_service.get_current_user(token)

@profile_bp.route('/edit', methods=['PATCH'])
@verify_token()
def edit_user() -> Tuple[Dict, int]:
    token = request.headers.get('Authorization').split(" ")[1]
    data = request.get_json()
    return profile_service.edit_user(token, data)