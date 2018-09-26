import json
from tests.base import BaseTest

class TestUsers(BaseTest):
    def test_can_sign_up(self):
        response = self.client.post(self.AUTH_URL+"signup", data=json.dumps(self.test_user)
                                    ,content_type="application/json")
        print(response.data)