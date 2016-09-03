from google.appengine.ext import ndb
from models.baseClass import BaseClass
from datetime import datetime
from models.authentication import AuthMethods, AuthMethodsResponse
from models.imagecloud import ImageCloudManager
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
    display = ndb.StringProperty()



class RegisterEvent(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data.get('title') or not received_json_data.get('place') or not received_json_data.get('date'):
                response_data['status'] = 'EVENT INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data.get('time') or not received_json_data.get('display'):
                response_data['status'] = 'EVENT INCOMPLETE'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            else:
                imageUploaded = ''
                if received_json_data.get('image'):
                    imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))


                if received_json_data.get('date'):
                    eventDate = received_json_data.get('date')
                    eventDate = datetime.strptime(eventDate, "%d/%m/%Y %H:%M:%S")
                else:
                    eventDate = datetime.now()

                keyUser = user.getUserKey(user.get_id())
                event = Event(
                    title=received_json_data.get('title'),
                    date=eventDate,
                    description=received_json_data.get('description'),
                    time=received_json_data.get('time'),
                    place=received_json_data.get('place'),
                    image=imageUploaded,
                    display=received_json_data.get('display')
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
            jsonEventList = []
            query = Event.query().order(-Event.date)
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
                                   "dateShow": date,
                                   "time": event.time,
                                   "place": event.place,
                                   "image": event.image,
                                   "display": event.display}

                    jsonEventList.append(jsonEvent)

            response_data = jsonEventList
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting event list'.decode('latin-1')


class UpdateEvent(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            id = received_json_data.get('id')
            event = Event.get_by_id(id)

            title = received_json_data.get('title')
            description = received_json_data.get('description')
            date = received_json_data.get('date')
            time = received_json_data.get('time')
            place = received_json_data.get('place')
            display = received_json_data.get('display')

            if title:
                event.title = received_json_data.get('title')
            if description:
                event.description = received_json_data.get('description')
            if date:
                eventDate = received_json_data.get('date')
                eventDate = datetime.strptime(eventDate, "%d/%m/%Y %H:%M:%S")
                event.date = eventDate
            if time:
                event.time = received_json_data.get('time')
            if place:
                event.place = received_json_data.get('place')
            if received_json_data.get('image'):
                imageUploaded = ImageCloudManager().upload(received_json_data.get('image'))
                event.image = imageUploaded
            if display:
                event.display = received_json_data.get('display')    

            event.put()

            response_data['message'] = 'Success updating event'.decode('latin-1')
            response_data['intern'] = True

        except:
            response_data['message'] = 'Error updating event'.decode('latin-1')
            response_data['intern'] = False



class DropEvent(AuthMethods):
    def handle_auth(self, received_json_data, response_data, user):
        try:
            id = received_json_data.get('id')
            event = Event.get_by_id(id)
            key = event.key

            key.delete()

            response_data['message'] = 'Success droping event'.decode('latin-1')
            response_data['intern'] = True
        except:
            response_data['message'] = 'Error droping event'.decode('latin-1')
            response_data['intern'] = False
            
            
class ClientLoadEvent(BaseClass):
    def handle(self, response_data):
        try:
            display = self.request.get('display')
            currentDate = datetime.now()
            query = Event.query(Event.date >= currentDate).order(Event.date)


            jsonEvent = {}
            jsonEventList = []
            eventList = query.fetch()

            for event in eventList:
                if event.key.id():
                    event.id = event.key.id()

                date = event.date.strftime('%d/%m/%Y')

                jsonEvent = {"title": event.title,
                               "description": event.description,
                               "date": date,
                               "dateShow": date,
                               "time": event.time,
                               "place": event.place,
                               "image": event.image,
                               "display": event.display}

                if display:
                    if event.display == display:
                        jsonEventList.append(jsonEvent)
                else:
                    jsonEventList.append(jsonEvent)

            response_data = jsonEventList
            self.response.out.write(json.dumps(response_data))
        except Exception as e:
            logging.critical('ERROR LOADING CLIENT EVENT: '+e.message)
            raise e
            