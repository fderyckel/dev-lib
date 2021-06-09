from flask.views import MethodView
from flask import render_template, session, g 
from .models import Admin
class Login(MethodView):
    """ This class is to handle login (limited to admins)"""

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        """This function is used to render login template"""
        return render_template(self.template_name)

    def post(self):
        """[summary]
        """
        pass


class Issue(MethodView):
    pass


class Return(MethodView):
    pass



# @app.before_request
# def security():
#     g.user = None
#     for i in session:
#         print(session[i])
#     if 'user_email' in session:
#         emails = getemail()
#         try:
#             useremail = [email for email in emails if email[0] == session['user_email']][0]
#             g.user = useremail
#         except Exception as e:
#             print("failed")