#!/usr/bin/env python
#
#       blok.py
#
#       Copyright 2009 Simon Tite <simon@tite.st>
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

# bloks/blok.py - compound blocks... what it's all about!
# sjt 20090527
from tag import *
#=========================================================================================
class Blok(TAG):
    def __init___(self,*content,**keywords):
        super(Blok,self)._init()
#=========================================================================================
class Page(Blok):
    """
    Outline of a page: the doctype preamble, the html, head and page containers.

    Non-keyword arguments must be objects which have a __unicode__() method: their
    output will inserted sequentially into the <body> portion of the HTML stream. The
    first argument (not optional) will be the title of the page. Other keyword arguments
    will be ignored, unless specifically mentioned here.
    """
    def __init__(self, title, *content, **kwords):
        super(Page,self).__init__("")
        self.head=HEAD(
            META(atts={"http-equiv":"content-type","content":"text/html;charset=utf-8"}),
            Jquery("/static/js/"),
            TITLE(title),
            TITLE(title),
        )
        self.body=BODY({},*content)
        preamble='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '''
        preamble += '''"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
        self.add(
            preamble,
            HTML({"xmlns":"http://www.w3.org/1999/xhtml","xml:lang":"en","lang":"en"},
                self.head,
                self.body,
            )
        )
#=========================================================================================
class Jquery(Blok):
    '''Creates the headers for jquery'''
    def __init__(self,path_to_jquery,*content,**kwords):
        super(Jquery,self).__init__()
        self.add(SCRIPT({"type":"text/javascript","src":path_to_jquery + "jquery.js"}))
        self.add(
            SCRIPT(
                {"type":"text/javascript"},
                "$(document).ready(function(){",
                "alert(\"start of program\");",
                "})"
            ),
        )
#=========================================================================================
class Link(Blok):
    '''Creates a simple link.'''
    def __init__(self,href,*content,**kwords):
        super(Link,self).__init__("")
        self.add(A({"href":href},*content,**kwords))
#=========================================================================================
class LinksMenu(Blok):
    '''Creates a list of links to other pages.'''

    def __init__(self,headstring,*content,**kwords):
        super(LinksMenu,self).__init__("")
        ul=UL({},headstring)
        for t in content:
            ul.add(LI({},Link(t[0],t[1])))
        self.add(ul)
#=========================================================================================
class Picture(Blok):
    """Display a simple picture"""

    def __init__(self,picname,alt="",*content,**kwords):
        super(Picture,self).__init__("")

        pic=IMG({
            "src":"/img/"+picname,
            "alt":alt
        },
        *content,**kwords)

        self.add(pic)
#=========================================================================================
class PictureLeft(Blok):
    """Display a picture floating left"""

    def __init__(self,picname,alt="",*content,**kwords):
        atts=kwords.update({"style":"float:left"})
        print "** DEBUG blok/PictureLeft kwords=",kwords
        super(PictureLeft,self).__init__(picname,alt,*content,**kwords)
#=========================================================================================
class UpTree(Blok):
    '''Creates a link to "../", thus going up the hierarchy of pages.'''

    def __init__(self,*content,**kwords):
        super(UpTree,self).__init__("")
        self.add(Link("../",*content,**kwords))
#=========================================================================================
def main():

    return 0

if __name__ == '__main__': main()
