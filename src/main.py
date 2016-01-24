# coding=utf-8
import os
import webapp2
import jinja2
import json
from google.appengine.ext.webapp.util import run_wsgi_app
from models.person import CallPerson
from models.message import Message, RegisterMessage, HandleMessage

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
                user_name=self.request.get('user_name'),
                email=self.request.get('email'),
                message=self.request.get('message')
        )
        msg.put()
        self.redirect('/handleMessage')

mapeamento = [
    ('/', PostHandler),
    ('/handleMessage', HandleMessage),
    ('/getPerson', CallPerson),
    ('/registerMessage', RegisterMessage)
]
app = webapp2.WSGIApplication(mapeamento, debug=True)
run_wsgi_app(app)
