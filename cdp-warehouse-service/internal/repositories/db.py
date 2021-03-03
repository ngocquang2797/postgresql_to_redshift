from internal.db.database_connector import Postgres, Redshift
import pandas.io.sql as sqlio
import psycopg2
from sqlalchemy import MetaData
import sqlalchemy


class DBRepository:
    def __init__(self):
        self.engine = Postgres().get_engine_folow()

    def get_all_profile(self):
        pg_conn1 = self.engine.connect()
        try:
            querry = "select name, id from profile_table"
            df = sqlio.read_sql_query(querry, pg_conn1)
            return df.to_dict('records')

        except psycopg2.OperationalError:
            print('OperationalError!!!!')
            pass

        finally:
            self.engine.dispose()


class MigrateDBRepository:
    def __init__(self):
        self.engine = Postgres().get_engine_folow()
        self.engine_transform_data = Postgres().get_engine_transform()
        self.engine_source = Redshift().get_engine()

    def migrate_db_to_rds(self, tb_name):
        src_conn = self.engine_transform_data.connect()

        dst_conn = self.engine_source.connect()
        try:
            df = sqlio.read_sql_table(tb_name, src_conn, schema='public')

            text_field = self.check_type(tb_name)

            df.to_sql(tb_name, dst_conn,
                      schema='public',
                      index=False,
                      if_exists='append',
                      method='multi',
                      dtype=text_field)

        except psycopg2.OperationalError:
            print('OperationalError!!!!')
            pass

        finally:
            self.engine_transform_data.dispose()
            self.engine_source.dispose()

    def get_table_name(self, id):
        pg_conn1 = self.engine.connect()
        try:
            querry = """select meta_name from meta
                        where id in (
                            select meta_id from destination
                            where id in (
                                select destination_field_id from profile_match_rule
                                where profile_field_id in (
                                    select id from profile_table_field
                                    where profile_table_id = '{0}')))""".format(id)

            # query flow 1
            df1 = sqlio.read_sql_query(querry, pg_conn1)
            list_name = list(dict.fromkeys(df1.to_numpy().flatten()))
            # query flow 2
            df2 = sqlio.read_sql_query("""select name from profile_table where id = '{0}'""".format(id), pg_conn1)
            for n in list(dict.fromkeys(df2.to_numpy().flatten())):
                list_name.append(n)
            return list_name

        except psycopg2.OperationalError:
            print('OperationalError!!!!')
            pass

        finally:
            self.engine.dispose()

    def check_type(self, name):
        meta = MetaData(self.engine_transform_data, True)
        try:
            table = meta.tables[name]
            types = [[col.name, col.type] for col in table.columns]
            re = {}
            for ele in types:
                if type(ele[1]) == sqlalchemy.sql.sqltypes.TEXT:
                    re[ele[0]] = sqlalchemy.types.VARCHAR(length=65535)
                elif type(ele[1]) == sqlalchemy.dialects.postgresql.UUID:
                    re[ele[0]] = sqlalchemy.types.VARCHAR(length=128)
                else:
                    re[ele[0]] = ele[1]

            return re

        except psycopg2.OperationalError:
            print('OperationalError!!!!')
            pass

    def get_all_table_names(self):
        return self.engine_transform_data.table_names()
