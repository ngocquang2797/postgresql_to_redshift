from internal.repositories.db import MigrateDBRepository


class MigrateDBService(object):
    def __init__(self):
        self.db_repo = MigrateDBRepository()

    def migrate_sv(self, keyword):
        tb_names = self.db_repo.get_table_name(keyword)
        if tb_names == []:
            return False, "Id not found"
        else:
            for tb in tb_names:
                print(tb)
                self.db_repo.migrate_db_to_rds(tb)

            return True, "Migrated successfully"

    def migrate_all_db(self):
        for tb in self.db_repo.get_all_table_names():
            print(tb)
            self.db_repo.migrate_db_to_rds(tb)

        return True, "Migrated successfully"
