import sqlalchemy as SA


class pgClient():

    def __init__(self, user, pwd, host, port, db):
        self.pg_url = 'postgresql://{}:{}@{}:{}/{}'.format(user, pwd, host, port, db)

        self.__pg_client = SA.create_engine(self.pg_url)

    def get_instance(self):
        return self.__pg_client


class rdsClient():

    def __init__(self, user, pwd, host, port, db):
        'redshift+psycopg2://{}:{}@{}:{}/{}'.format(user, pwd, host, port, db)
        rds_url = 'redshift+psycopg2://{}:{}@{}:{}/{}'.format(user, pwd, host, port, db)
        # 'redshift+psycopg2://paul:FnRb7fV44xTtB8fmbL5Zk5Zw7@cdp-data-warehouse-dev.cfynz0uf7qqb.ap-southeast-1.redshift.amazonaws.com:5439/main'

        self.__rds_client = SA.create_engine(rds_url)

    def get_instance(self):
        return self.__rds_client
