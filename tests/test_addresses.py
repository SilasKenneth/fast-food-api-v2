import json
from tests.base import BaseTest
from app.utils import toobj


class TestAddress(BaseTest):
    def test_can_add_address(self):
        response = self.client.post(self.ADDRESS_URL,
                                    data=json.dumps(self.address_test),
                                    headers=self.get_user_headers(),
                                    content_type="application/json")
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""), "The address was successfully saved")
        self.assertEqual(response.status_code, 201)

    def test_cannot_add_address_invalid_phone(self):
        response = self.client.post(self.ADDRESS_URL,
                                    data=json.dumps(self.address_invalid_phone),
                                    headers=self.get_user_headers(),
                                    content_type="application/json")
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "Invalid phone number please provide a valid phone number starting with 07")
        self.assertEqual(response.status_code, 400)

    def test_get_address(self):
        response = self.client.get(self.ADDRESS_URL,
                                   headers=self.get_user_headers())
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""), "success")
        self.assertEqual(response.status_code, 200)

    def test_get_one_address(self):
        response = self.client.get("/api/v2/addresses/%d"%1,
                                   headers=self.get_user_headers(),
                                   content_type="application/json")
        response2 = self.client.get(self.ADDRESS_URL + "/2",
                                    headers=self.get_user_headers())
        response_obj = toobj(response2.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_obj.get("message", ""), "success")

    def test_add_invalid_token(self):
        response = self.client.post(self.ADDRESS_URL,
                                    data=json.dumps(self.address_test))
        response_obj = toobj(response.data)
        self.assertEqual(response_obj.get("message", ""),
                         "Invalid authorization format use the format 'Bearer <TOKEN>'")
        self.assertEqual(response.status_code, 400)
