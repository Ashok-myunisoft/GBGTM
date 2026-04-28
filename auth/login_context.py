import json


def parse_login(login_dto):

    if isinstance(login_dto, dict):
        return login_dto

    if isinstance(login_dto, str):
        return json.loads(login_dto)

    raise Exception("Invalid login_dto")