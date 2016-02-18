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
    personUrlSafe = ndb.StringProperty()
    image = ndb.StringProperty()
    status = ndb.StringProperty()


class RegisterMessage(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('title') or not received_json_data.get('text') or not received_json_data.get('status'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data.get('personUrlSafe'):
                response_data['status'] = 'MESSAGE SHOULD BE BOUND WITH PERSON'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')

            else:
                keyUser = user.getUserKey(user.get_id())
                msg = Message(
                    title=received_json_data.get('title'),
                    text=received_json_data.get('text'),
                    personUrlSafe=received_json_data.get('personUrlSafe'),
                    image=received_json_data.get('image'),
                    status=received_json_data.get('status')
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
                                   "personUrlSafe": msg.personUrlSafe,
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
                                   "personUrlSafe": msg.personUrlSafe,
                                   "urlsafe": msg.urlsafe,
                                   "status": msg.status}

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
            status = received_json_data.get('status')
            personUrlSafe = received_json_data.get('personUrlSafe')

            if title:
                message.title = received_json_data.get('title')
            if text:
                message.text = received_json_data.get('text')
            if image:
                message.image = received_json_data.get('image')
            if status:
                message.status = received_json_data.get('status')
            if personUrlSafe:
                message.personUrlSafe = received_json_data.get('personUrlSafe')

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


