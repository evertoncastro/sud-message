from google.appengine.ext import ndb
from models.baseClass import BaseClass
import json
import logging
import webapp2


class Event(ndb.Model):
    def fakemethod(self):
        return True

class RegisterEvent():
    def fakemethod(self):
        return True

class UpdateEvent():
    def fakemethod(self):
        return True

class DropEvent():
    def fakemethod(self):
        return True

