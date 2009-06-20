import cherrypy
from cherrypy import _cptools

class Root(_cptools.XMLRPCController):
    @cherrypy.expose
    
    def echo(self, message):
        return message
    
if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/xmlrpc')
