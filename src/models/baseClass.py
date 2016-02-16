import webapp2
import json
import logging

class BaseClass(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        response_data = {}
        self.handle(response_data)
        #self.response.out.write(json.dumps(response_data))


    def post(self):
        #_origin = self.request.headers['Origin']
        self.response.headers.add_header("Access-Control-Allow-Origin","*")
        self.response.headers.add_header("Access-Control-Request-Method", "POST")
        self.response.headers['Content-Type'] = 'application/json'
        received_json_data=json.loads(self.request.body)
        response_data = {}
        self.handle(received_json_data, response_data)
        self.response.out.write(json.dumps(response_data))



class BaseClassAuth(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        response_data = {}
        self.handle(response_data)

    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        received_json_data=json.loads(self.request.body)
        response_data = {}
        self.handle(received_json_data, response_data)
        #self.response.out.write(json.dumps(response_data))
