import json
from tests.base import BaseTest


class TestUsers(BaseTest):
    def test_can_sign_up(self):
        response = self.client.post(self.AUTH_URL + "signup", data=json.dumps(self.test_user)
                                    , content_type="application/json")
        response_obj = json.loads(response.data)
        response_obj = {} if response_obj is None else response_obj
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_obj.get("message", None), "You successfully signed up"
                                                            " you can now login")
