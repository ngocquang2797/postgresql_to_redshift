from internal.http.handlers.migrate_db import MigrateData, ProfileInfo
from internal.routers.rest_plus import api, app


def __add_router(class_resource, name_space, url="", description='None'):
    ns = api.namespace(name_space, description=description)
    ns.add_resource(class_resource, url)
    api.add_namespace(ns)


def init_router():
    app.config["JSON_SORT_KEYS"] = False
    app.config['RESTPLUS_VALIDATE'] = True
    __add_router(MigrateData, name_space='database/migrate', description='migrate data table from pg to rds')
    __add_router(ProfileInfo, name_space='database/info',
                 description='get all profile, return [{"id": "id of profile", "name":"name of profile"}]')
