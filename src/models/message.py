import webapp2
import json
from google.appengine.ext import db
from models.baseClass import BaseClass


class Message(db.Model):
    user_name = db.StringProperty(required=True)
    email = db.EmailProperty()
    message = db.TextProperty(required=True)


class HandleMessage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<ul>')
        for msg in Message.all():
            self.response.out.write('<li>' + unicode(msg.message) + '</li>')
        self.response.out.write('</ul>')


class RegisterMessage(BaseClass):
    def handle(self, received_json_data, response_data):
        try:
            msg = Message(
                    user_name=received_json_data.get('user_name'),
                    email=received_json_data.get('email'),
                    message=received_json_data.get('message')
            )
            msg.put()
            response_data['message'] = 'Success registering message'.decode('latin-1')
        except:
            response_data['message'] = 'Error registering message'.decode('latin-1')


