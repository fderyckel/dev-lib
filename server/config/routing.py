
from flask.views import MethodView
from config import app, db
from flask import render_template, session, g, request, redirect, url_for
from .models import Admin, Issues
import requests

db.create_all()
db.session.commit()
pool_request = requests.Session()


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
        self.url = 'https://frappe.io/api/method/frappe-library'

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
                title = request.form.get('title')
                isbn = int(request.form.get('isnb'))

                params = {
                    "title": title,
                    "isbn": isbn
                }

                response = pool_request.get(self.url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if 'error' in data.keys():
                        return render_template(self.template_name, not_available=True)
                else:
                    return render_template(self.template_name, not_available=True)

                if Issues.query.filter_by(isbn=isbn).first():
                    print("broke here exists")
                    return render_template(self.template_name, not_available=True, taken=True)

                if len(data.json()['message']) > 1:
                    return render_template(self.template_name, multiple=True)

                issue = Issues(user_email=email, isbn=isbn,
                               book_name=title, book_id=int(data['message'][0]['bookID']), debt=debt)

                db.session.add(issue)
                db.session.commit()
                return redirect(url_for('home'))

            except Exception as e:
                print(e)
                return render_template(self.template_name)

        return redirect('/')


class Return(MethodView):
    pass
