
from typing import Dict, List
from flask.views import MethodView
from config import app, db
from flask import (
    render_template, session, g, request, redirect, url_for, Response
)
from .models import Admin
import jwt
import os
import requests
from .utils import *

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


class LoginView(MethodView):
    """ This class is to handle login (limited to admins)"""

    def __init__(self, template_name_get) -> None:
        self.template_name_get = template_name_get

    def get(self) -> None:
        """This function is used to render login template"""
        session.pop("user_email", None)
        return render_template(self.template_name_get), 200

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
                return redirect(url_for('home'), 302)
            else:
                return render_template(self.template_name_get, error='Invalid password'), 401
        return render_template(self.template_name_get, error='Invalid User'), 401


class HomeView(MethodView):
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
            return render_template(self.template_name), 200

        return redirect('/', 302)


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
            return render_template(self.template_name), 200
        return redirect('/', 302)

    def post(self) -> render_template:
        """
        Issue Books utilizing the given api
        """
        if g.user:
            try:
                debt = int(request.form.get('debt'))
                email = request.form.get('email')
                isbn = request.form.get('isbn')

            except Exception as e:
                print(e)
                return render_template(self.template_name)

            params = {
                "isbn": isbn
            }

            response = pool_request.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if result := check_errors(data=data):
                    if not isinstance(result, dict):
                        return render_template(self.template_name, not_available=True)
            else:
                return render_template(self.template_name, not_available=True), 200

            if check_availability(isbn=isbn, email=email) is False:
                return render_template(self.template_name, taken=True), 200

            if status := issue_book(user_email=email, isbn=isbn, debt=debt):
                if status == 'debt':
                    return render_template(self.template_name, debt=True), 200
                hash = jwt.encode(data, os.getenv(
                    "SECRET_KEY"))
                return redirect(url_for('success', hash=hash), code=302)

        return redirect('/issue', 302)


class CallBack(MethodView):
    """
    Class for successful issue
    """

    def __init__(self, template_name: str) -> None:
        self.template_name = template_name

    def get(self, hash: str) -> render_template:
        """Renders page post issue

        Args:
            hash (str): details of the book issued

        Returns:
            render_template
        """
        if g.user:

            payload = jwt.decode(hash, os.getenv(
                "SECRET_KEY"), algorithms='HS256')

            try:
                search_status = payload['search']
                if search_status:
                    title = payload['message'][0]['title']
                    isbn = payload['message'][0]['isbn']
                    return render_template(self.template_name, search=search_status, isbn=isbn, title=title), 200
            except Exception as e:
                print(e)

            try:
                title = payload['message'][0]['title']
                return render_template(self.template_name, book_name=title), 200

            except Exception as e:
                email, isbn = payload['email'], payload['isbn']
                return render_template(self.template_name, delete=True, isbn=isbn, email=email), 200

        return redirect('/', 302)


class ReturnView(MethodView):
    """
    Class to handle book returns
    """

    def __init__(self, template_name: str) -> None:
        self.template_name = template_name

    def get(self) -> render_template:
        if g.user:
            return render_template(self.template_name), 200
        return redirect('/', 302)

    def post(self) -> render_template:
        """Get form data

        Returns:
            render_template
        """
        if g.user:
            try:
                isbn = request.form.get('isbn')
                email = request.form.get('email')
            except Exception as e:
                print(e)
                return render_template(self.template_name)
            if return_books(isbn=isbn, email=email) is True:

                payload = {
                    "isbn": isbn,
                    "email": email
                }

                hash = jwt.encode(payload, os.getenv(
                    "SECRET_KEY"), algorithm='HS256')
                return redirect(url_for('success', returned=isbn, hash=hash), 302)
            return render_template(self.template_name, delete=True), 400

        return redirect('/', 302)


class Search(MethodView):
    """View for searching books by name and author
    """

    def __init__(self, template_name: str) -> None:
        self.template_name = template_name

    def get(self) -> render_template:
        """Render page for logged in users
        """
        if g.user:
            return render_template(self.template_name), 200
        return redirect('/', code=302)

    def post(self) -> None:
        """Handle form data
        """
        if g.user:
            try:
                author = request.form.get('author')
                title = request.form.get('title')
            except Exception as e:
                return render_template(self.template_name), 400

            params = {
                "author": author,
                "title": title
            }

            response = pool_request.get(url, params=params)
            if response.status_code == 200:
                data = response.json()

                if result := check_errors(data):
                    if not isinstance(result, dict):
                        return render_template(self.template_name, not_found=True), 400

                data['search'] = True
                hash = jwt.encode(data, os.getenv('SECRET_KEY'))
                return redirect(url_for('success', hash=hash), code=302)

        return redirect('/', 302)
