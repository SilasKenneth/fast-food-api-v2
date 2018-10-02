from flask import request
from flask_restful import Resource, reqparse
from app.models import Order, Address, Menu
from app.utils import (admin_token_required,
                       normal_token_required,
                       decode_token as claims,
                       empty)

from app.models import Order
from app.utils import admin_token_required


class OrderResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("address", required=True, help="Please provide "
                                                       "an address for delivery")
    parser.add_argument("items", required=True, help="Please specify a comma separated list of"
                                                     " items")

    @normal_token_required
    def post(self):
        print(request.authorization)
        args = self.parser.parse_args()
        address_id = args.get("address", "")
        items = args.get("items", "")
        if empty(address_id) or empty(items):
            return {"message": "Please specify an address and a list of"
                               " items"}, 400
        address = Address.find_by_id(address_id=address_id)
        if not address:
            return {"message": "The address you provided is not valid"
                               " please check your addresses and give a"
                               " valid id"}, 400
        items = items.split(",")
        ordered_items = []
        for item in items:
            item_object = Menu.find_by_id(meal_id=item)
            if item_object is None:
                return {"message": "The item with id %s does not exist."
                                   ". Try another" %
                                   item}, 404
            ordered_items.append(item_object)
        order = Order()
        return {"message": "The order was successfully placed", "order": order.json1}, 200

    @normal_token_required
    def get(self, order_id=None):
        if order_id is None:
            return Order.all()
        return Order.find_by_id(ids=order_id)

    @normal_token_required
    def put(self, order_id=None):
        pass


class AdminOrderResource(Resource):
    """The resource where admin manages orders"""

    @admin_token_required
    def get(self, order_id=None):
        """Get all orders if order_id is None otherwise get a specific order"""
        if order_id is None:
            orders = Order.all()
            result = [order.json for order in orders]
            return {"message": "success", "orders": result}, 200
        order_current = Order.find_by_id(ids=order_id)
        if not order_current:
            return {"message": "The order with id %s is not available" % order_id}, 404
        return order_current.json1

    @admin_token_required
    def put(self, order_id=None):
        """Update the status of an order"""
        if order_id is None:
            return {"message": "Missing order_id in your url"}, 400
        order = Order.find_by_id(ids=order_id)
        if order is None:
            return {"message": "The order with order_id %s was not "
                               "found" % order_id}, 404

        return order
