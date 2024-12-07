# Flask Firebase Authentication API

A secure REST API implementing token-based authentication using Flask, Firebase Authentication, and JWT tokens.

## Features

- Token-based authentication with JWT
- Firebase Authentication and Realtime Database integration
- Rate limiting protection (200/day, 50/hour)
- Input validation using Pydantic schemas
- Secure password requirements
- User session tracking
- CORS support
- Security headers

## Tech Stack

- Flask
- Firebase Authentication
- Firebase Realtime Database
- PyJWT
- Pydantic
- Flask-Limiter
- Flask-CORS
- Pyrebase

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```
2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements
```
4. Create a `.env` file in the root directory and add your Firebase configuration
```bash
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here
# Firebase Config
API_KEY=your-api-key
AUTH_DOMAIN=your-auth-domain
PROJECT_ID=your-project-id
STORAGE_BUCKET=your-storage-bucket
MSG_ID=your-messaging-sender-id
APP_ID=your-app-id
MEASURE_ID=your-measurement-id
DB_URL=your-database-url
```
5. Run the application
```bash
flask -app app run # or python app.py
```
```bash
# To run in debug mode
flask --app app run --debug
```

## Avaliable Routes (Authentication)
- `POST /auth/login` - User Login
- `POST /auth/signup` - User Registration
- `GET /auth/me` - Get Current User Profile
- `POST /auth/logout` - User Logout

## Available Routes (User)
- `GET /profile/me` - Get Current User Profile
- `PATCH /profile/edit` - Edit Current User Profile

## Available Routes (Places)
- `GET /places` - Get All Places
- `GET /places/{place_id}` - Get Place by ID
- `GET /places/category/{category}` - Get Places by Category. avaliable category(natural, historic, landmark, amenity, religion, waterway, sport)

## Sample Responses
```json
 {
        "avg_rating": null,
        "geometry": {
            "coordinates": [
                115.6028731,
                -8.2837348
            ],
            "type": "Point"
        },
        "id": "node/12052475969",
        "properties": {
            "city": null,
            "historic": null,
            "housenumber": null,
            "images": [
                "https://images.unsplash.com/photo-1535186830872-2c5fe5cc62fb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2NzgyNDJ8MHwxfHNlYXJjaHwxfHxhdHRyYWN0aW9ufGVufDB8fHx8MTczMjM4NDk2Mnww&ixlib=rb-4.0.3&q=80&w=400",
                "https://images.unsplash.com/photo-1416397202228-6b2eb5b3bb26?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2NzgyNDJ8MHwxfHNlYXJjaHwyfHxhdHRyYWN0aW9ufGVufDB8fHx8MTczMjM4NDk2Mnww&ixlib=rb-4.0.3&q=80&w=400",
                "https://images.unsplash.com/photo-1577378664765-388cda96aff7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2NzgyNDJ8MHwxfHNlYXJjaHwzfHxhdHRyYWN0aW9ufGVufDB8fHx8MTczMjM4NDk2Mnww&ixlib=rb-4.0.3&q=80&w=400"
            ],
            "landmark": null,
            "name": "Emerald",
            "natural": null,
            "postcode": null,
            "street": null,
            "tourism": "attraction"
        },
        "type": "Feature"
    },
    ```
## Firebase Setup
1.  Create a Firebase project in the Firebase Console
1. Enable Email/Password authentication
1. Create a Realtime Database
1. Copy the configuration details to your `.env` file