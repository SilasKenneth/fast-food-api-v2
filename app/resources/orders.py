from flask_restful import Resource

from app.models import Order
from app.utils import admin_token_required


class OrderResource(Resource):
    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass
class AdminOrderResource(Resource):
    @admin_token_required
    def get(self, order_id=None):
        if order_id is None:
            pass
        order = Order.find_by_id(ids=order_id)
        return order
    def post(self):
        pass
    def put(self, order_id):
        pass