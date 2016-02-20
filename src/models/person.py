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

            else:
                nowTime = datetime.now()
                person = PersonInfo(
                    firstname=received_json_data.get('firstname'),
                    lastname=received_json_data.get('lastname'),
                    exibitionName=received_json_data.get('exibitionName'),
                    image=received_json_data.get('image'),
                    unityName=received_json_data.get('unityName'),
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
                                   "personUrlSafe": person.urlsafe,
                                   "unityName": person.unityName}

                    jsonPersonList.append(jsonPerson)

            response_data = jsonPersonList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting person list'.decode('latin-1')


# class LoadPersonByunity(BaseClassAuth):
#     def handle(self, received_json_data, response_data):
#         try:
#             unity_urlsafe = received_json_data.get('unityUrlSafe')
#             jsonPerson = {}
#             jsonPersonList = []
#             personlist = PersonInfo.query(PersonInfo.unityUrlSafe==unity_urlsafe)
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
#                                    "unityUrlSafe": person.unityUrlSafe}
#
#                     jsonPersonList.append(jsonPerson)
#
#             response_data = jsonPersonList
#             self.response.out.write(json.dumps(response_data))
#         except:
#             response_data['message'] = 'Error getting message'.decode('latin-1')


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
            unityName = received_json_data.get('unityName')

            if lastname:
                person.lastname = received_json_data.get('lastname')
            if firstname:
                person.firstname = received_json_data.get('firstname')
            if exibitionName:
                person.exibitionName = received_json_data.get('exibitionName')
            if image:
                person.image = received_json_data.get('image')
            if unityName:
                person.unityName = received_json_data.get('unityName')

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