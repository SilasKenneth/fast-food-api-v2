import json

from tests.base import BaseTest
from app.utils import toobj


class TestOrders(BaseTest):
    def test_can_place_order(self):
        response = self.client.post(self.USER_ORDER_URL,
                                    content_type="application/json",
                                    data=json.dumps(self.order_valid),
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "")
        self.assertEqual(response.status_code, 400)

    def test_cannot_order_nothing(self):
        response = self.client.post(self.USER_ORDER_URL,
                                    content_type="application/json",
                                    data=json.dumps(self.order_valid),
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "")
        self.assertEqual(response.status_code, 400)

    def test_order_with_none_existent_item(self):
        response = self.client.post(self.USER_ORDER_URL,
                                    content_type="application/json",
                                    data=json.dumps(self.order_valid),
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "")
        self.assertEqual(response.status_code, 400)

    def test_order_empty(self):
        order = {}
        response = self.client.post(self.USER_ORDER_URL,
                                    content_type="application/json",
                                    data=json.dumps(order),
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", {}).get("address", ""), "Please provide an address for delivery")
        self.assertEqual(response.status_code, 400)

    def test_order_with_wrong_address(self):
        order = {
            "address": 2992922992,
            "items": "1,1,1,1,1,1"
        }
        response = self.client.post(self.USER_ORDER_URL,
                                    content_type="application/json",
                                    data=json.dumps(order),
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "The address you provided is not valid please check your addresses and give a valid id")
        self.assertEqual(response.status_code, 400)

    def test_order_with_no_items(self):
        order = {
            "address": 1,
            "items": ""
        }
        response = self.client.post(self.USER_ORDER_URL,
                                    content_type="application/json",
                                    data=json.dumps(order),
                                    headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "Please specify an address and a list of items")
        self.assertEqual(response.status_code, 400)
