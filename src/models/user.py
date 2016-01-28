from models.baseClass import BaseClass
import webapp2_extras.appengine.auth.models
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
                                         name=received_json_data['name']
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