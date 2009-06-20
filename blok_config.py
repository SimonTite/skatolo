#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       blok_config.py
#
#       Copyright 2009 Simon Tite <simon@tite.st>

import os.path
import cherrypy

#Some "global" constants used by skatolo.py

#Suggested widths of pictures, eg, logos, portraits, etc.
TN_MEGA="1024px"
TN_GIANT="512px"
TN_LARGE="256px"
TN_MEDIUM="128px"
TN_SMALL="64px"    #Useful "thumbnail" size for face shots
TN_TINY="32px"
TN_MICRO="16px"
TN_DEFAULT=TN_SMALL

def blok_config(root):

    # Define the global configuration settings of CherryPy
    global_conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
            'server.protocol_version': 'HTTP/1.1'
        }
    }
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print "current_dir ",current_dir
    application_conf = {
        '/': {'tools.staticdir.root': current_dir},
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

    # Update the global CherryPy configuration
    cherrypy.config.update(global_conf)

    # Create an instance of the application
    cherrypy.tree.mount(root, '/', config = application_conf)

    # Start the CherryPy HTTP server
    cherrypy.quickstart()
#=========================================================================================
def main():

    return 0

if __name__ == '__main__': main()
