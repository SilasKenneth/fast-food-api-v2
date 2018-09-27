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
