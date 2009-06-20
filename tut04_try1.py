"""
simonhome.py

The main page of my site
"""
import sys, os
sys.path.insert(0, os.path.abspath('bloks'))
import cherrypy
from tag import Blok,A,BODY,BR,H1,H2,H3,H4,H5,HR,LI,P,UL

class HomePage:
    @cherrypy.expose
    def index(self):
        page=BODY(
            P(
                "Hi this is the first paragrapfh of the home page,",
                "Check out the other stuff below"
            ),
            UL(
                LI(A("A silly joke",href="/joke/")),
                LI(A("Some useful links",href="/links/"))
            )
        )
        return unicode(page)

class JokePage:
    @cherrypy.expose
    def index(self):
        page=BODY(
            P(
                '"In Python, how do you create a string of random',
                'characters?" -- "Read a Perl file!"'
            ),
            P(
                HR(), A("Return",href="../")
            )
        )
        return unicode(page)

class LinksPage:
    def __init__(self):
        # Request handler objects can create their own nested request
        # handler objects. Simply create them inside their __init__
        # methods!
        self.extra = ExtraLinksPage()

    @cherrypy.expose
    def index(self):
        # Note the way we link to the extra links page (and back).
        # As you can see, this object doesn't really care about its
        # absolute position in the site tree, since we use relative
        # links exclusively.
        page=BODY(
            P("Some useful links:"),
            UL(
                LI(A("CherryPy homepage",href="http://www.cherrypy.org")),
                LI(A("Python homepage",href="http://www.python.org"))
            ),
            P("Click ", A("here ",href="./extra/"), "for some more useful links"),
            P(
                HR(), A("Return",href="../")
            )
        )
        return unicode(page)

class ExtraLinksPage:
    @cherrypy.expose
    def index(self):
        # Note the relative link back to the Links page!
        page=BODY(
            P("Here are some useful extra links:"),
            UL(
                LI(A("del.icio.us",href="http://del.icio.us")),
                LI(A("Hendrik's weblog",href="http://www.mornography.de"))
            ),
            P(
                HR(), A("Return",href="../")
            )
        )
        return unicode(page)

# This is the home page structure
root = HomePage()
root.joke = JokePage()
root.links = LinksPage()
cherrypy.tree.mount(root)

# Remember, we don't need to mount ExtraLinksPage here, because
# LinksPage does that itself on initialization. In fact, there is
# no reason why you shouldn't let your root object take care of
# creating all contained request handler objects.

if __name__ == '__main__':
    import os.path
    thisdir = os.path.dirname(__file__)
    cherrypy.quickstart(config=os.path.join(thisdir, 'tutorial.conf'))
