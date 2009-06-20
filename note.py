#!/usr/bin/python
# -*- coding: utf-8 -*

# Python standard library imports
import os.path
import sys
import time


###############################################################
#The unique module to be imported to use cherrypy
###############################################################
import cherrypy
sys.path.insert(0, os.path.abspath('bloks'))
from tag import *
from blok import *

# CherryPy needs an absolute path when dealing with static data
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

# We will keep our notes into a global list
_notes = []

###############################################################
# A few HTML templates
###############################################################
page=Page("Random notes")
page.cssfile="/style.css"
body=page.body

_header = """
<html>
  <head>
    <title>Random notes</title>
    <link rel="stylesheet" type="text/css" href="/style.css"></link>
  </head>
  <body>
  <div class="container">"""

_footer = """
  </div>
  </body>
</html>"""

_note_form = """
  <div class="form">
  <form method="post" action="post" class="form">
    <input type="text" value="Your note here..." name="text" size="60"></input>
    <input type="submit" value="Add"></input>
  </form>
  </div>"""

_author_form = """
  <div class="form">
  <form method="post" action="set">
    <input type="text" name="name"></input>
    <input type="submit" value="Switch"></input>
  </form>
  </div>"""

_note_view = """
<br />
<div>
   %s
   <div class="info">%s - %s <a href="/note/%d">(%d)</a></div>
</div>"""

###############################################################
# Our only domain object (sometimes referred as to a Model)
###############################################################
class Note(object):
    def __init__(self, author, note):
        self.id = None
        self.author = author
        self.note = note
        self.timestamp = time.gmtime(time.time())

    def __str__(self):
        return self.note

    def __unicode__(self):
        return self.note

###############################################################
# The main entry point of the Note application
###############################################################
class NoteApp:
    """
    The base application which will be hosted by CherryPy
    """
    # Here we tell CherryPy we will enable the session
    # from this level of the tree of published objects
    # as well as its sub-levels
    _cp_config = { 'tools.sessions.on': True }

    def _render_note(self, note):
        """Helper to render a note into HTML"""
        return _note_view % (note,
                             note.author,
                             time.strftime("%a, %d %b %Y %H:%M:%S",
                                           note.timestamp),
                             note.id,
                             note.id)

    @cherrypy.expose
    def index(self):
        # Retrieve the author stored in the current session
        # None if not defined
        author = cherrypy.session.get('author', None)

        page = [_header]

        if author:
            page.append("""
            <div><span>Hello %s, please leave us a note.
            <a href="author">Switch identity</a>.</span></div>""" % (author,))
            page.append(_note_form)
        else:
            page.append("""<div><a href="author">Set your identity</a></span></div>""")

        notes = _notes[:]
        notes.reverse()
        for note in notes:
            page.append(self._render_note(note))

        page.append(_footer)
        # Returns to the CherryPy server the page to render
        return page

    @cherrypy.expose
    def note(self, id):
        # Retrieve the note attached to the given id
        try:
            note = _notes[int(id)]
        except:
            # If the ID was not valid, let's tell the
            # client we did not find it
            raise cherrypy.NotFound
        return [_header, self._render_note(note), _footer]

    @cherrypy.expose
    def post(self, text):
        author = cherrypy.session.get('author', None)

        # Here if the author was not in the session
        # we redirect the client to the author form
        if not author:
            raise cherrypy.HTTPRedirect('/author')

        note = Note(author, text)
        _notes.append(note)
        note.id = _notes.index(note)
        raise cherrypy.HTTPRedirect('/')

class Author(object):
    @cherrypy.expose
    def index(self):
        return [_header, _author_form, _footer]

    @cherrypy.expose
    def set(self, name):
        cherrypy.session['author'] = name
        return [_header, """
        Hi %s. You can now leave <a href="/" title="Home">notes</a>.
""" % (name,), _footer]


if __name__ == '__main__':
    # Define the global configuration settings of CherryPy
    global_conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'server.protocol_version': 'HTTP/1.1'
        }
    }
    current_dir = os.path.dirname(os.path.abspath(__file__))
    application_conf = {
        '/': {
            'tools.staticdir.root': current_dir,
            '/static/css': {
                'tools.gzip.on': True,
                'tools.gzip.mime_types':['text/css'],
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'styles',
            },
            '/static/js': {
                'tools.gzip.on': True,
                'tools.gzip.mime_types':['application/javascript'],
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'scripts',
            },
            '/img': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'images',
            },
        }
    }

    # Update the global CherryPy configuration
    cherrypy.config.update(global_conf)

    # Create an instance of the application
    note_app = NoteApp()
    # attach an instance of the Author class to the main application
    note_app.author = Author()

    # mount the application on the '/' base path
    cherrypy.tree.mount(note_app, '/', config = application_conf)

    # Start the CherryPy HTTP server
    cherrypy.quickstart()
    # Start the CherryPy engine
    # cherrypy.engine.start()
