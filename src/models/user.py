from models.baseClass import BaseClass
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from util.Util import Util
from google.appengine.api import mail
import logging

try:
    from ndb import model
except ImportError: # pragma: no cover
    from google.appengine.ext.ndb import model

from google.appengine.ext import ndb

class User(webapp2_extras.appengine.auth.models.User):

    @classmethod
    def getUserKey(cls, user_id):
        user_key = model.Key(cls, user_id)

        return user_key

    @classmethod
    def create_auth_token(cls, user_id):
        """Creates a new authorization token for a given user ID.
        :param user_id:
            User unique ID.
        :returns:
            A string with the authorization token.
        """
        return cls.token_model.create(user_id, 'auth').key.id()

class RegisterUser(BaseClass):

    def handle(self, received_json_data, response_data):
        try:
            # valid parameters
            if not received_json_data.get('email') or not received_json_data.get('password'):
                response_data['status'] = 'INVALID_PARAMETER'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            elif not received_json_data['firstname'] and not received_json_data('lastname'):
                response_data['status'] = 'INVALID_PARAMETER'
                response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
            else:
                isOk = False
                email = received_json_data['email']

                user, props = User.create_user(email, unique_properties=['email'],
                                               password_raw=received_json_data['password'],
                                               email=email,
                                               firstname=received_json_data['firstname'],
                                               lastname=received_json_data['lastname']
                                               )

                if not user:
                    response_data['status'] = 'ALREADYEXISTS_USER'
                    response_data['desc'] = 'Usuario ja existe'.decode('latin-1')
                    response_data['extra'] = props
                else:
                    isOk=True

                    userTemp = User.get_by_id(props.key.id())
                    token = userTemp.create_auth_token(userTemp.get_id())
                    response_data['token'] = token

                    keyUser = userTemp.getUserKey(userTemp.get_id())
                    userGlobalInfo = UserGlobalInfo(
                        image=received_json_data.get('image'),
                        email=received_json_data.get('email'),
                        firstname=received_json_data.get('firstname'),
                        lastname=received_json_data.get('lastname'),
                        parent=keyUser
                    )
                    userGlobalInfo.put()

                if isOk:
                    response_data['status'] = 'OK'
        except:
            response_data['status'] = 'ERROR'
            response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')


class UpdateUser(BaseClass):

    def handle(self, received_json_data, response_data):
        try:
            tokenOrig = received_json_data['token']
            user_id, token = Util().parseToken(tokenOrig)
            user, temp = User.get_by_auth_token(int(user_id), token)

            if not user:
                response_data['status'] = 'NOT_FOUND_USER'
                response_data['desc'] = 'Usuario nao encontrado'.decode('latin-1')
            else:
                firstname = received_json_data['firstname']
                lastname = received_json_data['lastname']
                image = received_json_data['image']

                if firstname:
                    user.firstname = firstname
                if lastname:
                    user.lastname = lastname

                user.put()
                user_id = user.get_id()
                userGlobalInfo = UserGlobalInfo.query(ancestor=user.getUserKey(user_id)).fetch()
                userGlobalInfo = userGlobalInfo[0]
                if image:
                    userGlobalInfo.image = image
                if firstname:
                    userGlobalInfo.firstname = firstname
                if lastname:
                    userGlobalInfo.lastname = lastname

                userGlobalInfo.put()

                response_data['desc'] = 'Usuario atualizado com sucesso'.decode('latin-1')

        except:
            response_data['status'] = 'NOT_FOUND_USER'
            response_data['desc'] = 'Usuario nao encontrado'.decode('latin-1')


class DoLogin(BaseClass):

    def handle(self, received_json_data, response_data):
        email = received_json_data['email']
        password = received_json_data['password']
        try:
            u = User.get_by_auth_password(email, password)
            user_id = u.get_id()
            logging.debug('user_id [%s]', user_id)
            token = u.create_auth_token(user_id)
            response_data['status'] = 'OK'
            #response_data['desc'] = 'Ola {user}, seja bem-vindo!'.format(user=u.firstname).decode('unicode_escape')
            userGlobalInfo = UserGlobalInfo.query(ancestor=u.getUserKey(user_id)).fetch()
            userGlobalInfo = userGlobalInfo[0]
            if userGlobalInfo.key.urlsafe():
                    userGlobalInfo.urlsafe = userGlobalInfo.key.urlsafe()

            response_data['token'] = token
            jsondata = {'firstname': u.firstname, 'lastname': u.lastname,
                        'email': u.email, 'id': user_id, 'image': userGlobalInfo.image, 'userGlobalInfoUrlSafe': userGlobalInfo.urlsafe}

            response_data['user_data'] = jsondata
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            response_data['status'] = 'INVALID_USERPASSWORD'
            response_data['desc'] = 'E-mail ou senha invalidos'.decode('latin-1')
            logging.info('Login failed for user %s because of %s', email, type(e))


class UserGlobalInfo(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    image = ndb.StringProperty()
    email = ndb.StringProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()



