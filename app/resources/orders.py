from flask_restful import Resource


class OrderResource(Resource):
    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass
class AdminOrderResource(Resource):
    def get(self, order_id=None):
        if order_id is None:
            pass
        order = ""
    def post(self):
        pass
    def put(self, order_id):
        pass