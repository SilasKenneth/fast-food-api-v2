import json
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
        self.USER_ORDER_URL = "/api/v2/users/orders"
        self.ADDRESS_URL = "/api/v2/addresses"
        self.sample_meal = {
            "name": "Soda na chips",
            "description": "This is menu item"
                           " ordering at any given moment",
            "price": 200
        }
        self.duplicate_meal = self.sample_meal
        self.meal_without_name = {
            "name": "",
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
        self.meal_with_invalid_name = {
            "name": "199191",
            "price": 200,
            "description": self.sample_meal['description']
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
        self.test_user_login = {
            "username": "silaskenn",
            "password": "SilasK@2018"
        }
        self.user_tests_admin = {
            "username": "silaskenny",
            "password": "SilasK@2019"
        }
        self.address_test = {
            "town": "Mombasa",
            "street": "Mpeketoni",
            "phone": "0707885973"
        }
        self.address_invalid_phone = {
            "town": "Nairobi",
            "street": "Jogoo Road",
            "phone": "07082727"
        }

        self.order_valid = {
            "address": "1",
            "items": "1,1,1,1,1,1",
        }
        self.order_nonexistent_product = {
            "address": "1",
            "items": "1,100,10,1"
        }
        self.order_invalid_address = {
            "address": "h",
            "items": "1,1,1,1,1"
        }

        self.order_non_existent_address = {
            "address": '1',
            "items": '1,1,1,1,1,1'
        }

        self.order_with_no_items = {
             "address": "1",
             "items":""
        }

    @classmethod
    def setUpClass(cls):
        cls.database = database

    @classmethod
    def tearDownClass(cls):
        cls.database.drop_tables()
        cls.database.create_tables()
        cls.database.create_default_admin()

    def create_test_user(self):
        response = self.client.post(self.AUTH_URL + "signup",
                                    data=json.dumps(self.test_user),
                                    content_type="application/json")

    def logged_in_user(self):
        self.create_test_user()
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.test_user_login),
                                    content_type="application/json")
        try:
            response_obj = json.loads(response.data)
            # print(response_obj)
        except Exception as ex:
            response_obj = {}
        # print(response_obj)
        return response_obj.get("token", "")

    def logged_in_admin(self):
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.user_tests_admin),
                                    content_type="application/json")
        try:
            response_obj = json.loads(response.data)
        except Exception as ex:
            response_obj = {}
        return response_obj.get("token", "")

    def get_admin_headers(self):
        headers = {'Authorization': 'Bearer {}'.format(self.logged_in_admin())}
        return headers

    def get_user_headers(self):
        headers = {'Authorization': 'Bearer {}'.format(self.logged_in_user())}
        return headers
