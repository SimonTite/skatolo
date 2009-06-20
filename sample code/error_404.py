import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        # shortcut to cherrypy.HTTPError(404)
        raise cherrypy.NotFound
    
if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/')
