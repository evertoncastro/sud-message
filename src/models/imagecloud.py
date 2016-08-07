from google.appengine.ext import ndb
from imgurpython import ImgurClient
import logging

class ImageCloud(ndb.Model):
    dateCreation = ndb.DateTimeProperty(auto_now=True)
    client_id = ndb.StringProperty()
    client_secret = ndb.StringProperty()
    access_token = ndb.StringProperty()
    refresh_token = ndb.StringProperty()
    
    def create(self):
        image = ImageCloud(
            client_id= '8208c4b5f89b7c6',
            client_secret='5304136ecc8fdcbee91db30914eb60b6ac2b6e1c',
            access_token='003f532697d652a37babc365c57d8346584ce517',
            refresh_token='45ab269dea40e744febae6249b992e36054092dd',
            id='1')
        
        image.put()

class ImageCloudManager(object):
    def upload(self, url):
        imagecloud = ImageCloud().get_by_id('1')
        logging.info('Image cloud: '+str(imagecloud))
        try:                
            client = ImgurClient(imagecloud.client_id, imagecloud.client_secret)
            client.set_user_auth(imagecloud.access_token, imagecloud.refresh_token)
            conf = {"album" : "KHz1y"}
                   
            resp = client.upload_from_url(url, config=conf, anon=False)
            logging.info('Resp imgur: '+str(resp))
            return resp['link']
        except Exception as e:
            logging.info("Erro imgur: "+str(e))
            raise ErrorUploadImage      
        
 
class ErrorUploadImage(Exception):
    def __init__(self):
        raise Exception        
            
            