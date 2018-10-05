from flask import request
from flask_restful import Resource, reqparse
from app.models import Order, Address, Menu
from app.utils import (admin_token_required,
                       normal_token_required,
                       decode_token as claims,
                       empty,
                       get_details_from_token as details)

from app.models import Order


class OrderResource(Resource):
    """The class for the normal user orders endpoints"""
    parser = reqparse.RequestParser()
    parser.add_argument("address", required=True, help="Please provide an address for delivery")
    parser.add_argument("items", required=True, help="Please specify a comma separated list of items")

    @normal_token_required
    def post(self):
        """Create a new order"""
        args = self.parser.parse_args()
        address_id = args.get("address", "")
        items = args.get("items", "")
        customer_id = details(claims).get("id", "0")
        if empty(address_id) or empty(items):
            return {"message": "Please specify an address and a list of"
                               " items"}, 400
        address = Address.find_by_id(address_id=address_id, user_id=customer_id)
        if not address:
            return {"message": "The address you provided is not valid"
                               " please check your addresses and give a"
                               " valid id"}, 400
        items = items.split(",")
        new_items = [int(item) for item in items if item.strip() != '']
        copy_items = set(new_items)
        new_items = list(new_items)
        ordered_items = []
        total = 0.00
        for item in copy_items:
            item_object = Menu.find_by_id(meal_id=item)
            if item_object is None:
                return {"message": "The item with id %s does not exist."
                                   ". Try another" %
                                   item}, 404
            item_object.quantity = new_items.count(item)
            total += float(item_object.price * item_object.quantity)
            ordered_items.append(item_object)
        order = Order(customer_id, address_id, ordered_items)
        order.total = total
        saved = order.save()
        if not saved:
            return {"message": "There was a problem placing the order please try again"}, 400
        return {"message": "The order was successfully placed", "order": order.json1}, 200

    @normal_token_required
    def get(self, order_id=None):
        """Get orders if not order_id is provided otherwise get a given order if it belongs to the user"""
        customer_id = details(claims).get("id", "")
        if order_id is None:
            orders = Order.all(user_id=customer_id, user_type=1)
            if not orders:
                return {"message": "You don't currently have any orders"}, 404
            orders = [order.json for order in orders]
            return {"message":"success", "orders":orders}
        order = Order.find_by_id(ids=order_id, user_id=customer_id)
        if not order:
            return {"message": "The order was not found in the database "
                               ".Try again"}, 404
        return {"message": "success", "order": order.json1}, 200

    @normal_token_required
    def put(self, order_id=None):
        """Update the status of an order"""
        if order_id is None:
            return {"message": "There was no order id provided in the url"}, 400
        order = Order.find_by_id(ids=order_id)
        if not order:
            return {"message": "The order with id %s doesn't exist"%order_id}, 404
        if order.status.lower() != "new":
            return {"message": "The order you are trying to cancel cannot be cancelled at the stage it "
                               "is currently at"}, 400
        cancelled = order.cancel()
        if cancelled:
            return {"message": "The order was successfully cancelled", "data": order.json}, 400
        return {"message": "There was a problem cancelling the order"}, 400


class AdminOrderResource(Resource):
    """The resource where admin manages orders"""
    parser = reqparse.RequestParser()
    parser.add_argument("status", required=True, help="Please provide a status")

    @admin_token_required
    def get(self, order_id=None):
        """Get all orders if order_id is None otherwise get a specific order"""
        details1 = details(claims)
        if order_id is None:
            orders = Order.all()
            result = [order.json for order in orders]
            return {"message": "success", "orders": result}, 200
        order_current = Order.find_by_id(ids=order_id, user_id=details1.get("id", "1"))
        if not order_current:
            return {"message": "The order with id %s is not available" % order_id}, 404
        return order_current.json1

    @admin_token_required
    def put(self, order_id=None):
        """Update the status of an order by cancelling it"""
        args = self.parser.parse_args()
        status = args.get("status", "")
        if order_id is None:
            return {"message": "Missing order_id in your url"}, 400
        if empty(status):
            return {"message": "Please provide a status to change the order %s's status to" % order_id}, 403
        order = Order.find_by_id(ids=order_id)
        if order is None:
            return {"message": "The order with order_id %s was not "
                               "found" % order_id}, 404
        order.status = status
        return order
