import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        raise NotImplementedError, "This is an error..."
    
if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/')
