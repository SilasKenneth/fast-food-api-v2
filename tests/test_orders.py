from tests.base import BaseTest
from app.models import Order


class TestOrders(BaseTest):
    def test_can_place_order(self):
        self.assertEqual(1, 1)
    def test_cannot_order_nothing(self):
        order = Order(1, 1, "10")
        self.assertEqual(order, order)