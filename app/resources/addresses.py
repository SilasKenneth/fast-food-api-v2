from flask_restful import Resource, reqparse
from app.utils import normal_token_required
class AddressResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("town", required=True, help="Please provide a town")
    parser.add_argument("street", required=True, help="Please provide a street")
    parser.add_argument("phone", required=True, help="Please provide a phone")

    @normal_token_required
    def get(self, address_id = None):
        pass
    @normal_token_required
    def post(self):
        pass
    @normal_token_required
    def put(self, address_id = None):
        pass