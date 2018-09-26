from unittest import TestCase
from app import create_app
from app.db import database


class BaseTest(TestCase):
    def setUp(self):
        self.database = database
        self.database.drop_tables()
        self.database.create_tables()
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.MENU_URL = "/api/v2/menu"
        self.ORDER_URL = "/api/v2/orders"
        self.sample_meal = {
            "name": "Soda na chips",
            "description": "This is menu item that every single customer of ours prefers"
                           " ordering at any given moment",
            "price": 200
        }
        self.duplicate_meal = self.sample_meal
        self.meal_without_name = {
            "name" : "",
            "description": "Some good food",
            "price": 200
        }

        self.meal_with_invalid_price = {
            "name": "Sushi",
            "description": "Some good one",
            "price": -300
        }
        self.meal_with_no_description = {
            "name": "Silly meal",
            "price": 200,
            "description": ""
        }

    def tearDown(self):
        self.database.drop_tables()
