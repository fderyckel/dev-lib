from unittest import TestCase
from config.models import Admin

class TestAdminModel(TestCase):
    def test_valid_entry(self):
        user = Admin(email='testuser@localhost.com', password='testpassword')
        self.assertIsInstance(user, Admin)
        
    @staticmethod
    def create_invalid():
        user = Admin('testuser@localhost.com')
        
    def test_invalid_entry(self):
        self.assertRaises(TypeError, )