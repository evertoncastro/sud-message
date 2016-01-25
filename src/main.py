# coding=utf-8
import os
import webapp2
import jinja2
import json
from google.appengine.ext.webapp.util import run_wsgi_app
from models.person import CallPerson
from models.message import Message, RegisterMessage, LoadMessage

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
    ('/getPerson', CallPerson),
    ('/registerMessage', RegisterMessage)
]
app = webapp2.WSGIApplication(mapeamento, debug=True)
run_wsgi_app(app)
