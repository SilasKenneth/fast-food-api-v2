from unittest import TestCase
from app import create_app
from app.db import database
from copy import deepcopy


class BaseTest(TestCase):
    def setUp(self):
        self.database = database
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.MENU_URL = "/api/v2/menu"
        self.ORDER_URL = "/api/v2/orders"
        self.AUTH_URL = "/api/v2/auth/"
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
        self.test_user = {
            "fullnames": "Silas Kenneth",
            "username": "silaskenn",
            "password": "SilasK@2018",
            "confirm_pass": "SilasK@2018",
            "email": "silaskenn@gmail.com"
        }
        self.test_user_invalid_password = {
            "username": "silaskenn",
            "password": "SilasK@2019"
        }
        self.user_invalid_username = {
            "username": "wronusername",
            "password": "SilasK@2019"
        }
        self.user_unmet_password = {
            "fullnames": self.test_user['fullnames'],
            "username": "silaskenny",
            "email": "silaskenn@gmail.com",
            "password": "Silas2019",
            "confirm_pass": "Silas2019"
        }
        self.user_invalid_email = {
            "username": "silaskenn",
            "fullnames": "Silas Kenneth",
            "email": "silask@no",
            "password": "Nyamwaro@2012",
            "confirm_pass": "Nyamwaro@2012"
        }
        self.user_invalid_username_signup = deepcopy(self.test_user)
        self.user_invalid_username_signup['username'] = "Invalid100"

    @classmethod
    def setUpClass(cls):
        cls.database = database
        cls.database.create_tables()
    @classmethod
    def tearDownClass(cls):
        cls.database.drop_tables()
