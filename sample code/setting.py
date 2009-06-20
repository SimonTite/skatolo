import cherrypy

class Root:
    # Global settings to this controller
    # class which will impact all the page handlers
    _cp_config = {'tools.gzip.on': True}
    
    @cherrypy.expose
    def index(self):
        return "welcome"
    
    @cherrypy.expose
    def default(self, *args, **kwargs):
        return "oops"

    @cherrypy.expose
    # this next line is useless because we have set the class
    # attribute _cp_config but shows you how to configure a tool
    # using its decorator.
    @cherrypy.tools.gzip()
    def echo(self, msg):
        return msg
    
    @cherrypy.expose
    def hello(self):
        return "there"
    # Locally disable a tool
    hello._cp_config = {'tools.gzip.on': False}

if __name__ == '__main__':
    cherrypy.config.update({'checker.on': False})
    cherrypy.quickstart(Root(), '/')
