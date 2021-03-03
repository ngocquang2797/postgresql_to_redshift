import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restx import Resource
from werkzeug.exceptions import (
    BadRequest
)

from internal.db.mongo_connector import Mongo
from internal.entities.user import User
from internal.http.request.auth.user_add import AddUserValidator
from internal.http.request.request import get_json_body, get_param
from internal.repositories.user import UserRepository
from internal.services.user_service import UserService


class AddUserHandler(Resource):
    user_repo = None
    user_service = None

    def __init__(self) -> None:
        self.di()

    def di(self):
        self.user_repo = UserRepository(Mongo.get_instance())
        self.user_service = UserService(self.user_repo)

    def post(self):
        _, request_body = get_json_body(request)

        validator = AddUserValidator(request_body)
        is_valid, _, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": "Bad request"})

        user = User(
            username=get_param('username', request_body),
            password=get_param('password', request_body),
            email=get_param('email', request_body),
            role=get_param('role', request_body),
            status=get_param('status', request_body),
        )

        is_ok, result, msg = self.user_service.add_user(user)
        if is_ok is False:
            return jsonify({"errors": str(msg), "status": BadRequest.code, "message": "Bad request"})

        return jsonify({"data": json.loads(json_util.dumps(result)), "status": status.HTTP_200_OK,
                        "message": "created user successfully"})
