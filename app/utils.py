import re
import json


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
    matched = re.match("^[a-zA-Z][a-zA-Z ]{50,100}$", desc)
    if matched is None:
        return False
    return True


def toobj(jsonified):
    try:
        res = json.loads(jsonified)
        return res
    except Exception as ex:
        return {}


def validate_email(email):
    if not isinstance(email, str):
        return False
    if len(email) <= 7:
        return False
    ans = re.match("^.+@(\\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email)
    if ans is None:
        return False
    return True


def validate_password(password):
    if not isinstance(password, str):
        return False
    ans = re.match(r"(?=.*[A-Za-z0-9])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{6,12}", password)
    if ans is None:
        return False
    return True


def validate_username(username):
    if not isinstance(username, str):
        return False
    if len(username) < 6 or len(username) > 12:
        return False
    else:
        ans = re.match(r'^[a-z|\s]+$', username)
        if ans is None:
            return False
        return True


def validate_fullname(names):
    if not isinstance(names, str):
        return False
    if len(names) < 12 or len(names) > 50:
        return False
    ans = re.match(r'^[A-Z][a-z]{4,20} [A-Z][a-z]{4,20}$', names)
    if ans is None:
        return False
    return True
