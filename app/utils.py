import re
import json
from functools import wraps
import jwt
from flask import request, current_app


def validate_phone(phone):
    if not isinstance(phone, str):
        return False
    if len(phone) < 10:
        return False
    if phone[0:2] != '07':
        return False
    valid = re.match('^07[0-9]{8,8}$', phone)
    if not valid:
        return False
    return True


def empty(value):
    if not isinstance(value, str):
        return True
    if len(value.strip()) == 0:
        return True
    return False


def valid_price(price):
    if not isinstance(price, str):
        if isinstance(price, (int, float)):
            return True
        return False
    if not str(price).isnumeric():
        return False
    if float(price) <= 0.50:
        return False
    return True


def valid_name(name):
    if not isinstance(name, str):
        return False
    matched = re.match("^[a-zA-Z][a-zA-Z ]{4,20}$", name)
    if matched is None:
        return False
    return True


def valid_description(desc):
    if not isinstance(desc, str):
        return False
    matched = re.match("^[a-zA-Z][a-zA-Z ]{12,}$", desc)
    if matched is None:
        return False
    return True


def toobj(jsonified):
    """Use json.loads without having to write it every now and again"""
    try:
        res = json.loads(jsonified)
        return res
    except Exception as ex:
        return {}


def validate_email(email):
    """Validator to check if email requirements are met"""
    if not isinstance(email, str):
        return False
    if len(email) <= 7:
        return False
    ans = re.match("^.+@(\\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email)
    if ans is None:
        return False
    return True


def validate_password(password):
    """Validator to check is password requirements are met"""
    if not isinstance(password, str):
        return False
    ans = re.match(r"(?=.*[A-Za-z0-9])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{6,12}", password)
    if ans is None:
        return False
    return True


def validate_username(username):
    """A validator to check if username requirements are met"""
    if not isinstance(username, str):
        return False
    if len(username) < 3 or len(username) > 12:
        return False
    else:
        ans = re.match(r'^[a-z|\s]+$', username)
        if ans is None:
            return False
        return True


def validate_fullname(names):
    if not isinstance(names, str):
        return False
    if len(names) < 6 or len(names) > 50:
        return False
    ans = re.match(r'^[A-Z][a-z]{2,20} [A-Z][a-z]{2,20}$', names)
    if ans is None:
        return False
    return True


def normal_token_required(func):
    """Make sure that a token is provided"""

    @wraps(func)
    def decorated(*args, **kwargs):
        # import pdb;
        # pdb.set_trace()
        access_token = None
        try:
            authorization_header = request.headers.get('Authorization', "")
            authorization_header = authorization_header.split(" ")
            if len(authorization_header) < 2:
                return {"message": "Invalid authorization format use the format \'Bearer <TOKEN>\'"}, 400
            access_token = authorization_header[1]
            if access_token:
                decoded_token = decode_token(access_token)
                print(decoded_token)
                user_id = decoded_token.get("id", None)
                role = decoded_token.get("user_type", None)
                if role != "normal":
                    return {"message": "Invalid access token provided please login to"
                                       " get a new valid token"}, 401
                if user_id is None:
                    return {"message": "Invalid access token provided please login to view"
                                       " get a valid token"}, 401
                return func(*args, **kwargs)

            return {'message': "Please login first, your session might have expired"}, 401
        except jwt.DecodeError as ex:
            # print(e)
            return {'message': 'An error occurred while decoding token.', 'error': str(ex)}, 400
        except jwt.ExpiredSignature as ex:
            return {"message": "The token you provided token has expired please login again",
                    "error": str(ex)}, 400
        except jwt.InvalidTokenError as ex:
            return {"message": "There were other issues decoding the token please try to "
                               "login again", "error": str(ex)}, 400

    return decorated


def admin_token_required(func):
    """Make sure that a token is provided"""

    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            authorization_header = request.headers.get('Authorization', "")
            authorization_header = authorization_header.split(" ")
            print(authorization_header)
            if len(authorization_header) < 2:
                return {"message": "Invalid authorization format use the format \'Bearer <TOKEN>\'"}, 400
            access_token = authorization_header[1]
            if access_token:
                decoded_token = decode_token(access_token)
                user_id = decoded_token.get("id", None)
                role = decoded_token.get("user_type", None)
                # print(decoded_token)
                if role != "admin":
                    return {"message": "Invalid access token provided please login to view"
                                       " get a valid token"}, 401
                if user_id is None or role is None:
                    return {"message": "Invalid access token provided please login to"
                                       " get a valid token"}, 401
                return func(*args, **kwargs)
            return {'message': "Please login first, your session might have expired"}, 401
        except jwt.DecodeError as ex:
            # print(e)
            return {'message': 'An error occurred while decoding token.', 'error': str(ex)}, 400
        except jwt.ExpiredSignature as ex:
            return {"message": "The token you provided token has expired please login again", "error": str(ex)}, 400
        except jwt.InvalidTokenError as ex:
            return {"message": "There were other issues decoding the token please try to login again", "error": str(ex)}, 400

    return decorated


def decode_token(token):
    try:
        if not isinstance(token, (bytes, str)):
            return {}
        claims = jwt.decode(token, current_app.config.get("JWT_SECRET_KEY"), True,
                            algorithms=["HS256"])
        return claims
    except Exception as ex:
        # print(ex)
        return {}

def get_details_from_token(decoder):
    token = request.headers.get("Authorization", "").split(" ")
    return decoder(token[1])