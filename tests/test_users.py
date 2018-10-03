import json
from tests.base import BaseTest
from app.utils import (toobj)


class TestUsers(BaseTest):
    def test_can_sign_up(self):
        response = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.test_user)
                                    , content_type="application/json")
        response_obj = toobj(response.data)
        response_obj = {} if response_obj is None else response_obj
        # print(response_obj)
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_obj.get("message", None), "You successfully signed up"
                                                            " you can now login")

    def test_sign_up_invalid_password(self):
        response = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.user_unmet_password)
                                    , content_type="application/json")
        response_obj = toobj(response.data)
        response_obj = {} if response_obj is None else response_obj
        # print(response_obj)
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_obj.get("message", None), "Please enter a valid password it must "
                                                            "contain atleast one lowercase, uppercase "
                                                            "special character and a number")

    def test_sign_up_invalid_email(self):
        response = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.user_invalid_email)
                                    , content_type="application/json")
        response_obj = toobj(response.data)
        response_obj = {} if response_obj is None else response_obj
        # print(response_obj)
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_obj.get("message", None), "Please enter a valid email address")

    def test_signup_invalid_username(self):
        response = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.user_invalid_username_signup)
                                    , content_type="application/json")
        response_obj = toobj(response.data)
        response_obj = {} if response_obj is None else response_obj
        # print(response_obj)
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_obj.get("message", None), "Please specify a valid username "
                                                            " a username should contain lowercase letters"
                                                            " only and be between 6 to 12 letters")

    def test_signup_existing_username(self):
        response = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.test_user)
                                    , content_type="application/json")
        response1 = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.test_user)
                                     , content_type="application/json")
        response_obj = toobj(response1.data)
        response_obj = {} if response_obj is None else response_obj
        self.assertNotEqual(response1.data, None)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response_obj.get("message", None), "The username or email is already in use")

    def test_login(self):
        response1 = self.client.post(self.AUTH_URL + "login", data=json.dumps(self.test_user)
                                     , content_type="application/json")
        response_obj = toobj(response1.data)
        response_obj = {} if response_obj is None else response_obj
        # print(response_obj)
        self.assertNotEqual(response1.data, None)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response_obj.get("message", None), "You successfully logged in")
