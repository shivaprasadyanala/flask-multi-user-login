import jwt
from flask import request, jsonify
from .models import User
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            response = jsonify(
                {"message": "No authentication credentials are provided"})
            response.status_code = 401
            return response
        try:
            data = jwt.decode(token, os.environ.get(
                'SIGNING_KEY'), algorithms=['HS256'])
            print(data)
            current_user = User.query.filter_by(id=data['id']).first()

        except Exception as error:
            response = jsonify(
                {"message": "invalid token", "erro": str(error)})
            response.status_code = 401
            return response
        return f(current_user, *args, **kwargs)
    return decorated


def requires_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract the JWT from the request header
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
                if not token:
                    response = jsonify(
                        {"message": "No authentication credentials are provided"})
                    response.status_code = 401
                    return response
                try:
                    data = jwt.decode(token, 'secret_key',
                                      algorithms=['HS256'])
                    print(data)
                    if data['role'] != permission:
                        print("hi")
                        response = jsonify(
                            {"message": "invalid credentails"})
                        response.status_code = 401
                        return response
                    current_user = User.query.filter_by(id=data['id']).first()

                except Exception as error:
                    response = jsonify(
                        {"message": "invalid token", "erro": str(error)})
                    response.status_code = 401
                    return response
                # If the user has the required permission, allow them to access the route or resource
                return f(*args, **kwargs)
        return decorated_function
    return decorator
