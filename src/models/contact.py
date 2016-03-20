from config.constants import developerContact
from models.baseClass import BaseClass
import json

class Contact(object):
     def getDeveloperContactList(self):
         return developerContact


class GetDeveloperContactList(BaseClass):
    def handle(self, response_data):
        try:
            list = Contact().getDeveloperContactList()
            response_data = list
            self.response.out.write(json.dumps(response_data))
        except:
            response_data['message'] = 'Error getting developer contact list'.decode('latin-1')
            
