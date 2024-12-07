from typing import Optional, List, Dict
from datetime import datetime
from api.utils.firebase import db

class Places:
    def __init__(
        self,
        place_id: str,
        name: str,
        tourism: str,
        coordinates: List[float],
        images: List[str],
        geometry_type: str,
        type: str,
        historic: str = None,
        landmark: str = None,
        natural: str = None,
        city: str = None,
        housenumber: str = None,
        postcode: str = None,
        street: str = None,
        opening_hours: str = None,
        website: str = None,
        phone: str = None,
        avg_rating: float = None
    ) -> None:
        self.id = place_id
        self.name = name
        self.tourism = tourism
        self.coordinates = coordinates
        self.images = images
        self.geometry_type = geometry_type
        self.type = type
        self.historic = historic
        self.landmark = landmark
        self.natural = natural
        self.city = city
        self.housenumber = housenumber
        self.postcode = postcode
        self.street = street
        self.opening_hours = opening_hours
        self.website = website
        self.phone = phone
        self.avg_rating = avg_rating

    @staticmethod
    def _create_from_data(place_data: Dict, place_id: str = None) -> 'Places':
        """
        Helper method to create Places object from database data
        """
        ratings_data = db.child("ratings").child(place_data.get('id')).get('rating').val()
        avg_rating = None
        if ratings_data:
            total_rating = 0
            num_ratings = 0
            for rating in ratings_data.values():
                total_rating += rating.get('rating', 0)
                num_ratings += 1
            if num_ratings > 0:
                avg_rating = total_rating / num_ratings

        return Places(
            place_id=place_data.get('id'),
            name=place_data['properties'].get('name'),
            tourism=place_data['properties'].get('tourism'),
            coordinates=place_data['geometry'].get('coordinates', []),
            images=place_data['properties'].get('images', []),
            geometry_type=place_data['geometry'].get('type'),
            historic=place_data['properties'].get('historic', None),
            landmark=place_data['properties'].get('landmark', None),
            natural=place_data['properties'].get('natural', None),
            city=place_data['properties'].get('addr:city', None),
            housenumber=place_data['properties'].get('addr:housenumber', None),
            postcode=place_data['properties'].get('addr:postcode', None),
            street=place_data['properties'].get('addr:street', None),
            opening_hours=place_data['properties'].get('opening_hours', None),
            website=place_data['properties'].get('website', None),
            phone=place_data['properties'].get('phone', None),
            type=place_data.get('type'),
            avg_rating=avg_rating
        )

    @staticmethod
    def get_by_id(place_id: str) -> Optional['Places']:
        """
        Fetches a Place object from the database using its ID.
        Args:
            place_id: The unique identifier of the feature
        Returns:
            place object if found, None otherwise
        """
        places_data = db.child("places").child(place_id).get().val()
        return Places._create_from_data(places_data) if places_data else None

    @staticmethod
    def get_all() -> List['Places']:
        """
        Fetches all places from the database.
        Returns:
            List of Places objects
        """
        places_data = db.child("places").get().val()
        places_list = []
        if places_data:
            for place_id, place_data in places_data.items():
                places_list.append(Places._create_from_data(place_data))
        return places_list

    @staticmethod
    def get_places_by_category(category:str) -> List['Places']:
        """
        Fetches all places from the database where natural attribute is not null.
        Returns:
            List of Places objects with natural attributes
        """
        places_data = db.child("places").get().val()
        places_list = []
        if places_data:
            for place_id, place_data in places_data.items():
                if place_data['properties'].get(category):
                    places_list.append(Places._create_from_data(place_data))
        return places_list

    def to_dict(self) -> Dict:
        """
        Converts the Feature object to a dictionary representation.
        Returns:
            A dictionary representation of the Feature.
        """
        return {
            "id": self.id,
            "properties": {
                "name": self.name,
                "tourism": self.tourism,
                "images": self.images,
                "historic": self.historic,
                "landmark": self.landmark,
                "natural": self.natural,
                "city": self.city,
                "housenumber": self.housenumber,
                "postcode": self.postcode,
                "street": self.street,
                "opening_hours": self.opening_hours,
                "website": self.website,
                "phone": self.phone,
            },
            "geometry": {
                "coordinates": self.coordinates,
                "type": self.geometry_type
            },
            "type": self.type,
            "avg_rating": self.avg_rating
        }