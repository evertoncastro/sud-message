import webapp2


class BaseClass(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        received_json_data=json.loads(self.request.body)
        response_data = {}
        self.handle(received_json_data, response_data)
        # Write here the response.....
        self.response.out.write(json.dumps(response_data))