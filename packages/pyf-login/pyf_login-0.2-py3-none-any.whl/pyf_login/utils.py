import hashlib


def calculate_md5(username, password):
    data = ":".join([username, "Piehouse", password])
    hash_object = hashlib.md5(data.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


class MyJsonResponse:
    def __init__(self):
        self.data = {"msg": "", "code": 0, "data": {}}

    def update(self, msg=None, code=None, data=None):
        if msg:
            self.data["msg"] = msg
        if code:
            self.data["code"] = code
        if data:
            self.data["data"] = data
