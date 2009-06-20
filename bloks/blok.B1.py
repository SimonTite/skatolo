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

# bloks/blok.py - compund blocks... what it's all about!
# sjt 20090527
from tag import *
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
            META(d1={"http-equiv":"content-type"},content="text/html;charset=utf-8"),
            TITLE(title)
        )
        self.body=BODY(*content)
        self.add(
            HTML(
                self.head,
                self.body,
                #the attributes of the HTML tag
                xmlns="http://www.w3.org/1999/xhtml",
                extradict={"xml:lang": "en"},
                #need to pass a dictionary if the key is not a legal python variable
                lang="en"
            )
        )
        self.preamble='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
#=========================================================================================
class LinksMenu(Blok):
    '''Creates a list of links to other pages.

    name:   LinksMenu( "heading",("text1","href string1"), ("text, "href2"), ...)
        def __init__

    @return <ul>Heading<li><a href="href-string1">"text-string1"</li>
                        <li><a href="href-string2">"text-string2"</li>

    '''
    def __init__(self,headstring,*content,**kwords):
        super(LinksMenu,self).__init__("")
        ul=UL(headstring)
        for t in content:
            ul.add(LI(A(t[0],href=t[1])))
        self.add(ul)
#=========================================================================================
class UpTree(Blok):
    '''
    Creates a link to "../", thus going up the hierarchy of pages.

name: UpTree
@param      text to display as link (e.g. "Return")
*content    ignored
**kwords    ignored
@return     "<a href="../">parameter1</a>
    '''

    def __init__(self,text,*content,**kwords):
        super(UpTree,self).__init__("")
        self.add(A(text,href="../"))
#=========================================================================================
def main():

    return 0

if __name__ == '__main__': main()
