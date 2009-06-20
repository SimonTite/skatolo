import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPError(401, 'You are not authorized to access this resource')
if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/')
