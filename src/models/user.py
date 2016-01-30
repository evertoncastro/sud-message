from models.baseClass import BaseClass
import webapp2_extras.appengine.auth.models
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
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
        # valid parameters
        if not received_json_data.get('email') or not received_json_data.get('password'):
            response_data['status'] = 'INVALID_PARAMETER'
            response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
        elif not received_json_data['name']:
            response_data['status'] = 'INVALID_PARAMETER'
            response_data['desc'] = "Erro de comunicacao com o servidor".decode('latin-1')
        else:
            isOk = False            
            email = received_json_data['email']                    
                            
            user, props = User.create_user(email, unique_properties=['email'],
                                         password_raw=received_json_data['password'],
                                         email=email,
                                         name=received_json_data['name'],
                                         image=received_json_data['image']
                                         )
            
            if not user:
                response_data['status'] = 'ALREADYEXISTS_USER'
                response_data['desc'] = 'Usuario ja existe'.decode('latin-1')
                response_data['extra'] = props
            else:
                isOk=True
                logging.debug('PROPS: [%s]', str(props.key.id()))
                userTemp = User.get_by_id(props.key.id())
                token = userTemp.create_auth_token(userTemp.get_id())
                logging.debug('TOKEN: [%s]', token);
                response_data['token'] = token                    
            
            if isOk:
                response_data['status'] = 'OK'
                
                
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
            response_data['desc'] = 'Ola {user}, seja bem-vindo!'.format(user=u.name).decode('latin-1')
            response_data['token'] = token

            jsondata = {'name': u.name, 'email': u.email}
            
            response_data['user_data'] = jsondata
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            response_data['status'] = 'INVALID_USERPASSWORD'
            response_data['desc'] = 'E-mail ou senha invalidos'.decode('latin-1')
            logging.info('Login failed for user %s because of %s', email, type(e))