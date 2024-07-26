from flask import request
from shared_kernel.auth import JWTTokenHandler
from shared_kernel.config import Config
from shared_kernel.exceptions import Unauthorized

config = Config()
token_handler = JWTTokenHandler(config.get('JWT_SECRET_KEY'))


# Decorator to protect routes
def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')

        if not token:
            raise Unauthorized('Token is missing!')

        payload = token_handler.decode_token(token)
        if 'error' in payload:
            raise Unauthorized("Failed to parse token")

        # Add user information to the request context
        current_user = {
            "user_id": payload['user_id'],
            "org_id": payload['org_id']
        }
        return f(current_user, *args, **kwargs)

    return decorator
