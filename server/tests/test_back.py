from unittest import TestCase
import requests
import time

from werkzeug.wrappers import response

pool = requests.Session()


class TestLogin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:5000/'

    def test_login_invalid_credentials(self):
        body = {
            "email": "libuser@localhost.com",
            "password": "libuserad"
        }
        response = pool.post(self.url, data=body)
        self.assertEqual(response.status_code, 400)

    def test_login_valid_credentials(self):
        body = {
            "email": "libuser@localhost.com",
            "password": "libuser"
        }
        response = pool.post(self.url, data=body)
        code = [code.status_code for code in response.history]
        self.assertIn(302, code)
        self.assertEqual(response.status_code, 200)
        

    def test_login_invalid_user(self):
        body = {
            "email": "randomuser@localhost.com",
            "password": "libuser"
        }
        response = pool.post(self.url, data=body)
        self.assertEqual(response.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        pass


class TestIssue(TestCase):
    pass


class TestReturn(TestCase):
    pass
