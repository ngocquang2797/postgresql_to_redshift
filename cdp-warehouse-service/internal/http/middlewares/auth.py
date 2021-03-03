"""Authentication utilities needed by API."""

from functools import wraps

from flask import request
from werkzeug.exceptions import (
    Forbidden,
    Unauthorized
)

from internal.db.mongo_connector import Mongo
from internal.repositories.user import UserRepository
from internal.services.auth import AuthService
from internal.services.user_service import UserService


def get_access_token():
    access_token: str
    try:
        access_token = request.headers.get('Authorization')
    except KeyError:
        return {"message": "Authentication token is missing."}, Unauthorized.code

    return access_token


def auth(f):
    """
    Perform token based authentication.
    Token is supposed to be passed in headers.
    If found, decrypt token and get matching user.
    If no token in header or user not found, return an error message.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = get_access_token()
        is_valid, msg, user = verify_token(access_token)

        if not user:
            return {"message": msg}, Unauthorized.code

        return f(*args, **kwargs)

    return decorated


def is_admin(f):
    """
    Check if user is premium.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """Use this decorator on API endpoints restricted to admin users."""
        access_token = get_access_token()
        is_valid, msg, user = verify_token(access_token)
        if not user:
            return {"message": msg}, Unauthorized.code

        if user['role'] != 'admin':
            return {"message": Forbidden.description}, Forbidden.code

        return f(*args, **kwargs)

    return decorated


def has_roles(allowed_roles: list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # print("has roles: ", allowed_roles)
            access_token = get_access_token()
            is_valid, msg, user = verify_token(access_token)

            if not user:
                return {"message": msg}, Unauthorized.code
            if user['role'] not in allowed_roles:
                return {"message": Forbidden.description}, Forbidden.code

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def verify_token(auth_token: str):
    user_repo = UserRepository(Mongo.get_instance())
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)

    return auth_service.verify_auth_token(auth_token)
