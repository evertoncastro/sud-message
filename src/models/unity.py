from google.appengine.ext import ndb
from models.baseClass import BaseClass
from models.authentication import AuthMethods, AuthMethodsResponse
import json
import webapp2


class Unity(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty()
    image = ndb.StringProperty()
    status = ndb.StringProperty()

class RegisterUnity(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('name'):
                response_data['status'] = 'UNITY INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            if not received_json_data.get('image'):
                response_data['status'] = 'UNITY INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            if not received_json_data.get('status'):
                response_data['status'] = 'UNITY INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')

            else:
                unity = Unity(
                    name=received_json_data.get('name'),
                    image=received_json_data.get('image'),
                    status=received_json_data.get('status')
                )
                unity.put()
                response_data['message'] = 'Success registering unity'.decode('latin-1')
                response_data['intern'] = True
        except:
            response_data['message'] = 'Error registering unity'.decode('latin-1')
            response_data['intern'] = False


class LoadUnityList(BaseClass):
    def handle(self, response_data):
        try:
            jsonUnity = {}
            jsonUnityList = []
            query = Unity.query().order(Unity.dateCreation)
            unityList = query.fetch()

            for unity in unityList:
                if unity.key.id():
                    unity.id = unity.key.id()

                if unity.key.urlsafe():
                    unity.urlsafe = unity.key.urlsafe()

                    dateCreation = unity.dateCreation.strftime('%d/%m/%Y')

                    jsonUnity = {"id": unity.id,
                                   "name": unity.name,
                                   "image": unity.image,
                                   "urlsafe": unity.urlsafe,
                                   "status": unity.status,
                                   "dateCreation": dateCreation}

                    jsonUnityList.append(jsonUnity)

            response_data = jsonUnityList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting unity list'.decode('latin-1')



class UpdateUnity(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            unity_urlsafe = received_json_data.get('urlsafe')
            unity_urlsafe = ndb.Key(urlsafe=unity_urlsafe)
            unity = unity_urlsafe.get()

            name = received_json_data.get('name')
            image = received_json_data.get('image')
            status = received_json_data.get('status')

            if name:
                unity.name = received_json_data.get('name')
            if image:
                unity.image = received_json_data.get('image')
            if status:
                unity.status = received_json_data.get('status')

            unity.put()

            response_data['message'] = 'Success updating unity'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error updating unity'.decode('latin-1')
            response_data['intern'] = False


