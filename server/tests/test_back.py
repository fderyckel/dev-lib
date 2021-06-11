from unittest import TestCase
import requests
import time

from werkzeug.wrappers import response

pool = requests.Session()


class TestLogin(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:5000/'

    def test_login_invalid_credentials(self) -> None:
        """Test invalid password assert statuscode 401
           Unauthorized 
        """
        body = {
            "email": "libuser@localhost.com",
            "password": "libuserad"
        }
        response = pool.post(self.url, data=body)
        self.assertEqual(response.status_code, 401)

    def test_login_valid_credentials(self) -> None:
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

    def test_login_invalid_user(self) -> None:
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
        """Log user out post tests
        """
        response = pool.get(cls.url)


class TestIssueUnauthorized(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://localhost:5000/issue'

    def test_unauthorized(self) -> None:
        """Assert redirection to login page
        """

        response = pool.get(self.url)
        codes = [code.status_code for code in response.history]
        self.assertIn(302, codes)

    @classmethod
    def tearDownClass(cls):
        """Log user out post tests
        """
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

    def test_valid_access(self) -> None:
        """Assert access to authenticated users
        """
        url = 'http://localhost:5000/issue'
        response = pool.get(url)
        self.assertEqual(response.status_code, 200)
        codes = [code.status_code for code in response.history]
        self.assertNotIn(302, codes)

    def test_issue_valid(self):
        """Test valid issue assert redirection to success page
           post valid issue remove issue from db post successful
           redirection
        """
        data = {
            "email": "testuser@localhost.com",
            "isbn": "184416411X",
            "debt": 100
        }

        url = 'http://localhost:5000/issue'
        response = pool.post(url, data=data)
        codes = [code.status_code for code in response.history]
        self.assertIn(302, codes)

        url = 'http://localhost:5000/return'
        data = {
            "email": "testuser@localhost.com",
            "isbn": "184416411X"
        }
        response = pool.post(url, data=data)
        codes = [code.status_code for code in response.history]
        self.assertIn(302, codes)

    @classmethod
    def tearDownClass(cls):
        """log user out post all tests
           (remove user from session)
        """
        url = 'http://localhost:5000/'
        pool.get(url)


class TestReturn(TestCase):
    pass
