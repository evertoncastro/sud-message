import webapp2
import json

class BaseClass(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        response_data = {}
        self.handle(response_data)
        # Write here the response.....
        #self.response.out.write(json.dumps(response_data))
    
    def post(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        received_json_data=json.loads(self.request.body)
        response_data = {}
        self.handle(received_json_data, response_data)
        # Write here the response.....
        self.response.out.write(json.dumps(response_data))