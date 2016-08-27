import webapp2
import json
from datetime import datetime
from models.baseClass import BaseClass, BaseClassAuth
from google.appengine.ext import ndb
from models.authentication import AuthMethods, AuthMethodsResponse
from models.unity import Unity
from imgurpython import ImgurClient
from models.imagecloud import ImageCloudManager
import requests
import logging

class Missionary(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    image = ndb.StringProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    exibitionName = ndb.StringProperty()
    mission = ndb.StringProperty()
    email = ndb.StringProperty()
    address = ndb.StringProperty()
    period_serving = ndb.StringProperty()
    unityName = ndb.StringProperty()
    

class RegisterMissionary(AuthMethods):
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
            elif not received_json_data.get('mission'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('email'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('address'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False
            elif not received_json_data.get('period_serving'):
                response_data['status'] = 'PERSON INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
                response_data['intern'] = False 
        

            else:
                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                
                missionary = Missionary(
                    firstname=received_json_data.get('firstname'),
                    lastname=received_json_data.get('lastname'),
                    exibitionName=received_json_data.get('exibitionName'),
                    image=imageUploaded,
                    unityName=received_json_data.get('unityName'),
                    mission=received_json_data.get('mission'),
                    email=received_json_data.get('email'),
                    address=received_json_data.get('address'),
                    period_serving=received_json_data.get('period_serving')
                )
                missionary.put()
                response_data['message'] = 'Success registering missionary'.decode('latin-1')
                response_data['intern'] = True
        except:
            response_data['message'] = 'Error registering missionary'.decode('latin-1')
            response_data['intern'] = False


class LoadMissionaryList(BaseClass):
    def handle(self, response_data):
        try:
            jsonMissionary = {}
            jsonMissionaryList = []
            query = Missionary.query().order(Missionary.unityName)
            missionaryList = query.fetch()
            for missionary in missionaryList:
                if missionary.key.id():
                    missionary.id = missionary.key.id()

                    jsonMissionary = {"id": missionary.id,
                                   "firstname": missionary.firstname,
                                   "lastname": missionary.lastname,
                                   "exibitionName": missionary.exibitionName,
                                   "mission": missionary.mission,
                                   "email": missionary.email,
                                   "address": missionary.address,
                                   "period_serving": missionary.period_serving,
                                   "image": missionary.image,
                                   "exibitionName": missionary.exibitionName,
                                   "unityName": missionary.unityName}

                    jsonMissionaryList.append(jsonMissionary)

            response_data = jsonMissionaryList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting person list'.decode('latin-1')


class UpdateMissionary(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('id'):
                response_data['intern'] = False
                response_data['message'] = "No id parameter received".decode('latin-1')

            else:
                firstname=received_json_data.get('firstname'),
                lastname=received_json_data.get('lastname'),
                exibitionName=received_json_data.get('exibitionName'),
                unityName=received_json_data.get('unityName'),
                mission=received_json_data.get('mission'),
                email=received_json_data.get('email'),
                address=received_json_data.get('address'),
                period_serving=received_json_data.get('period_serving')
                id = received_json_data.get('id')

                missionary = Missionary.get_by_id(id)

                if missionary:
                    if lastname:
                        missionary.lastname = received_json_data.get('lastname')
                    if firstname:
                        missionary.firstname = received_json_data.get('firstname')
                    if exibitionName:
                        missionary.exibitionName = received_json_data.get('exibitionName')
                    if received_json_data.get('image'):
                        logging.info('CALLING_IMAGE_API')
                        imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                        missionary.image = imageUploaded
                    if unityName:
                        missionary.unityName = received_json_data.get('unityName')
                    if mission:
                        missionary.mission = received_json_data.get('mission')
                    if email:
                        missionary.email = received_json_data.get('email')
                    if address:
                        missionary.address = received_json_data.get('address')
                    if period_serving:
                        missionary.period_serving = received_json_data.get('period_serving')

                        missionary.put()

                        response_data['message'] = 'Success updating missionary'.decode('latin-1')
                        response_data['intern'] = True

                else:
                    response_data['message'] = 'Missionary not found'.decode('latin-1')
                    response_data['intern'] = False

        except:
            response_data['message'] = 'Error updating missionary'.decode('latin-1')
            response_data['intern'] = False


class DeleteMissionary(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('id'):
                response_data['intern'] = False
                response_data['message'] = "No id parameter received".decode('latin-1')
            
            else:    
                id = received_json_data.get('id')
                missionary = Missionary.get_by_id(id)
                key = missionary.key
                if key:      
                    key.delete()
                    response_data['message'] = 'Success deleting missionary'.decode('latin-1')
                    response_data['intern'] = True
        except:
            response_data['message'] = 'Error droping person'.decode('latin-1')
            response_data['intern'] = False
            
            
class ClientLoadMissionaryList(BaseClass):
    def handle(self, response_data):
        try:
            jsonMissionary = {}
            jsonMissionaryList = []
            query = Missionary.query().order(Missionary.unityName)
            missionaryList = query.fetch()
            for missionary in missionaryList:             

                jsonMissionary = {"firstname": missionary.firstname,
                               "lastname": missionary.lastname,
                               "exibitionName": missionary.exibitionName,
                               "mission": missionary.mission,
                               "email": missionary.email,
                               "address": missionary.address,
                               "period_serving": missionary.period_serving,
                               "image": missionary.image,
                               "exibitionName": missionary.exibitionName,
                               "unityName": missionary.unityName}

                jsonMissionaryList.append(jsonMissionary)

            response_data = jsonMissionaryList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting person list'.decode('latin-1')