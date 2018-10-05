import unittest
from app.models import Base


class TestModels(unittest.TestCase):
    def test_cannot_get_from_invalid_table(self):
        base = Base()
        res = base.all("sopapsspp")
        self.assertEqual([], res)
