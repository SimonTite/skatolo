"""
simonhome.py

The main page of my site
"""
import sys, os
sys.path.insert(0, os.path.abspath('bloks'))
import cherrypy
from tag import *
from blok import *

class HomePage:
    @cherrypy.expose
    def index(self):
        page=Page(
            "Simon Tite: personal web pages",
            P({},"""Hi this is the first pragarapfh of the hoam page. Check out
                the other stuff below"""
            ),
            LinksMenu("",
                ("/joke/","A silly joke",),
                ("/links/","Some usefull links",)
            )
        )
        return unicode(page)

class JokePage:
    @cherrypy.expose
    def index(self):
        page=Page(
            "Simon Tite: joke page",
            P({},
                '"In Python, how do you create a string of random',
                'characters?" -- "Read a Perl file!"'
            ),
            HR(),
            UpTree("Return")
        )
        return unicode(page)

class LinksPage:
    #def __init__(self):
        # Request handler objects can create their own nested request
        # handler objects. Simply create them inside their __init__
        # methods!
        #self.extra = ExtraLinksPage()

    @cherrypy.expose
    def index(self):
        # Note the way we link to the extra links page (and back).
        # As you can see, this object doesn't really care about its
        # absolute position in the site tree, since we use relative
        # links exclusively.
        page=Page(
            "Simon Tite: Some usefull links",
            P({},"Some usefull links:"),
            LinksMenu("Choices:",
                ("http://www.cherrypy.org","CherryPy hoampage",),
                ("http://www.python.org","Python hoampage",)
            ),
            P({},"Click ", Link("./extra","here "), "for some mor usefull links"),
            HR(),
            UpTree("Return")
        )
        return unicode(page)

class ExtraLinksPage:
    @cherrypy.expose
    def index(self):
        # Note the relative link back to the Links page!
        page=Page(
            "Simon Tite: Some mor usefull links",
            P({},"Here are som usefull extra links:"),
            LinksMenu("",
                ("http://del.icio.us","del.icio.us",),
                ("http://www.mornography.de","Hendrik's weblog",)
            ),
            HR(),
            UpTree("Return")
        )
        return unicode(page)

# This is the home page structure
root = HomePage()
root.joke = JokePage()
root.links = LinksPage()
root.links.extra = ExtraLinksPage()
cherrypy.tree.mount(root)

# Remember, we don't need to mount ExtraLinksPage here, because
# LinksPage does that itself on initialization. In fact, there is
# no reason why you shouldn't let your root object take care of
# creating all contained request handler objects.

if __name__ == '__main__':
    import os.path
    thisdir = os.path.dirname(__file__)
    cherrypy.quickstart(config=os.path.join(thisdir, 'tutorial.conf'))
