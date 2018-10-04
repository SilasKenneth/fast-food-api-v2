from flask_restful import Resource, reqparse, request
from app.models import Menu
from app.utils import (empty,
                       valid_price,
                       valid_name,
                       valid_description,
                       decode_token as claims,
                       admin_token_required)


class MenuResource(Resource):
    """Menu item endpoints resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, help="Please provide an item name")
    parser.add_argument("description", required=True, help="Please provide a description")
    parser.add_argument("price", required=True, help="Please provide a price")

    @admin_token_required
    def post(self):
        """Create a new menu item"""
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
        menu_item = Menu(name, description, price)
        saved = menu_item.save()
        if saved:
            return {"message": "The menu item was successfully saved", "data":
                menu_item.json1}, 201
        return {"message": "There was problem saving the item. Try again"}, 403

    @admin_token_required
    def put(self, menu_id):
        """Update a menu item"""
        menu = Menu.find_by_id(meal_id=menu_id)
        if menu is None:
            return {"message": "The menu item with an id number %s doesn't"
                               " exist"%menu_id}, 404
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
        menu_item.id = menu.id
        updated = menu_item.update()
        if updated:
            return {"message": "The menu item was successfully updated",
                    "menu_item": menu_item.json}, 200
        else:
            return {"message": "There was a problem updating the menu item"
                               " maybe you provided a name already taken by"
                               " another menu item"}, 400

    def get(self, menu_id=None):
        """Get either all menu items"""
        if menu_id is None:
            meals = Menu.all()
            if not meals:
                return {"message": "No menu items are currently available. Check on later"}, 404
            return {"message": "success", "menu": meals}, 200
        if not isinstance(menu_id, str) and not isinstance(menu_id, int):
            return {"message": "The menu item with id %s does not exist" % menu_id}, 404
        meal = Menu.find_by_id(meal_id=menu_id)
        print(meal)
        if not meal:
            return {"message": "The menu item with id %s does not exist" % menu_id}, 404
        return {"message": "success", "item": meal.json}

    @admin_token_required
    def delete(self, meni_id=None):
        pass
