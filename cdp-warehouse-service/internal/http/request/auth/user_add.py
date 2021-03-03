from validator import validate


class AddUserValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            "password": "required",
            "password_confirmation": "required",
            "role": "required",
            "email": "required|mail"
        }
        return rules

    def validate(self, payload: dict):
        rules = self.__get_rules()
        return validate(payload, rules, return_info=True)
