import webapp2
import json
from google.appengine.ext import db
from models.baseClass import BaseClass
from google.appengine.ext import ndb
from google.appengine.api import images
from _codecs import encode



class Message(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    image = ndb.BlobProperty();
    
        

# class HandleMessage(webapp2.RequestHandler):
#     def get(self):
#         query = Message.query()
#         messagelist = query.fetch()
#         self.response.headers.add_header("Access-Control-Allow-Origin", "*")
#         self.response.headers['Content-Type'] = 'application/json'
#         for msg in messagelist:
#             if msg.image:
#                 msg.image = msg.image.encode('base64');
#                 newimage = msg.image;
#                 id = msg.key.id()
#                 newimage = msg.image.encode('base64');
#         
#         self.response.out.write(json.dumps(msg.image)) 

class LoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            newMessage = {}
            query = Message.query()
            messagelist = query.fetch()
            for msg in messagelist:
                if msg.image:
                    msg.image = msg.image.encode('base64');
                if msg.key.id():
                    msg.id = msg.key.id()
                     
                     
            newMessage = {"message": msg.message, "id": msg.id, "name": msg.name, "email": msg.email, "image": msg.image}        
            response_data = newMessage
            self.response.out.write(json.dumps(response_data))   
            
        except:
            response_data['message'] = 'Error registering message'.decode('latin-1')  

class RegisterMessage(BaseClass):
    def handle(self, received_json_data, response_data):
        try:           
            image = received_json_data.get('image')
            msg = Message(
                    name=received_json_data.get('name'),
                    email=received_json_data.get('email'),
                    message=received_json_data.get('message'),
                    image = received_json_data.get('image')
            )
        
            msg.put()
            response_data['message'] = 'Success registering message'.decode('latin-1')
        except:
            response_data['message'] = 'Error registering message'.decode('latin-1')


