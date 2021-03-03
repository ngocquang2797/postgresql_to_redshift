import os

from sqlalchemy import create_engine, engine


class Postgres:
    __full_uri = None
    __database: engine = None

    def __init__(self):
        postgres_uri = os.environ.get("POSTGRES_URI")
        db_name = os.environ.get("POSTGRES_NAME")
        db_name_transform = os.environ.get("POSTGRES_NAME_TRANSFORM")
        self.__full_uri_folow = f"""postgresql://{postgres_uri}/{db_name}"""
        self.__full_uri_transform = f"""postgresql://{postgres_uri}/{db_name_transform}"""

    def get_engine_folow(self) -> engine:
        if self.__database is None:
            self.__database = create_engine(self.__full_uri_folow)
        return self.__database

    def get_engine_transform(self) -> engine:
        if self.__database is None:
            self.__database = create_engine(self.__full_uri_transform)
        return self.__database


class Redshift:
    __full_uri = None
    __database: engine = None

    def __init__(self):
        rds_uri = os.environ.get("RDS_URI")
        db_name = os.environ.get("RDS_NAME")
        self.__full_uri = f"""redshift+psycopg2://{rds_uri}/{db_name}"""

    def get_engine(self) -> engine:
        if self.__database is None:
            self.__database = create_engine(self.__full_uri)
        return self.__database
