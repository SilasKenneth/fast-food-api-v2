from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_restful import Api

from config import configurations


def create_app(config):
    """
    Create a new flask app and return the app
    """
    app = Flask(__name__)
    app.config.from_object(configurations.get(config, "production"))
    app.url_map.strict_slashes = False
    with app.app_context():
        from app.resources.users import LoginResource
        from app.resources.users import SignUpResource
        from app.resources.users import ProfileResource
        from app.resources.menu import MenuResource
        from app.resources.orders import OrderResource
        from app.resources.addresses import AddressResource
        from app.resources.orders import AdminOrderResource
    api = Api(app)
    CORS(app)
    api.add_resource(LoginResource, "/api/v2/auth/login")
    api.add_resource(SignUpResource, "/api/v2/auth/signup")
    api.add_resource(MenuResource, "/api/v2/menu",
                     "/api/v2/menu/<int:menu_id>")
    api.add_resource(ProfileResource, "/api/v2/user")
    api.add_resource(OrderResource, "/api/v2/users/orders",
                     "/api/v2/users/orders/<int:order_id>")
    api.add_resource(AddressResource, "/api/v2/addresses",
                     "/api/v2/addresses/<int:address_id>")
    api.add_resource(AdminOrderResource, "/api/v2/orders",
                     "/api/v2/orders/<int:order_id>")

    @app.route("/")
    def index():
        return jsonify({"message": "Hello customer"})

    return app
