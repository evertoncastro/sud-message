from google.appengine.ext import ndb
from models.baseClass import BaseClass
import json
import logging
import webapp2

class Event(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=False)
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    host = ndb.StringProperty()
    image = ndb.StringProperty()

class RegisterEvent():
    def handle_auth(self, received_json_data, response_data, user):
        try:
            if not received_json_data("title") or not received_json_data("description") or not  received_json_data("host"):
                response_data["status"] = "MESSAGE INCOMPLETE"
                response_data["desc"] = "Um ou mais parametros nao foram enviados corretamente, tente novamente mais tarde".decode("latin-1")
            else:
               event = Event(
                 title=received_json_data.get("title"),
                 description=received_json_data.get("description"),
                 host=received_json_data.get("host")
               )
               if received_json_data.get("image"):
                   event.image = received_json_data.get("image")

               event.put()
               response_data["message"] = "Evento criado com sucesso".decode("latin-1")
               response_data["intern"] = True
        except:
            response_data["message"] = "Algo deu errado no cadastro do evento".decode("latin-1")
            response_data["intern"] = False

class UpdateEvent():
    def fakemethod(self):
        return True

class DropEvent():
    def fakemethod(self):
        return True
