from flask import request
from flask_restful import Resource, reqparse
from app.models import Address
from app.utils import (normal_token_required,
                       empty,
                       validate_phone,
                       decode_token as claims,
                       get_details_from_token)


class AddressResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("town", required=True, help="Please provide a town")
    parser.add_argument("street", required=True, help="Please provide a street")
    parser.add_argument("phone", required=True, help="Please provide a phone")

    @normal_token_required
    def get(self, address_id=None):
        user_id = get_details_from_token(claims).get("id", "0")
        if address_id is None:
            addresses = Address.all(user_id=user_id)
            if not addresses:
                return {"message": "You currently don't have any addresses. Add one first"}, 404
            res = [address.json1 for address in addresses]
            return {"message":"success", "addresses":res}, 200
        address = Address.find_by_id(user_id=user_id)
        if not address:
            return {"message": "The address with id %s was not found in your addresses" % (
                address_id
            )}
        return {"message": "success", "address": address.json1}

    @normal_token_required
    def post(self):
        details = get_details_from_token(claims)
        args = self.parser.parse_args()
        town = args.get("town", "")
        street = args.get("street", "")
        phone = args.get("phone", "")
        if empty(phone) or empty(town) or empty(street):
            return {"message": "Please provide a phone, street and town"}, 400
        if not validate_phone(phone):
            return {"message": "Invalid phone number please provide a valid phone number starting with 07"}, 400
        address = Address(town, street, phone)
        if not details.get("id", ""):
            return {"message": "We could not verify your token please try again"}, 403
        saved = address.save(user_id=details.get("id", ""))
        if saved:
            return {"message": "The address was successfully saved", "data": address.json}, 200
        return {"message": "There was a problem saving the address to the database"}, 400
