import webapp2
import json
from datetime import datetime
from models.baseClass import BaseClass, BaseClassAuth
from google.appengine.ext import ndb
from models.authentication import AuthMethods, AuthMethodsResponse
from models.message import Message
from models.imagecloud import ImageCloudManager
import logging

class PersonInfo(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=False)
    image = ndb.StringProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    exibitionName = ndb.StringProperty()
    unityName = ndb.StringProperty()
    calling = ndb.StringProperty()

class RegisterPerson(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('firstname'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('lastname'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('exibitionName'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('image'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('unityName'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('calling'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False

            else:
                if received_json_data.get('thisDate'):
                    nowTime = received_json_data.get('thisDate')
                    nowTime = datetime.strptime(nowTime, "%d/%m/%Y %H:%M:%S")
                else:
                    nowTime = datetime.now()

                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))

                person = PersonInfo(
                    firstname=received_json_data.get('firstname'),
                    lastname=received_json_data.get('lastname'),
                    exibitionName=received_json_data.get('exibitionName'),
                    image=imageUploaded,
                    unityName=received_json_data.get('unityName'),
                    calling=received_json_data.get('calling'),
                    dateCreation = nowTime
                )
                person.put()
                response_data['message'] = 'Success registering Person'.decode('latin-1')
                response_data['intern'] = True
        except:
            response_data['message'] = 'Error registering Person'.decode('latin-1')
            response_data['intern'] = False


class LoadPersonList(BaseClass):
    def handle(self, response_data):
        try:
            jsonPerson = {}
            jsonPersonList = []
            query = PersonInfo.query().order(PersonInfo.dateCreation)
            personlist = query.fetch()
            for person in personlist:
                if person.key.id():
                    person.id = person.key.id()

                if person.key.urlsafe():
                    person.urlsafe = person.key.urlsafe()

                    jsonPerson = {"id": person.id,
                                   "firstname": person.firstname,
                                   "lastname": person.lastname,
                                   "image": person.image,
                                   "exibitionName": person.exibitionName,
                                   "unityName": person.unityName,
                                   "calling": person.calling}

                    jsonPersonList.append(jsonPerson)

            response_data = jsonPersonList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting person list'.decode('latin-1')


class UpdatePerson(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            response_data['intern'] = False
            id = received_json_data.get('id')
            person = PersonInfo.get_by_id(id)

            firstname = received_json_data.get('firstname')
            lastname = received_json_data.get('lastname')
            exibitionName = received_json_data.get('exibitionName')
            unityName = received_json_data.get('unityName')
            calling = received_json_data.get('calling')

            if lastname:
                person.lastname = received_json_data.get('lastname')
            if firstname:
                person.firstname = received_json_data.get('firstname')
            if exibitionName:
                person.exibitionName = received_json_data.get('exibitionName')
            if received_json_data.get('image'):
                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                person.image = imageUploaded
            if unityName:
                person.unityName = received_json_data.get('unityName')    
            if calling:
                person.calling = received_json_data.get('calling')    

            person.put()

            response_data['message'] = 'Success updating person'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error updating person'.decode('latin-1')
            response_data['intern'] = False


class DropPerson(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            id = received_json_data.get('id')

            query = Message.query().order()
            messagelist = query.fetch()
            allow_delete = True
            for message in messagelist:
                if int(message.person_id) == id:
                    allow_delete = False
                    break
            if allow_delete:
                person = PersonInfo.get_by_id(id)
                key = person.key
                key.delete()
                response_data['message'] = 'Success droping person'.decode('latin-1')
                response_data['intern'] = 'OK'
            else:
                response_data['message'] = 'Success droping person'.decode('latin-1')
                response_data['intern'] = 'NOT_ALLOWED'
        except Exception as e:
            raise e
            
            
class ClientLoadPerson(BaseClass):
    def handle(self, response_data):
        try:
            id = int(self.request.get('id'))
            person = PersonInfo.get_by_id(id)
            
            jsonPerson = {"firstname": person.firstname,
                           "lastname": person.lastname,
                           "image": person.image,
                           "exibitionName": person.exibitionName,
                           "unityName": person.unityName,
                           "calling": person.calling}
    
    
            response_data = jsonPerson
            self.response.out.write(json.dumps(response_data))
        except Exception as e:
            logging.critical('ERROR LOADING CLIENT PERSON')
            raise e

         
            