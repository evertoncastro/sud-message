from models.baseClass import BaseClass
from models.message import Message
from models.events import Event
from datetime import datetime
import json
import logging

class ClientLoadBanner(BaseClass):
    def handle(self, response_data):
        try:
            message_banners = ClientLoadBanner.load_message_banner()
            event_banners = ClientLoadBanner.load_event_banner()

            response_data = event_banners+message_banners
            self.response.out.write(json.dumps(response_data))
        except Exception as e:
            logging.critical('ERROR LOADING CLIENT BANNER')
            raise e

    @staticmethod
    def load_message_banner():
        try:
            query = Message.query(Message.status == 1, Message.display == 'banner')
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
                                   "dateCreation": dateCreation,
                                   "type": 'message'}

                    jsonMessageList.append(jsonMessage)

            return jsonMessageList
        except Exception as e:
            logging.critical('ERROR LOADING CLIENT BANNER MESSAGES')
            raise e

    @staticmethod
    def load_event_banner():
        try:
            currentDate = datetime.now()
            query = Event.query(Event.date >= currentDate).order(Event.date)

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
                               "display": event.display,
                               "type": 'event'}

                if event.display == 'banner':
                    jsonEventList.append(jsonEvent)

            return jsonEventList
        except Exception as e:
            logging.critical('ERROR LOADING CLIENT BANNER EVENTS: '+e.message)
            raise e