import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restx import Resource
from werkzeug.exceptions import (
    BadRequest
)

from internal.db.mongo_connector import Mongo
from internal.http.request.auth.login_request import LoginValidator
from internal.http.request.request import get_json_body
from internal.repositories.user import UserRepository
from internal.services.auth import AuthService
from internal.services.user_service import UserService


class LoginHandler(Resource):
    user_repo = None
    auth_service = None
    user_service = None

    def __init__(self) -> None:
        self.di()

    def di(self):
        self.user_repo = UserRepository(Mongo.get_instance())
        self.user_service = UserService(self.user_repo)
        self.auth_service = AuthService(self.user_service)

    def post(self):
        _, request_body = get_json_body(request)

        validator = LoginValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": "Bad request"})

        password = payload['password']
        email = payload['email']

        is_ok, token = self.auth_service.authenticate(email, str(password))
        if is_ok is False:
            return jsonify(
                {"errors": "email or password is not valid", "status": BadRequest.code, "message": "Bad request"})

        return jsonify({"data": json.loads(json_util.dumps({"token": token})), "status": status.HTTP_200_OK,
                        "message": "login successfully"})
