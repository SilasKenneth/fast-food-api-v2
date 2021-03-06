import json
from app.utils import toobj
from tests.base import BaseTest


class TestMenu(BaseTest):
    def test_can_add_menu_item(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.sample_meal), content_type="application/json",
                                    headers=self.get_admin_headers())
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None), "The menu item was successfully saved")
        self.assertEqual(response.status_code, 201)

    def test_cannot_add_empty_name(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.meal_without_name),
                                    headers=self.get_admin_headers(),
                                    content_type="application/json")
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None),
                         "You have to specify all details of an item such as name, price, description")
        self.assertEqual(response.status_code, 403)

    def test_cannot_add_empty_description(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.meal_with_no_description),
                                    content_type="application/json", headers=self.get_admin_headers())
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None),
                         "You have to specify all details of an item such as name, price, description")
        self.assertEqual(response.status_code, 403)

    def test_cannot_add_invalid_price(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.meal_with_invalid_price),
                                    content_type="application/json", headers=self.get_admin_headers())
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None), "Please specify a valid price for the item")
        self.assertEqual(response.status_code, 403)

    def test_cannot_add_existing(self):
        response1 = self.client.post(self.MENU_URL, data=json.dumps(self.sample_meal),
                                     content_type="application/json",
                                     headers=self.get_admin_headers())
        response = self.client.post(self.MENU_URL, data=json.dumps(self.sample_meal),
                                    content_type="application/json",
                                    headers=self.get_admin_headers())
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None), "There was problem saving the item. Try again")
        self.assertEqual(response.status_code, 403)

    def test_cannot_add_invalid_name(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.sample_meal), content_type="application/json",
                                    headers=self.get_admin_headers())
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None), "There was problem saving the item. Try again")
        self.assertEqual(response.status_code, 403)

    def test_cannot_add_without_token(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.sample_meal), content_type="application/json")
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None), "Invalid authorization format use the format 'Bearer <TOKEN>'")
        self.assertEqual(response.status_code, 400)

    def test_cannot_add_without_admin_token(self):
        response = self.client.post(self.MENU_URL, data=json.dumps(self.sample_meal), content_type="application/json",
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertNotEqual(response_obj, None)
        self.assertEqual(response_obj.get("message", None), "Please login first, your session might have expired")
        self.assertEqual(response.status_code, 401)
