from google.appengine.ext import ndb
from models.baseClass import BaseClass
from models.authentication import AuthMethods, AuthMethodsResponse
import json
import logging
import webapp2


class Message(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    title = ndb.StringProperty()
    text = ndb.StringProperty()
    userGlobalInfoUrlSafe = ndb.StringProperty()
    image = ndb.StringProperty()


class RegisterMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('title') or not received_json_data.get('text'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data.get('userGlobalInfoUrlSafe'):
                response_data['status'] = 'MESSAGE SHOULD BE BOUND WITH USER GLOBAL INFO'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            else:
                keyUser = user.getUserKey(user.get_id())
                msg = Message(
                    title=received_json_data.get('title'),
                    text=received_json_data.get('text'),
                    userGlobalInfoUrlSafe=received_json_data.get('userGlobalInfoUrlSafe'),
                    image=received_json_data.get('image'),
                    parent=keyUser
                )
                msg.put()
                response_data['message'] = 'Success registering message'.decode('latin-1')
        except:
            response_data['message'] = 'Error registering message'.decode('latin-1')


class LoadMessageByUser(AuthMethodsResponse):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            id_user = user.get_id()
            jsonMessage = {}
            jsonMessageList = []
            messagelist = Message.query(ancestor=user.getUserKey(id_user)).fetch()
            for msg in messagelist:
                if msg.key.id():
                    msg.id = msg.key.id()

                if msg.key.urlsafe():
                    msg.urlsafe = msg.key.urlsafe()

                    jsonMessage = {"id": msg.id,
                                   "title": msg.title,
                                   "text": msg.text,
                                   "image": msg.image,
                                   "userGlobalInfoUrlSafe": msg.userGlobalInfoUrlSafe,
                                   "urlsafe": msg.urlsafe}

                    jsonMessageList.append(jsonMessage)

            response_data = jsonMessageList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting message'.decode('latin-1')


class LoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            jsonMessage = {}
            jsonMessageList = []
            query = Message.query()
            messagelist = query.fetch()
            for msg in messagelist:
                if msg.key.id():
                    msg.id = msg.key.id()

                if msg.key.urlsafe():
                    msg.urlsafe = msg.key.urlsafe()


                    jsonMessage = {"id": msg.id,
                                   "title": msg.title,
                                   "text": msg.text,
                                   "image": msg.image,
                                   "userGlobalInfoUrlSafe": msg.userGlobalInfoUrlSafe,
                                   "urlsafe": msg.urlsafe}

                    jsonMessageList.append(jsonMessage)

            response_data = jsonMessageList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting message'.decode('latin-1')



class UpdateMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            message_urlsafe = received_json_data.get('urlsafe')
            message_urlsafe = ndb.Key(urlsafe=message_urlsafe)
            message = message_urlsafe.get()

            title = received_json_data.get('title')
            text = received_json_data.get('text')
            image = received_json_data.get('image')

            if title:
                message.title = received_json_data.get('title')
            if text:
                message.text = received_json_data.get('text')
            if image:
                message.image = received_json_data.get('image')

            message.put()

            response_data['message'] = 'Success updating message'.decode('latin-1')
        except:
            response_data['message'] = 'Error updating message'.decode('latin-1')


class DropMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            message_urlsafe = received_json_data.get('urlsafe')
            message_urlsafe = ndb.Key(urlsafe=message_urlsafe)

            message_urlsafe.delete()

            response_data['message'] = 'Success droping message'.decode('latin-1')
        except:
            response_data['message'] = 'Error droping message'.decode('latin-1')


# class LoadMessage(BaseClass):
#     def handle(self, response_data):
#         try:
#             jsonMessage = {}
#             jsonMessageList = []
#             query = Message.query()
#             messagelist = query.fetch()
#             for msg in messagelist:
#                 if msg.image:
#                     msg.image = msg.image.encode('base64');
#                 if msg.key.id():
#                     msg.id = msg.key.id()  
#                        
#                 jsonMessage = {"message": msg.message, 
#                                "id": msg.id, 
#                                "name": msg.name, 
#                                "email": msg.email, 
#                                "image": msg.image} 
#                  
#                 jsonMessageList.append(jsonMessage)
#                      
#             response_data = jsonMessageList
#             self.response.out.write(json.dumps(response_data))   
#               
#         except:
#             response_data['message'] = 'Error getting message'.decode('latin-1')  
#             self.response.out.write(json.dumps(response_data))   

