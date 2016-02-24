from google.appengine.ext import ndb
from models.baseClass import BaseClass
from datetime import datetime
from models.authentication import AuthMethods, AuthMethodsResponse
import json
import logging
import webapp2


class Event(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    time = ndb.StringProperty()
    place = ndb.StringProperty()
    image = ndb.StringProperty()
    unityNumber = ndb.StringProperty()


class RegisterEvent(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('title') or not received_json_data.get('place') or not received_json_data.get('date'):
                response_data['status'] = 'MESSAGE INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data.get('time')or not received_json_data.get('unityNumber'):
                response_data['status'] = 'MESSAGE SHOULD BE BOUND WITH PERSON'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            else:
                if received_json_data.get('date'):
                    nowTime = received_json_data.get('date')
                    nowTime = datetime.strptime(nowTime, "%d/%m/%Y %H:%M:%S")
                else:
                    nowTime = datetime.now()

                keyUser = user.getUserKey(user.get_id())
                event = Event(
                    title=received_json_data.get('title'),
                    date=nowTime,
                    description=received_json_data.get('description'),
                    time=received_json_data.get('time'),
                    place=received_json_data.get('place'),
                    image=received_json_data.get('image'),
                    unityNumber=received_json_data.get('unityNumber')
                )

                event.put()
                response_data['message'] = 'Success registering event'.decode('latin-1')
                response_data['intern'] = True
        except:
            response_data['message'] = 'Error registering event'.decode('latin-1')
            response_data['intern'] = False


class LoadEvent(BaseClass):
    def handle(self, response_data):
        try:
            unityNumber = self.request.get('unityNumber')
            jsonEvent = {}
            jsonEventList = []
            query = Event.query(Event.unityNumber==unityNumber).order(Event.date)
            eventList = query.fetch()

            for event in eventList:
                if event.key.id():
                    event.id = event.key.id()

                if event.key.urlsafe():
                    event.urlsafe = event.key.urlsafe()

                    date = event.date.strftime('%d/%m/%Y')

                    jsonEvent = {"id": event.id,
                                   "title": event.title,
                                   "description": event.description,
                                   "date": date,
                                   "time": event.time,
                                   "place": event.place,
                                   "image": event.image,
                                   "unityNumber": event.unityNumber,
                                   "eventUrlSafe": event.urlsafe}

                    jsonEventList.append(jsonEvent)

            response_data = jsonEventList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting event list'.decode('latin-1')



class UpdateEvent():
    def fakemethod(self):
        return True

class DropEvent():
    def fakemethod(self):
        return True

