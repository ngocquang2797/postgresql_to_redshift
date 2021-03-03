import datetime
from typing import Tuple

import jwt
from itsdangerous import (BadSignature)
from werkzeug.security import check_password_hash

from internal.entities.user import User
from internal.services.user_service import UserService


class AuthService(object):
    user_service = None

    def __init__(self, user_service: UserService):
        self.access_token = None
        self.user_service = user_service

    def authenticate(self, email: str, password: str) -> Tuple[bool, str]:
        user = self.user_service.get_by_email(email)
        if user is None:
            return False, "user is not existed."

        if check_password_hash(user['password'], password) is False:
            return False, "email or password is not correct. Please try again"

        token = self.__generate_auth_token(user)
        return True, token

    @staticmethod
    def __generate_auth_token(user: User):
        """Generate an API auth token for user."""
        print(user)
        token = jwt.encode(
            {'user_id': str(user['_id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            "secret", algorithm="HS256")
        return token

    def verify_auth_token(self, access_token: str) -> Tuple[bool, str, dict]:
        """Check that user API token is correct."""
        split_token = access_token.split()
        if len(split_token) != 2:
            return False, 'invalid token', {}

        if split_token[0] != 'Bearer':
            return False, 'invalid token', {}

        token = split_token[1]
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False, 'Token has been expired. Please log in again.', {}
        except jwt.InvalidTokenError:
            return False, 'Invalid token. Please log in again.', {}
        except BadSignature:
            return False, 'invalid token', {}

        user = self.user_service.get_by_id(data['user_id'])
        return True, 'success', user
