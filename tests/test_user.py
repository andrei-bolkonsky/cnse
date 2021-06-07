import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        test_user = User(password='ploud')
        self.assertTrue(test_user.password_hash is not None)

    def test_no_password_getter(self):
        test_user = User(password='ploud')
        with self.assertRaises(AttributeError):
            test_user.password

    def test_password_verification(self):
        test_user = User(password='ploud')
        self.assertTrue(test_user.verify_password('ploud'))
        self.assertFalse(test_user.verify_password('glob'))

    def test_password_salts_are_random(self):
        test_user = User(password='cat')
        test_user_2 = User(password='cat')
        self.assertTrue(test_user.password_hash != test_user_2.password_hash)