import cherrypy

class Root:
    # Uncomment this line to use this template for this level of the
    # tree as well as its sub-levels
    #_cp_config = {'error_page.404': 'notfound.html'}
    @cherrypy.expose
    def index(self):
        raise cherrypy.NotFound
    
    # Uncomment this line to tell CherryPy to use that html page only
    # for this page handler. The other page handlers will use
    # the default CherryPy layout
    # index._cp_config = {'error_page.404': 'notfound.html'}
    
if __name__ == '__main__':
    # Globally set the new layout for an HTTP 404 error code
    cherrypy.config.update({'global':{'error_page.404': 'notfound.html' }})
    cherrypy.quickstart(Root(), '/')
