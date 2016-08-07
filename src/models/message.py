from google.appengine.ext import ndb
from models.baseClass import BaseClass
from models.authentication import AuthMethods, AuthMethodsResponse
from models.imagecloud import ImageCloudManager, ErrorUploadImage
from datetime import datetime
import json
import logging
import webapp2


class Message(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=False)
    title = ndb.StringProperty()
    text = ndb.TextProperty()
    personUrlSafe = ndb.StringProperty()
    image = ndb.StringProperty()
    status = ndb.StringProperty()
    display = ndb.StringProperty()

class RegisterMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('title') or not received_json_data.get('text') or not received_json_data.get('status'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data.get('personUrlSafe')or not received_json_data.get('display'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')

            else:
                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                
                if received_json_data.get('thisDate'):
                    nowTime = received_json_data.get('thisDate')
                    nowTime = datetime.strptime(nowTime, "%d/%m/%Y %H:%M:%S")
                else:
                    nowTime = datetime.now()

                keyUser = user.getUserKey(user.get_id())
                msg = Message(
                    title=received_json_data.get('title'),
                    text=received_json_data.get('text'),
                    personUrlSafe=received_json_data.get('personUrlSafe'),
                    image=imageUploaded,
                    status=received_json_data.get('status'),
                    display=received_json_data.get('display'),
                    dateCreation=nowTime
                )
                msg.put()
                response_data['message'] = 'Success registering message'.decode('latin-1')
                response_data['intern'] = True
        except:
            if ErrorUploadImage:
                response_data['message'] = 'Error uploading image'.decode('latin-1')
                response_data['intern'] = False
            else:    
                response_data['message'] = 'Error registering message'.decode('latin-1')
                response_data['intern'] = False


class LoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            unityNumber = self.request.get('unityNumber')
            jsonMessage = {}
            jsonMessageList = []
            query = Message.query().order(-Message.dateCreation)
            messagelist = query.fetch()

            for msg in messagelist:
                if msg.key.id():
                    msg.id = msg.key.id()

                if msg.key.urlsafe():
                    msg.urlsafe = msg.key.urlsafe()

                    dateCreation = msg.dateCreation.strftime('%d/%m/%Y')

                    jsonMessage = {"id": msg.id,
                                   "title": msg.title,
                                   "text": msg.text,
                                   "image": msg.image,
                                   "personUrlSafe": msg.personUrlSafe,
                                   "urlsafe": msg.urlsafe,
                                   "status": msg.status,
                                   "display": msg.display,
                                   "dateCreation": dateCreation}

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
            newimage = received_json_data.get('newimage')
            status = received_json_data.get('status')
            display = received_json_data.get('display')
            personUrlSafe = received_json_data.get('personUrlSafe')

            if title:
                message.title = received_json_data.get('title')
            if text:
                message.text = received_json_data.get('text')
            if image and newimage:                
                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                message.image = imageUploaded
            if status:
                message.status = received_json_data.get('status')
            if display:
                message.display = received_json_data.get('display')    
            if personUrlSafe:
                message.personUrlSafe = received_json_data.get('personUrlSafe')

            message.put()

            response_data['message'] = 'Success updating message'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error updating message'.decode('latin-1')
            response_data['intern'] = False


class DropMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            message_urlsafe = received_json_data.get('urlsafe')
            message_urlsafe = ndb.Key(urlsafe=message_urlsafe)

            message_urlsafe.delete()

            response_data['message'] = 'Success droping message'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error droping message'.decode('latin-1')
            response_data['intern'] = False


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
                                   "personUrlSafe": msg.personUrlSafe,
                                   "urlsafe": msg.urlsafe}

                    jsonMessageList.append(jsonMessage)

            response_data = jsonMessageList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting message'.decode('latin-1')
            
            
class ClientLoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            unityNumber = self.request.get('unityNumber')
            display = self.request.get('display')
            status = '1'
            
            if display:
                query = Message.query(Message.status==status, Message.display==display).order(-Message.dateCreation)
            else:    
                query = Message.query(Message.status==status).order(-Message.dateCreation)
            
            messagelist = query.fetch()
            jsonMessage = {}
            jsonMessageList = []

            for msg in messagelist:
                if msg.key.id():
                    msg.id = msg.key.id()

                if msg.key.urlsafe():
                    msg.urlsafe = msg.key.urlsafe()

                    dateCreation = msg.dateCreation.strftime('%d/%m/%Y')

                    jsonMessage = {"id": msg.id,
                                   "title": msg.title,
                                   "text": msg.text,
                                   "image": msg.image,
                                   "personUrlSafe": msg.personUrlSafe,
                                   "urlsafe": msg.urlsafe,
                                   "status": msg.status,
                                   "display": msg.display,
                                   "dateCreation": dateCreation}

                    jsonMessageList.append(jsonMessage)

            response_data = jsonMessageList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting message'.decode('latin-1')            