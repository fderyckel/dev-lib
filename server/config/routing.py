from flask.views import MethodView
from config import app, db
from flask import render_template, session, g, request, redirect, url_for
from .models import Admin, Issues

db.create_all()
db.session.commit()

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


class Issue(MethodView):
    """
    Class to handle Book issues
    """
    pass

class Return(MethodView):
    pass
