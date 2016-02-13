# coding=utf-8
import os
import webapp2
import jinja2
from google.appengine.ext.webapp.util import run_wsgi_app
from models.message import RegisterMessage, LoadMessage, LoadMessageByUser, UpdateMessage, DropMessage
from models.user import RegisterUser, DoLogin, UpdateUser, User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class PostHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/create_message.html')
        self.response.write(template.render())

    def post(self):
        email = self.request.get('email'),
        User.create_user(email, unique_properties=['email'],
                        password_raw=self.request.get('password'),
                        email=email,
                        name= self.request.get('name'),
                        image= self.request.get('image'))
       

mapeamento = [
    ('/', PostHandler),
    ('/loadMessage', LoadMessage),
    ('/registerMessage', RegisterMessage),
    ('/updateMessage', UpdateMessage),
    ('/registerUser', RegisterUser),
    ('/doLogin', DoLogin),
    ('/loadMessageByUser', LoadMessageByUser),
    ('/dropMessage', DropMessage),
    ('/updateUser', UpdateUser)
]


app = webapp2.WSGIApplication(mapeamento, debug=True)
run_wsgi_app(app)
