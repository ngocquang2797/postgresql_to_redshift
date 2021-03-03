import os

from flask import Blueprint
from internal.routers.rest_plus import api, app
from internal.routers.routes import init_router


def init_app():
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    init_router()
    app.register_blueprint(blueprint)

    return app


if __name__ == '__main__':
    init_app()
    host = os.environ.get("HOST", "0.0.0.0")
    port = os.environ.get("PORT", 3001)
    debug = os.environ.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)
