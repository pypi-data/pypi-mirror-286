import jwt
import logging
from datetime import datetime
from django.conf import settings
from django.db.models import Model
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError


class JwtToken:

    def __init__(self) -> None:
        self.key = settings.JWT_SETTINGS["SIGNING_KEY"]
        self.algrithms = settings.JWT_SETTINGS["ALGORITHMS"]
        self.algrithm = settings.JWT_SETTINGS["ALGORITHMS"][0]
        self.header_type = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]
        self.header_name = settings.JWT_SETTINGS["AUTH_HEADER_NAME"]
        self.options = {
            "verify_signature": settings.JWT_SETTINGS["VERIFY_SIGNATURE"],
            "verify_exp": settings.JWT_SETTINGS["VERIFY_EXP"],
            "require": settings.JWT_SETTINGS["REQUIRE"],
        }

    def encode(self, payload: dict) -> str:
        tmp = {
            "exp": datetime.utcnow() + settings.JWT_SETTINGS["ACCESS_TOKEN_LIFETIME"]
        }
        payload.update(tmp)
        return jwt.encode(payload=payload, key=self.key, algorithm=self.algrithm)

    def decode(self, s: str) -> tuple:
        try:
            res = jwt.decode(
                jwt=s, key=self.key, algorithms=self.algrithms, options=self.options
            )
            return res, ""
        except ExpiredSignatureError as e:
            return None, "Token expired."
        except InvalidSignatureError as e:
            return None, "Token is not valid."
        except DecodeError as e:
            return None, "Not enough segments."

    def encode_user(self, payload: dict) -> str:
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dict type.")
        if "id" not in payload or "username" not in payload:
            raise KeyError("Payload must contain the 'id' and 'username' fields.")
        return self.encode(payload)

    def decode_user(self, s: str, User: Model) -> tuple:
        try:
            obj, msg = self.decode(s)
            if not obj:
                return obj, msg
            user = (
                User.objects.values("id", "username", "password_hash")
                .filter(id=obj["id"])
                .first()
            )
            if not user:
                return None, "The account does not exist."
            if user.get("username") != obj["username"]:
                return None, "The token has been refreshed."
            return User.objects.filter(id=obj["id"]).first(), ""
        except Exception as e:
            logging.error(f"Error decoding jwt: {e}")
            logging.exception(e)
            return None, str(e)

    def check_headers_jwt(self, target: str) -> tuple:
        target_ls = target.strip().split(" ")
        if len(target_ls) != 2:
            return None, "Invalid Authorization header."
        header_type, value = target_ls
        if header_type != self.header_type:
            return None, "Invalid header type."
        return value, ""
