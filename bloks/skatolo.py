#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       skatolo.py
#
#       Copyright 2009 Simon Tite <simon@tite.st>
#


# bloks/blok.py - compound blocks... what it's all about!
# sjt 20090527
from tag import A,BODY,BR,DIV,H1,H2,H3,H4,H5,HEAD,HR,HTML,IMG,LI,LINK,META,P,SCRIPT,TAG
from tag import TITLE,UL
#some tags redefined for convenient use of using same object prefix in main code
import blok_config as bc
#=========================================================================================
class Blok(TAG):
    def __init___(self,*content,**keywords):
        super(Blok,self)._init()
#=========================================================================================
class Page(Blok):
    """
    Outline of a page: the doctype preamble, the html, head and page containers.

    Non-keyword arguments must be objects which have a __result() method: their
    output will inserted sequentially into the <body> portion of the HTML stream. The
    first argument (not optional) will be the title of the page. Other keyword arguments
    will be ignored, unless specifically mentioned here. Unlike most classes of this type,
    the add() function adds to the inner <body> block, not to the outer <html> block.
    """
    def __init__(self, title, *content, **kwords):
        super(Page,self).__init__("")
        self.head=HEAD(
            META(atts={"http-equiv":"content-type","content":"text/html;charset=utf-8"}),
            META(atts={"http-equiv":"Content-Style-Type","content":"text/css"}),
            Stylesheet("/static/css/skatolo.css"),
            Jquery("/static/js/jquery.js"),
            TITLE(title),
        )
        self.body=BODY(*content,**kwords)
        doctype='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '''
        doctype += '''"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
        self.add(
            '<?xml version="1.0" encoding="utf-8"?>',
            doctype,
            HTML(
                self.head,
                self.body,
                atts={"xmlns":"http://www.w3.org/1999/xhtml","xml:lang":"en","lang":"en"},
            )
        )
        self.add=self.body.add
        #(all elements added to the page from here on will be added to the body...)
#=========================================================================================
class ClearFloats(DIV):
    '''Creates an empty block which will appear BELOW everything so far, clearing all
    floating elements within the containing block.
    '''
    def __init__(self):
        kwords=_addsublist({},"classes","ClearFloats")
        super(ClearFloats,self).__init__(**kwords)
#=========================================================================================
class Jquery(Blok):
    '''Creates the headers for jquery'''
    def __init__(self,filename,*content,**kwords):
        super(Jquery,self).__init__()
        self.add(SCRIPT(atts={"type":"text/javascript","src":filename}))
        self.add(
            SCRIPT(
                "$(document).ready(function(){",
                "alert(\"start of program\");",
                "})",
                atts={"type":"text/javascript"},
            ),
        )
#=========================================================================================
class Link(Blok):
    '''Creates a simple link.'''
    def __init__(self,href,*content,**kwords):
        super(Link,self).__init__("")
        self.add(A(atts={"href":href},*content,**kwords))
#=========================================================================================
class LinksMenu(Blok):
    '''Creates a list of links to other pages.'''

    def __init__(self,headstring,*content,**kwords):
        super(LinksMenu,self).__init__("")
        ul=UL(headstring)
        for t in content:
            ul.add(LI(Link(t[0],t[1])))
        self.add(ul)
#=========================================================================================
class Picture(IMG):
    """Display a simple picture"""

    def __init__(self,picname,alt="",**kwords):
        #NB, note no content is allowed
        _addsubkeys(kwords,"atts","src","/img/"+picname)
        _addsubkeys(kwords,"atts","alt",alt)
        _addsubkeys(kwords,"styles","width",bc.TN_DEFAULT)
        super(Picture,self).__init__(**kwords)
#=========================================================================================
class PictureLeft(DIV):
    """Display a picture floating left"""
    #TODO - make sure this is within a valid block, as defined by XHTML spec...
    #TODO - make sure attributes are strings
    def __init__(self,picname,alt,*content,**kwords):
        _addsublist(kwords,"classes","PictureLeft")
        super(PictureLeft,self).__init__(**kwords)
        self.add(Picture(picname,alt))
        self.add(*content)
        self.add(ClearFloats())
#=========================================================================================
class PictureRight(Picture):
    """Display a picture floating right"""
    #TODO - make sure this is within a valid block, as defined by XHTML spec...
    #TODO - make sure attributes are strings
    def __init__(self,picname,alt,**kwords):
        _addsubkeys(kwords,"styles","float","right")
        super(PictureRight,self).__init__(picname,alt,**kwords)
#=========================================================================================
class Stylesheet(LINK):
    '''Creates the <link ... /> reference to a stylesheet.'''
    def __init__(self,sheetname):
        kwords={}
        _addsubkeys(kwords,"atts","rel","stylesheet")
        _addsubkeys(kwords,"atts","type","text/css")
        _addsubkeys(kwords,"atts","href",sheetname)
        super(Stylesheet,self).__init__(**kwords)
#=========================================================================================
class UpTree(Blok):
    '''Creates a link to "../", thus going up the hierarchy of pages.'''

    def __init__(self,*content,**kwords):
        super(UpTree,self).__init__("")
        self.add(Link("../",*content,**kwords))
#=========================================================================================
def _addsubkeys(d,kword,subkey,subitem):
    '''In the dictionary d, it adds subkey:subitem to the dictionary found in kword. If
    kword isn't found, then it is created, if the subkey already exists, then it is
    overwritten.
    '''
    tempdict=d.pop(kword,{})
    tempdict.update({subkey:subitem})
    d.update({kword:tempdict})
    return d
#=========================================================================================
def _addsublist(d,kword,item):
    '''In the dictionary d, it adds an item to the list found under kword. If the kword
    isn't found, then it is created.
    '''
    templist=d.pop(kword,[])
    if item not in templist:
        templist.append(item)
    d.update({kword:templist})
    return d

#=========================================================================================
def main():

    return 0

if __name__ == '__main__': main()
