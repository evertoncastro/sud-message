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
    person_id = ndb.StringProperty()
    image = ndb.StringProperty()
    status = ndb.IntegerProperty()
    display = ndb.StringProperty()

class RegisterMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('title') or not received_json_data.get('text') or not received_json_data.get('status'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data.get('person_id')or not received_json_data.get('display'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')

            else:
                imageUploaded = ''
                if received_json_data.get('image'):
                    imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                
                if received_json_data.get('thisDate'):
                    nowTime = received_json_data.get('thisDate')
                    nowTime = datetime.strptime(nowTime, "%d/%m/%Y %H:%M:%S")
                else:
                    nowTime = datetime.now()

                msg = Message(
                    title=received_json_data.get('title'),
                    text=received_json_data.get('text'),
                    person_id=str(received_json_data.get('person_id')),
                    image=imageUploaded,
                    status=int(received_json_data.get('status')),
                    display=received_json_data.get('display'),
                    dateCreation=nowTime
                )
                msg.put()
                response_data['message'] = 'Success registering message'.decode('latin-1')
                response_data['intern'] = True

        except Exception as e:
            raise e


class LoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            jsonMessageList = []
            query = Message.query().order(-Message.dateCreation)
            messagelist = query.fetch()

            for msg in messagelist:
                if msg.key.id():
                    msg.id = msg.key.id()

                if msg.key.urlsafe():

                    dateCreation = msg.dateCreation.strftime('%d/%m/%Y')

                    jsonMessage = {"id": msg.id,
                                   "title": msg.title,
                                   "text": msg.text,
                                   "image": msg.image,
                                   "person_id": int(msg.person_id),
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
            id = received_json_data.get('id')
            message = Message.get_by_id(id)

            title = received_json_data.get('title')
            text = received_json_data.get('text')
            status = received_json_data.get('status')
            display = received_json_data.get('display')
            person_id = received_json_data.get('person_id')

            if title:
                message.title = received_json_data.get('title')
            if text:
                message.text = received_json_data.get('text')
            if received_json_data.get('image'):
                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                message.image = imageUploaded
            if status:
                message.status = received_json_data.get('status')
            if display:
                message.display = received_json_data.get('display')    
            if person_id:
                message.person_id = str(received_json_data.get('person_id'))

            message.put()

            response_data['message'] = 'Success updating message'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error updating message'.decode('latin-1')
            response_data['intern'] = False


class DropMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            id = received_json_data.get('id')
            message = Message.get_by_id(id)
            key = message.key
            key.delete()

            response_data['message'] = 'Success droping message'.decode('latin-1')
            response_data['intern'] = True
        except Exception as e:
            raise e

            
class ClientLoadMessage(BaseClass):
    def handle(self, response_data):
        try:
            display = self.request.get('display')
            status = 1
            
            if display:
                query = Message.query(Message.status == status, Message.display==display)
            else:    
                query = Message.query(Message.status == status)

            messagelist = query.fetch()
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
                                   "person_id": msg.person_id,
                                   "status": msg.status,
                                   "display": msg.display,
                                   "dateCreation": dateCreation}

                    jsonMessageList.append(jsonMessage)

            response_data = jsonMessageList
            self.response.out.write(json.dumps(response_data))
        except Exception as e:
            logging.critical('ERROR LOADING CLIENT MESSAGES')
            raise e
