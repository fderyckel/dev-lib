
from flask.views import MethodView
from config import app, db
from flask import render_template, session, g, request, redirect, url_for
from .models import Admin
import jwt
import os
import requests
from .utils import check_errors, check_availability, issue_book

db.create_all()
db.session.commit()
pool_request = requests.Session()
url = 'https://frappe.io/api/method/frappe-library'


@app.before_request
def security():
    g.user = None
    if 'user_email' in session:
        emails = list(map(str, Admin.query.all()))
        try:
            useremail = [email for email in emails if email
                         == session['user_email']][0]

            g.user = useremail
        except Exception as e:
            print(e)


class Login(MethodView):
    """ This class is to handle login (limited to admins)"""

    def __init__(self, template_name_get) -> None:
        self.template_name_get = template_name_get

    def get(self) -> None:
        """This function is used to render login template"""
        session.pop("user_email", None)
        return render_template(self.template_name_get)

    def post(self) -> None:
        """ 
        This method is to handle all post data sent via the forms
        And attaches user to session if credentials are correct
        """
        email = request.form.get('email')
        password = request.form.get('password')

        user = Admin.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                session['user_email'] = email
                return redirect(url_for('home'))
            else:
                return render_template(self.template_name_get, error='Invalid password')
        return render_template(self.template_name_get, error='Invalid User')


class Home(MethodView):
    """
    This is the intermediate page / home page for the admin users
    """

    def __init__(self, template_name) -> None:
        self.template_name = template_name

    def get(self) -> render_template:
        """ 
        Renders the home page on a get request
        """
        if g.user:
            return render_template(self.template_name)

        return redirect('/')


class IssueView(MethodView):
    """
    Class to handle Book issues
    """

    def __init__(self, template_name) -> None:
        self.template_name = template_name

    def get(self) -> render_template:
        """
        Renders the page if user is logged
        """
        if g.user:
            return render_template(self.template_name)
        return redirect('/')

    def post(self) -> render_template:
        """
        Issue Books utilizing the given api
        """
        if g.user:
            try:
                debt = int(request.form.get('debt'))
                email = request.form.get('email')
                isbn = request.form.get('isnb')

            except Exception as e:
                print(e)
                return render_template(self.template_name)

            params = {
                "isbn": isbn
            }

            hash = jwt.encode(params, os.getenv(
                "SECRET_KEY"))

            response = pool_request.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if result := check_errors(data=data):
                    if not isinstance(result, dict):
                        return render_template(self.template_name, not_available=True)
            else:
                return render_template(self.template_name, not_available=True)

            if check_availability(isbn=isbn) is False:
                return render_template(self.template_name, taken=True)

            if status := issue_book(user_email=email, isbn=isbn, debt=debt) is True:
                return redirect(url_for('success', hash=hash))

            if status == 'debt':
                return render_template(self.template_name, debt=True)

        return redirect('/')


class CallBack(MethodView):
    """
    Class for successful issue
    """

    def __init__(self, template_name: str) -> None:
        self.template_name = template_name

    def get(self, hash: str) -> render_template:
        if g.user:

            payload = jwt.decode(hash, os.getenv(
                "SECRET_KEY"), algorithms='HS256')

            params = {
                "isbn": payload['isbn']
            }
            book_details = pool_request.get(url, params=params)
            if book_details.status_code == 200:
                data = book_details.json()
                if result := check_errors(data):
                    if not isinstance(result, dict):
                        return redirect(url_for('issue'))

                title = data['message'][0]['title']
                return render_template(self.template_name, book_name=title)

            return render_template(redirect(url_for('issue')))
        return redirect('/')


class Return(MethodView):
    pass
