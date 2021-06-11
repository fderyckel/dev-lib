from unittest import TestCase
from config import db
from config.models import Admin, Issues, Member


class TestAdminModel(TestCase):
    def test_valid_entry(self) -> None:
        """Test valid entry
        """
        user = Admin(email='testuser@localhost.com', password='testpassword')
        self.assertIsInstance(user, Admin)

    @staticmethod
    def create_invalid() -> str:
        """Raises error

        Returns:
            str: models class repr method
        """
        user = Admin('testuser@localhost.com')
        return user

    def test_invalid_entry(self) -> None:
        """Invalid data entry
        """
        self.assertRaises(TypeError, self.create_invalid)

    def test_repr(self) -> None:
        """Model repr methods
        """
        user = Admin(email='testuser@localhost.com', password='testpassword')
        self.assertEqual(str(user), 'testuser@localhost.com')


class TestIssueModel(TestCase):

    @classmethod
    def setUpClass(cls):
        """Prerequisite for the following tests on the database
        """
        cls.member = Member(user_email='localhost@gmail.com', debt=10)
        db.session.add(cls.member)
        db.session.commit()
        cls.issue = Issues(isbn=123, user=cls.member.id, fee=100)

    def test_valid_entry(self) -> None:
        self.assertIsInstance(self.issue, Issues)

    def invalid() -> None:
        """Raise error
        """
        Issues(isbn=123123)

    def test_invalid_entry(self) -> None:
        """Assert error on invalid entry
        """
        self.assertRaises(TypeError, self.invalid)

    @classmethod
    def tearDownClass(cls):
        """Clear out db insertions post tests
        """
        db.session.delete(cls.member)
        db.session.commit()
