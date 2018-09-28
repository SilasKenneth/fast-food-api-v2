from flask_restful import Resource, reqparse
from app.models import Menu
from app.utils import empty, valid_price, valid_name, valid_description


class MenuResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, help="Please provide an item name")
    parser.add_argument("description", required=True, help="Please provide a description")
    parser.add_argument("price", required=True, help="Please provide a price")

    def post(self):
        args = self.parser.parse_args()
        name = args.get("name", "")
        description = args.get("description", "")
        price = args.get("price", "")
        if empty(name) or empty(description) or empty(price):
            return {"message": "You have to specify all"
                               " details of an item"
                               " such as name, price, description"}, 403
        if not valid_name(name):
            return {"message": "Please specify a valid name for item"}, 403
        if not valid_price(price):
            return {"message": "Please specify a valid price"
                               " for the item"}, 403
        if not valid_description(description):
            return {"message": "Please specify a valid description "
                               "for the item"}
        menu_item = Menu(name, description, 200)
        saved = menu_item.save()
        if saved:
            return {"message": "The menu item was successfully saved", "data":
                menu_item.json}, 201
        return {"message": "There was problem saving the item. Try again"}, 403

    def put(self, menu_id):
        pass

    def get(self, meal_id=None):
        if meal_id is None:
            meals = Menu.all()
            return {"menu": meals}, 200
        if not isinstance(meal_id, str) and not isinstance(meal_id, int):
            return {"message": "The menu item with id %s does not exist" % meal_id}, 404
        meal = Menu.find_by_id(meal_id)
        if not meal:
            return {"message": "The menu item with id %s does not exist" % meal_id}, 404
        return {"item": meal.json}

    def delete(self, meal_id):
        pass
