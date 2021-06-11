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
        """Test invalid password assert statuscode 401
           Unauthorized 
        """
        body = {
            "email": "libuser@localhost.com",
            "password": "libuserad"
        }
        response = pool.post(self.url, data=body)
        self.assertEqual(response.status_code, 401)

    def test_login_valid_credentials(self):
        """Test valid login credentials assert redirection to
           home page.
        """
        body = {
            "email": "libuser@localhost.com",
            "password": "libuser"
        }
        response = pool.post(self.url, data=body)
        code = [code.status_code for code in response.history]
        self.assertIn(302, code)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_user(self):
        """Tests invalid login credentials assert status 401 
           unauthorized
        """
        body = {
            "email": "randomuser@localhost.com",
            "password": "libuser"
        }
        response = pool.post(self.url, data=body)
        self.assertEqual(response.status_code, 401)

    @classmethod
    def tearDownClass(cls):
        response = pool.get(cls.url)



class TestIssueUnauthorized(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:5000/issue'

    def test_unauthorized(self):
        """Assert redirection to login page
        """

        response = pool.get(self.url)
        codes = [code.status_code for code in response.history]
        self.assertIn(302, codes)

    @classmethod
    def tearDownClass(cls):
        url = 'http://localhost:5000/'
        pool.get(url)


class TestIssueAuthorized(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Log user in before testing issue
        """
        url = 'http://localhost:5000/'
        data = {
            "email": "libuser@localhost.com",
            "password": "libuser"
        }
        pool.post(url, data)

    def test_valid_login(self):
        url = 'http://localhost:5000/issue'
        response = pool.get(url)
        self.assertEqual(response.status_code, 200)
        codes = [code.status_code for code in response.history]
        self.assertNotIn(302, codes)

    @classmethod
    def tearDownClass(cls):
        """log user out post all tests
           (remove user from session)
        """
        url = 'http://localhost:5000/'
        pool.get(url)


class TestReturn(TestCase):
    pass
