import webapp2

class Person(object):
    def set_name(self, name):
        self.name = name
        

class CallPerson(webapp2.RequestHandler):
    def get(self):
        person = Person()
        person.set_name('Everton de Castro')
        self.response.out.write(person.name)

