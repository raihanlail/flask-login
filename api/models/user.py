from flask_login import UserMixin
from typing import Optional, List
from api.utils.firebase import db
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_id: str, username: str, email: str, avatar:str, created_at: int = None, last_login: int = None, search_history: List[str] = None) -> None:
        self.id = user_id
        self.username = username
        self.email = email
        self.avatar = avatar
        self.created_at = datetime.fromtimestamp(created_at/1000) if created_at else None
        self.last_login = datetime.fromtimestamp(last_login/1000) if last_login else None
      
    
    @staticmethod
    def get_by_id(user_id: str) -> Optional['User']:
        """
        Args:
            user_id: The unique identifier of the user 
        Returns:
            User object if found, None otherwise
        """
        user_data = db.child("users").child(user_id).get().val()
        if user_data:
            return User(
                user_id=user_id,
                username=user_data.get('username'),
                email=user_data.get('email'),
                avatar=user_data.get('avatar'),
                created_at=user_data.get('created_at'),
                last_login=user_data.get('last_login'),
                search_history=user_data.get('search_history', [])
            )
        return None