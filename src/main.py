# coding=utf-8
import os
import webapp2
import jinja2
from google.appengine.ext.webapp.util import run_wsgi_app
from models.message import RegisterMessage, LoadMessage, LoadMessageByUser, UpdateMessage, DropMessage, ClientLoadMessage
from models.user import RegisterUser, DoLogin, UpdateUser, User
from models.person import RegisterPerson, LoadPersonList, UpdatePerson, DropPerson, ClientLoadPerson
from models.unity import UpdateUnity, LoadUnityList, RegisterUnity, LoadFullUnityList
from models.events import RegisterEvent, UpdateEvent, LoadEvent, DropEvent, ClientLoadEvent
from models.missionary import RegisterMissionary, LoadMissionaryList, UpdateMissionary, DeleteMissionary, ClientLoadMissionaryList
from models.contact import GetDeveloperContactList
from models.imagecloud import ImageCloud

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class PostHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world')

    def post(self):
        email = self.request.get('email'),
        User.create_user(email, unique_properties=['email'],
                        password_raw=self.request.get('password'),
                        email=email,
                        name= self.request.get('name'),
                        image= self.request.get('image'))
        

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        admin =  users.is_current_user_admin()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Hi, {}! Administrator: {} </br> (<a href="{}">sign out</a>)'.format(nickname, admin, logout_url)
                
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))        


class Image(webapp2.RequestHandler):
    def get(self):
        ImageCloud().create()

mapping = [
    ('/', PostHandler),
    ('/main_page', MainPage),
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
    ('/loadFullUnityList', LoadFullUnityList),
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
    ('/clientGetDeveloperContactList', GetDeveloperContactList),
    ('/imgur', Image)]


app = webapp2.WSGIApplication(mapping, debug=True)
run_wsgi_app(app)
