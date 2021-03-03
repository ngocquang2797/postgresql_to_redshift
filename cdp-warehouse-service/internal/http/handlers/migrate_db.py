from flask import jsonify, request, make_response
from flask_api import status
from flask_restx import Resource, fields
from werkzeug.exceptions import (
    BadRequest
)
from internal.routers.rest_plus import api
from internal.http.request.request import get_json_body
from internal.http.request.migratedb import MigrateValidator
from internal.services.migrate_service import MigrateDBService
from internal.services.profile_service import ProfileService


class _PayloadMigrateData:
    @staticmethod
    def get_payload_for_post():
        return api.model('Payload for MigrateData post',
                         {'id': fields.String(example='25258af3-b726-4027-a1db-07f66a2613f9')})


class MigrateData(Resource):

    def __init__(self, *ak, **kwargs):
        super().__init__(*ak, **kwargs)
        self.di()

    def di(self):
        self.migrate_service = MigrateDBService()

    @api.expect(_PayloadMigrateData.get_payload_for_post(), validate=True)
    def post(self):
        _, request_body = get_json_body(request)

        is_ok = False

        validator = MigrateValidator(request_body)

        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        if request_body == {}:
            is_ok, self.message = self.migrate_service.migrate_all_db()
        else:
            is_ok, self.message = self.migrate_service.migrate_sv(request_body['id'])

        if is_ok:
            return jsonify({"status": status.HTTP_200_OK,
                            "message": self.message})

        else:
            return make_response(jsonify({"message": self.message}), BadRequest.code)


class ProfileInfo(Resource):
    def __init__(self, *ak, **kwargs):
        super().__init__(*ak, **kwargs)
        self.di()

    def di(self):
        self.profile_service = ProfileService()

    def get(self):
        is_ok, data = self.profile_service.profile_info()
        if is_ok:
            return jsonify({"data": data})
        else:
            return jsonify({"status": status.HTTP_200_OK,
                            "data": data})
