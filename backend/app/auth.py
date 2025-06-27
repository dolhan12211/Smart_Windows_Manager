import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify, current_app

# For demonstration purposes, a simple hardcoded user.
# In a real application, this would come from a database.
USERS = {
    "admin": {
        "password_hash": generate_password_hash("adminpass"),
        "roles": ["admin"]
    },
    "testuser": { # Added test user
        "password_hash": generate_password_hash("testpass"),
        "roles": ["user"]
    }
}

# Secret key for JWT. In a real application, this should be loaded from environment variables.
SECRET_KEY = "your_super_secret_jwt_key" # TODO: Load from environment variable

def create_token(username):
    """
    Creates a JWT token for the given username.
    """
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 minutes
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    """
    Verifies a JWT token and returns the decoded payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def authenticate_user(username, password):
    """
    Authenticates a user against the stored credentials.
    """
    user = USERS.get(username)
    if user and check_password_hash(user["password_hash"], password):
        return True
    return False

def register_user(username, password):
    """
    Registers a new user.
    """
    if username in USERS:
        return False, "User already exists"
    
    USERS[username] = {
        "password_hash": generate_password_hash(password),
        "roles": ["user"] # Default role for new users
    }
    return True, "User registered successfully"

def token_required(f):
    """
    Decorator to protect API endpoints, requiring a valid JWT token.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for 'x-access-token' in headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # If not in headers, check for 'Authorization' header with 'Bearer' prefix
        elif 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = verify_token(token)
            if "error" in data:
                return jsonify({"message": data["error"]}), 401
            current_user = data['username']
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

if __name__ == '__main__':
    # Example usage:
    test_username = "admin"
    test_password = "adminpass"

    if authenticate_user(test_username, test_password):
        print(f"User '{test_username}' authenticated successfully.")
        token = create_token(test_username)
        print(f"Generated Token: {token}")

        decoded_payload = verify_token(token)
        print(f"Decoded Payload: {decoded_payload}")

        # Simulate expired token
        expired_token_payload = {
            "username": test_username,
            "exp": datetime.utcnow() - timedelta(minutes=1),
            "iat": datetime.utcnow()
        }
        expired_token = jwt.encode(expired_token_payload, SECRET_KEY, algorithm="HS256")
        print(f"Expired Token: {expired_token}")
        print(f"Verification of expired token: {verify_token(expired_token)}")
    else:
        print(f"Authentication failed for '{test_username}'.")
