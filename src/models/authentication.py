
import logging
from models.baseClass import BaseClass, BaseClassAuth
from models.user import User
from util.Util import Util

class AuthMethods(BaseClass):
    def handle(self, received_json_data, response_data):
        tokenOrig = received_json_data['token']
        
        user_id, token = Util().parseToken(tokenOrig)
        user, temp = User.get_by_auth_token(int(user_id), token)
        
        logging.debug('UserBean [%s] - temp [%s]', str(user), str(temp))
        
        if user:
            self.handle_auth(received_json_data, response_data, user)
        else:
            response_data['status'] = 'INVALID_TOKEN'
            response_data['desc'] = 'Usuario nao autenticado'.decode('latin-1')


class AuthMethodsResponse(BaseClassAuth):
    def handle(self, received_json_data, response_data):
        tokenOrig = received_json_data['token']

        user_id, token = Util().parseToken(tokenOrig)
        user, temp = User.get_by_auth_token(int(user_id), token)

        logging.debug('UserBean [%s] - temp [%s]', str(user), str(temp))

        if user:
            self.handle_auth(received_json_data, response_data, user)
        else:
            response_data['status'] = 'INVALID_TOKEN'
            response_data['desc'] = 'Usuario nao autenticado'.decode('latin-1')