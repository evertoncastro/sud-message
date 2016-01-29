

class Util(object):
    
    def parseToken(self, token):
        values = token.split('.')
        return values[0], values[2]