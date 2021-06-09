from datetime import datetime
from unittest import TestCase
from config.models import Admin, Issues


class TestAdminModel(TestCase):
    def test_valid_entry(self):
        user = Admin(email='testuser@localhost.com', password='testpassword')
        self.assertIsInstance(user, Admin)

    @staticmethod
    def create_invalid():
        user = Admin('testuser@localhost.com')
        return user

    def test_invalid_entry(self):
        self.assertRaises(TypeError, self.create_invalid)

    def test_repr(self):
        user = Admin(email='testuser@localhost.com', password='testpassword')
        self.assertEqual(str(user), 'testuser@localhost.com')


class TestIssueModel(TestCase):

    @classmethod
    def setUpClass(cls):
        issue = Issues(user_email='testissue@gmail.com',
                       book_name='testbook', book_id=1231, debt=None)
        cls.issue = issue

    def test_valid_entry(self):
        self.assertIsInstance(self.issue, Issues)

    def invalid():
        Issues(user_email='testissue@gmail.com',
               book_name='testbook', book_id=None, debt=None)

    def test_invalid_entry(self):
        self.assertRaises(TypeError, self.invalid)

    def test_unique(self):
        self.assertEqual(str(self.issue), 'testissue@gmail.com')

    @classmethod
    def tearDownClass(cls):
        pass
