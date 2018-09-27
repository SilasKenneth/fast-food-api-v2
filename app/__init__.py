from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_restful import Api
from config import configurations


def create_app(config):
    prefix = "/api/v2/"
    user_blueprint =  Blueprint("users", __name__, url_prefix=prefix)
    orders_blueprint = Blueprint("orders", __name__, url_prefix=prefix)
    menu_blueprint = Blueprint("menu", __name__, url_prefix=prefix)
    address_blueprint = Blueprint("addresses", __name__, url_prefix=prefix)

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
    app.register_blueprint(user_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(menu_blueprint)
    app.register_blueprint(address_blueprint)
    api = Api(app)
    CORS(app)
    api.add_resource(LoginResource, "/api/v2/auth/login")
    api.add_resource(SignUpResource, "/api/v2/auth/signup")
    api.add_resource(MenuResource, "/api/v2/menu", "/api/v2/menu/<int:ids>")
    api.add_resource(ProfileResource, "/api/v2/user")
    api.add_resource(OrderResource, "/api/v2/orders", "/api/v2/orders/<int:ids>")
    api.add_resource(AddressResource, "/api/v2/addresses", "/api/v2/addresses/<int:ids>")
    @app.route("/")
    def index():
        return jsonify({"message": "Hello customer"})

    return app
