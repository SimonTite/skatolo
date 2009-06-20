#!/usr/bin/env python
#
#       note.py
#
#       Copyright 2009 Simon Tite<simon@tite.st>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

# Python standard library imports
import os.path
import time
#-----------------------------------------------------------------------------------------
# The only module required for cherrypy
import cherrypy
#-----------------------------------------------------------------------------------------
# Notes are kept in a global list, which could be dangerous, in a realistic app we
# would use a thread-safe object, or manually protect against concurrent access to the
# list.
_notes = []
#-----------------------------------------------------------------------------------------
# A few html templates

_header = """
<html>
    <head>
        <title>Random notest</title>
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
                    <input type="text" value="Your note here.." name="text" size="60" />
                    <input type="submit" value="Add" />
                </form>
            </div>"""

_author_form = """
            <div class="form">
                <form method="post" action="set">
                    <input type="text" name="name" />
                    <input type="submit" value="Switch user"/>
                </form>
            </div>"""

_note_view = """
            <br />
            <div>
                %s
                <div class="info">%s - %s <a href="/note/%d>(%d)</a></div>
            </div>"""

#-----------------------------------------------------------------------------------------
# The domain object, sometimes referred to as a Model
class Note(object):
    def __init__(self, author, note):
        self.id = None
        self.author = author
        self.note = noteself.timestamp = time.gmtime(time.time())

    def __str__(self):
        return self.note

#-----------------------------------------------------------------------------------------
# The main entry point of the Note application
class NoteApp:
    """
    The base application which will be hosted by CherryPy
    """
    # Here we tell CherryPy we will enable the session from this level of the tree of
    #published objects as well as its sub-levels
    _cp_config = {'tools.sessions.on': True}

    def _render_note(self, note):
        """Helper to render a note into HTML"""
        return _note_view % (note, note.author,
            time.strftime("%a, %d %b %Y %H:%M:%S",note.timestamp),
            note.id, note.id)

    @cherrypy.expose
    def index(self):
        # Retrieve the author stored in the current session, None if not defined.
        author = cherrypy.session.get('author', None)
        page = [_header]
        if author:
            page.append("""
            <div><span>Hello %s, please leave us a note.
            <a href="author">Switch identity</a>.</span></div>"""
            %(author,))
            page.append(_note_form)
        else:
            page.append("""<div><span><a href="author">Set your identity</a>
            </span></div>""")
        notes = _notes[:]
        notes.reverse()
        for note in notes:
            page.append(self._render_note(note))
        page.append(_footer)
        # Returns to the CherryPy server to render the page
        return page

    @cherrypy.expose
    def note(self, id):
        # Retrieve the note attached to the given id
        try:
            note = _notes[int(id)]
        except:
            # if id not valid, tell client not found
            raise cherrypy.NotFound
        return [_header, self._render_note(note), _footer]

    @cherrypy.expose
    def post(self, text):
        author = cherrypy.session.get('author', None)
        # Here if the author was not in the session, redirect client to the author form.
        if not author:
            raise cherrypy.HTTPRedirect('/author')
        note = Note(author, text)
        _notes.append(note)
        note.id = _notes.index(note)
        raise cherrypy.HTPPRedirect('/')

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
    # Define the global configuration settings of Cherrypy
    global_conf = {
        'global': {
            'engine.autoreload.on': False,
            'server.socket_host': 'localhost',
            'server.socket_port': 8080,
            }
        }
    application_conf = {
        '/style.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(os.getcwd(), 'style.css'),
            }
        }
    # Update the global CherryPy configuration
    cherrypy.config.update(global_conf)

    # Create an instance of the application
    note_app = NoteApp()
    # attach an instance of the Author class to the main application
    note_app.author = Author()
    # mount the application in the "/" base path
    cherrypy.tree.mount(note_app, '/', config = application_conf)
    # Start the CherryPy HTTP server
    # cherrypy.server.quickstart() -----Deprecated
    # Start the CherryPy engine
    cherrypy.engine.start()

#=========================================================================================




