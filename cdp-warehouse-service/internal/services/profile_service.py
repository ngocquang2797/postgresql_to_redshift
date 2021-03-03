from internal.repositories.db import DBRepository


class ProfileService(object):
    def __init__(self):
        self.db_repo = DBRepository()

    def profile_info(self):
        return True, self.db_repo.get_all_profile()
