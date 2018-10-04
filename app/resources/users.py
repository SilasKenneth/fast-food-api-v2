import os
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
import jwt
from flask import current_app
from app.utils import (validate_username,
                       validate_password,
                       validate_email, empty,
                       validate_fullname)
from app.models import User


class SignUpResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("fullnames", required=True, help="Please specify your full name")
    parser.add_argument("username", required=True, help="Please specify a username")
    parser.add_argument("email", required=True, help="Please specify an email")
    parser.add_argument("password", required=True, help="Please specify a password")
    parser.add_argument("confirm_pass", required=True, help="Please confirm your password")

    def post(self):
        args = self.parser.parse_args()
        fullnames = args.get("fullnames", "")
        username = args.get("username", "")
        email = args.get("email", "")
        password = args.get("password", "")
        confirm_pass = args.get("confirm_pass", "")
        if empty(fullnames) or empty(username) or empty(email) or empty(password) or empty(confirm_pass):
            return {"message": "All the fields are required"}, 400
        if not validate_fullname(fullnames):
            return {"message": "Please enter a valid full name"
                               " it should contain first and last name which"
                               " start with capital letters"}, 400
        if not validate_username(username):
            return {"message": "Please specify a valid username "
                               " a username should contain lowercase"
                               " letters only and be between 6 to 12 letters"}, 400
        if not validate_email(email):
            return {"message": "Please enter a valid email address"}, 400
        if not validate_password(password):
            return {"message": "Please enter a valid password"
                               " it must contain atleast one"
                               " lowercase, uppercase special character and a"
                               " number"}, 400
        user = User(fullnames, username, password, email)
        if not check_password_hash(user.password, confirm_pass):
            return {"message": "The password and the verifications don't"
                               " match"}, 400
        saved = user.save()
        if not saved:
            return {"message": "The username or email is already in use"}, 400
        return {"message": "You successfully signed up you can now login", "data": user.json1}


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, help="Provide a username")
    parser.add_argument("password", required=True, help="Provide a password")

    def post(self):
        args = self.parser.parse_args()
        username = args.get("username", "")
        password = args.get("password", "")
        user = User.get_by_username_or_email(username)
        if user is None:
            return {"message": "Incorrect username or password provided"}, 403
        if not check_password_hash(user.password, password):
            return {"message": "Incorrect username or password provided"}, 403
        payload = user.json
        key = current_app.config.get("JWT_SECRET_KEY")
        token = jwt.encode(payload=payload, key=key).decode("utf8")
        return {"message": "You successfully logged in", "token": str(token)}


class ProfileResource(Resource):
    def put(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass
