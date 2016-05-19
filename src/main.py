# coding=utf-8
import os
import webapp2
import jinja2
from google.appengine.ext.webapp.util import run_wsgi_app
from models.message import RegisterMessage, LoadMessage, LoadMessageByUser, UpdateMessage, DropMessage, ClientLoadMessage
from models.user import RegisterUser, DoLogin, UpdateUser, User
from models.person import RegisterPerson, LoadPersonList, UpdatePerson, DropPerson, ClientLoadPerson
from models.unity import UpdateUnity, LoadUnityList, RegisterUnity
from models.events import RegisterEvent, UpdateEvent, LoadEvent, DropEvent, ClientLoadEvent
from models.missionary import RegisterMissionary, LoadMissionaryList, UpdateMissionary, DeleteMissionary, ClientLoadMissionaryList
from models.contact import GetDeveloperContactList

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class PostHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/create_message.html')
        self.response.write(template.render())

    def post(self):
        email = self.request.get('email'),
        User.create_user(email, unique_properties=['email'],
                        password_raw=self.request.get('password'),
                        email=email,
                        name= self.request.get('name'),
                        image= self.request.get('image'))


mapping = [
    ('/', PostHandler),
    ('/loadMessage', LoadMessage),
    ('/registerMessage', RegisterMessage),
    ('/updateMessage', UpdateMessage),
    ('/registerUser', RegisterUser),
    ('/doLogin', DoLogin),
    ('/loadMessageByUser', LoadMessageByUser),
    ('/dropMessage', DropMessage),
    ('/updateUser', UpdateUser),
    ('/registerPerson', RegisterPerson),
    ('/loadPersonList', LoadPersonList),
    ('/updatePerson', UpdatePerson),
    ('/dropPerson', DropPerson),
    ('/registerUnity', RegisterUnity),
    ('/loadUnityList', LoadUnityList),
    ('/updateUnity', UpdateUnity),
    ('/registerEvent', RegisterEvent),
    ('/updateEvent', UpdateEvent),
    ('/dropEvent', DropEvent),
    ('/registerMissionary', RegisterMissionary),
    ('/loadMissionaryList', LoadMissionaryList),
    ('/updateMissionary', UpdateMissionary),
    ('/deleteMissionary', DeleteMissionary),
    ('/clientLoadMissionaryList', ClientLoadMissionaryList),
    ('/loadEvent', LoadEvent),
    ('/clientLoadEvent', ClientLoadEvent),
    ('/clientLoadMessage', ClientLoadMessage),
    ('/clientLoadPerson', ClientLoadPerson),
    ('/clientGetDeveloperContactList', GetDeveloperContactList)

]


app = webapp2.WSGIApplication(mapping, debug=True)
run_wsgi_app(app)
