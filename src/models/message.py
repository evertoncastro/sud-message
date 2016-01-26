import webapp2
import json
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import images
from models.baseClass import BaseClass


class Message(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    image = ndb.BlobProperty();
    

class LoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            jsonMessage = {}
            jsonMessageList = []
            query = Message.query()
            messagelist = query.fetch()
            for msg in messagelist:
                if msg.image:
                    msg.image = msg.image.encode('base64');
                if msg.key.id():
                    msg.id = msg.key.id()  
                       
                jsonMessage = {"message": msg.message, 
                               "id": msg.id, 
                               "name": msg.name, 
                               "email": msg.email, 
                               "image": msg.image} 
                 
                jsonMessageList.append(jsonMessage)
                     
            response_data = jsonMessageList
            self.response.out.write(json.dumps(response_data))   
              
        except:
            response_data['message'] = 'Error getting message'.decode('latin-1')  
            self.response.out.write(json.dumps(response_data))   
            
            
class UpdateMessage(BaseClass):
    def handle(self, received_json_data, response_data):     
        try: 
            message_id = int(received_json_data.get('id'));
            message = Message.get_by_id(message_id)
                 
            message.name = received_json_data.get('name')
            message.email = received_json_data.get('email')
            message.message = received_json_data.get('message')
            
            message.put()
            
            response_data['message'] = 'Success updating message'.decode('latin-1')
        except:
            response_data['message'] = 'Error updating message'.decode('latin-1')
        
              
            

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


