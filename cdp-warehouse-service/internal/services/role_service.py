from datetime import datetime
from typing import Tuple, Type

from internal.entities.role import Role, ROLE_STATUS_ACTIVE
from internal.repositories.role import RoleRepository


class RoleService(object):
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def add_role(self, role: Role) -> Tuple[bool, Type[Role], str]:
        existed_role = self.get_by_code(role.name)
        if existed_role:
            return False, Role, "The role name was taken. Please set other role"

        now = datetime.now()
        role.created_at = now
        role.updated_at = now
        role.status = ROLE_STATUS_ACTIVE

        return True, self.role_repo.create(role), "Created new role successfully"

    def update_role(self, role: Role):
        return self.role_repo.create(role)

    def delete_role(self, role_id: str):
        return self.role_repo.delete(role_id)

    def get_by_code(self, code: str) -> dict:
        return self.role_repo.get_by_code(code)

    def get_by_id(self, role_id: str) -> dict:
        return self.role_repo.get(role_id)
