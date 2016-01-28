# coding=utf-8
import os
import webapp2
import jinja2
from google.appengine.ext.webapp.util import run_wsgi_app
from models.message import Message, RegisterMessage, LoadMessage, UpdateMessage
from models.user import RegisterUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class PostHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/create_message.html')
        self.response.write(template.render())

    def post(self):
        msg = Message(
                name=self.request.get('name'),
                email=self.request.get('email'),
                message=self.request.get('message'),
                image=self.request.get('image')
        )
        msg.put()
        self.redirect('/loadMessage')

mapeamento = [
    ('/', PostHandler),
    ('/loadMessage', LoadMessage),
    ('/registerMessage', RegisterMessage),
    ('/updateMessage', UpdateMessage),
    ('/registerUser', RegisterUser)
]

app = webapp2.WSGIApplication(mapeamento, debug=True)
run_wsgi_app(app)
