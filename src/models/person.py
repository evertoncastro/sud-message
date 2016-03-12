import webapp2
import json
from datetime import datetime
from models.baseClass import BaseClass, BaseClassAuth
from google.appengine.ext import ndb
from models.authentication import AuthMethods, AuthMethodsResponse
from models.unity import Unity

class PersonInfo(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=False)
    image = ndb.StringProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    exibitionName = ndb.StringProperty()
    unityName = ndb.StringProperty()
    unityNumber = ndb.StringProperty()

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
            elif not received_json_data.get('unityNumber'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False

            else:
                if received_json_data.get('thisDate'):
                    nowTime = received_json_data.get('thisDate')
                    nowTime = datetime.strptime(nowTime, "%d/%m/%Y %H:%M:%S")
                else:
                    nowTime = datetime.now()

                person = PersonInfo(
                    firstname=received_json_data.get('firstname'),
                    lastname=received_json_data.get('lastname'),
                    exibitionName=received_json_data.get('exibitionName'),
                    image=received_json_data.get('image'),
                    unityName=received_json_data.get('unityName'),
                    unityNumber=received_json_data.get('unityNumber'),
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
            unityNumber = self.request.get('unityNumber')
            jsonPerson = {}
            jsonPersonList = []
            query = PersonInfo.query(PersonInfo.unityNumber==unityNumber).order(PersonInfo.dateCreation)
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
                                   "personUrlSafe": person.urlsafe,
                                   "unityName": person.unityName,
                                   "unityNumber": person.unityNumber}

                    jsonPersonList.append(jsonPerson)

            response_data = jsonPersonList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting person list'.decode('latin-1')


# class LoadPersonList(BaseClass):
#     def handle(self, response_data):
#         try:
#             jsonPerson = {}
#             jsonPersonList = []
#             query = PersonInfo.query().order(PersonInfo.dateCreation)
#             personlist = query.fetch()
#             for person in personlist:
#                 if person.key.id():
#                     person.id = person.key.id()
#
#                 if person.key.urlsafe():
#                     person.urlsafe = person.key.urlsafe()
#
#                     jsonPerson = {"id": person.id,
#                                    "firstname": person.firstname,
#                                    "lastname": person.lastname,
#                                    "image": person.image,
#                                    "exibitionName": person.exibitionName,
#                                    "personUrlSafe": person.urlsafe,
#                                    "unityName": person.unityName}
#
#                     jsonPersonList.append(jsonPerson)
#
#             response_data = jsonPersonList
#             self.response.out.write(json.dumps(response_data))
#         except:
#             response_data['message'] = 'Error getting person list'.decode('latin-1')


class UpdatePerson(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            response_data['intern'] = False
            person_urlsafe = received_json_data.get('personUrlSafe')
            person_urlsafe = ndb.Key(urlsafe=person_urlsafe)
            person = person_urlsafe.get()

            firstname = received_json_data.get('firstname')
            lastname = received_json_data.get('lastname')
            exibitionName = received_json_data.get('exibitionName')
            image = received_json_data.get('image')

            if lastname:
                person.lastname = received_json_data.get('lastname')
            if firstname:
                person.firstname = received_json_data.get('firstname')
            if exibitionName:
                person.exibitionName = received_json_data.get('exibitionName')
            if image:
                person.image = received_json_data.get('image')

            person.put()

            response_data['message'] = 'Success updating person'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error updating person'.decode('latin-1')
            response_data['intern'] = False


class DropPerson(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            person_urlsafe = received_json_data.get('urlsafe')
            person_urlsafe = ndb.Key(urlsafe=person_urlsafe)

            person_urlsafe.delete()

            response_data['message'] = 'Success droping person'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error droping person'.decode('latin-1')
            response_data['intern'] = False
            
            
class ClientLoadPerson(BaseClass):
    def handle(self, response_data):
        try:
            person_urlsafe = self.request.get('personUrlSafe')
            person_urlsafe = ndb.Key(urlsafe=person_urlsafe)
            person = person_urlsafe.get()
            
            jsonPerson = {"firstname": person.firstname,
                           "lastname": person.lastname,
                           "image": person.image,
                           "exibitionName": person.exibitionName,
                           "unityName": person.unityName}
    
    
            response_data = jsonPerson
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting person info'.decode('latin-1')
         
            