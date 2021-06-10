from unittest import TestCase
from config import db
from config.models import Admin, Issues, Member 

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


        cls.member = Member(user_email='localhost@gmail.com', debt=10)
        db.session.add(cls.member)
        db.session.commit()
        cls.issue = Issues(isbn=123, user=cls.member.id)

    def test_valid_entry(self):
        self.assertIsInstance(self.issue, Issues)

    def invalid():
        Issues(isbn=123123)

    def test_invalid_entry(self):
        self.assertRaises(TypeError, self.invalid)

    @classmethod
    def tearDownClass(cls):
        db.session.delete(cls.member)
        db.session.commit()
