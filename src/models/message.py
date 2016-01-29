from google.appengine.ext import ndb
from models.baseClass import BaseClass
from models.authentication import AuthMethods
import json


class Message(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    title = ndb.StringProperty()
    text = ndb.StringProperty()
    userName = ndb.StringProperty()
   
    
#     def saveMessage(self, objMessage, userAuth):
#         try:
#             #keyUser = userAuth.getUserKey(userAuth.get_id())
#             msg = Message(
#                         title='Title',                        
#                         text='Text',
#                         userName=userAuth.get('name')
#             )        
#             msg.put_async() 
#             return msg.name
#         except:
#             objMessage['desc'] = 'Deu erro'.decode('latin-1')  
            

class RegisterMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):    
        keyUser = user.getUserKey(user.get_id())
        msg = Message(
                    title=received_json_data.get('title'),                      
                    text=received_json_data.get('text'),       
                    userName=user.name,
                    parent=keyUser
        )        
        msg.put()
        #name = Message().saveMessage(received_json_data, user)
        response_data['message'] = 'Success registering message'.decode('latin-1')
        response_data['name'] = msg.userName
        
#         except:
#             response_data['message'] = 'Error registering message'.decode('latin-1')         

# class RegisterMessage(AuthMethods):
#     def handle_auth(self, received_json_data, response_data, user):    
#         try:          
#             name = Message().saveMessage(received_json_data, user)
#             response_data['message'] = 'Success registering message'.decode('latin-1')
#             response_data['name'] = name
#         
#         except:
#             response_data['message'] = 'Error registering message'.decode('latin-1')              
    

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
            
            
class UpdateMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data):     
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
        
              
    
            
            
# class RegisterMessage(AuthMethods):
#     def handle_auth(self, received_json_data, response_data, user):       
#         try:           
#             msg = Message(
#                     name=received_json_data.get('name'),
#                     email=received_json_data.get('email'),
#                     message=received_json_data.get('message'),
#                     image = received_json_data.get('image')
#             )
#          
#             msg.put()
#             response_data['message'] = 'Success registering message'.decode('latin-1')
#         except:
#             response_data['message'] = 'Error registering message'.decode('latin-1')
            


