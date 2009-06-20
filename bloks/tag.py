#       tag.py
# -*- coding: utf-8 -*-
#
#       Copyright 2009 Simon Tite<simon@tite.st>
#       All rights reserved

# BLOKS application TAG module
#
# sjt 20090514 bloks/tag.py
# sjt 20090607 major change to structure to handle attributes in a better way

class Error(Exception):
    pass

class TagError(Error):
    def __init__(self, message):
        self.message = message
    def __unicode__(self, message):
        print self.message

##
# A class describing an html block and all its contents (text and inner blocks)
##

##
# @def      Blok(tag, atts={}, *content, **kwords)
# @defreturn An instance of the Blok class
# @param    tag     The html tag string, e.g. span, h1, div, etc (can be blank)
# @keyparam atts    An optional dictionary containing the attributes of the block
# @param    *content Objects contained in the block. These can be lines of text, or child
#                   objects.
# @param  **attributes    These can be described as <b>keyword="value"</b>, in which
#                   case the keyword has to be a legal Python identifier,
#=========================================================================================
class TAG(object):
    '''Base object for a html tag.

    A tag contains a list of content items, which can be any object, including strings
    or other tag objects, capable of displaying itself with the __unicode__() method.
    '''
    #-------------------------------------------------------------------------------------
    def __init__(self,tag="",*content,**kwords):
        '''The tag itself may be blank, the contents are a list of unicode objects, and
        the following kwords will be interpreted:
        "atts":{a dictionary of attribute value pairs}
            eg "atts:{"href":"/home","alt":"a picture"}
        "styles":{a dictionary of style attribute pairs}
            eg "styles":{"color":"blue","height":"10px"}
        Other keyword options arriving here will be ignored.
        '''
        super(TAG,self).__init__()
        self.tag=tag; self.content=[]; self.atts={}
        if content:
            [self.add(t) for t in content]
        self.atts=kwords.pop("atts",{})
        self.styles=kwords.pop("styles",{})
        self.id=kwords.pop("id",{})
        self.classes=kwords.pop("classes",[])
    #-------------------------------------------------------------------------------------
    def result(self):
        res = ""
        if self.tag:
            res += "<" + self.tag

            if self.atts:
                res += " " + " ".join(
                    ['%s="%s"' % (k,v.replace('"','\\"')) for k,v in self.atts.items()]
                )
            if self.styles:
                res += " style='" + " ".join(
                    ["%s:%s;" % (k,v) for k,v in self.styles.items()]
                ) + "'"
            if self.id:
                res += " id='" + self.id +"'"
            if self.classes:
                res += " class='" + " ".join(
                    ["%s" % v for v in self.classes]) + "'"

        if self.content:
            if self.tag: res += ">\n"
            for item in self.content:
                if item:
                    #(item could be blank string, or None)
                    if isinstance(item,str):
                        res += item +"\n"
                    else:
                        res += item.result()
            if self.tag: res += "</" + self.tag + ">\n"
        else:
            if self.tag: res += " />\n"

        return res
    #-------------------------------------------------------------------------------------
    def add(self,item="",*items):
        self.content.append(item)
        if items:
            [self.add(t) for t in items]
        return item
        #(return the first or only object added, this return is often discarded)
#=========================================================================================
class A(TAG):
    """An html <a>..</a> block."""

    def __init__(self,*content,**attributes):
        super(A, self).__init__("a",*content,**attributes)
#=========================================================================================
class BODY(TAG):
    """An html <body>..</body> block."""

    def __init__(self,*content,**attributes):
        super(BODY, self).__init__("body",*content,**attributes)
#=========================================================================================
class BR(TAG):
    """An html <br /> block."""

    def __init__(self,*content,**attributes):
        super(BR, self).__init__("br",*content,**attributes)
#=========================================================================================
class DIV(TAG):
    """An html <div>..</div> block."""

    def __init__(self,*content,**attributes):
        super(DIV, self).__init__("div",*content,**attributes)
#=========================================================================================
class H1(TAG):
    """An html <h1>..</h1> block."""

    def __init__(self,*content,**attributes):
        super(H1, self).__init__("h1",*content,**attributes)
#=========================================================================================
class H2(TAG):
    """An html <h2>..</h2> block."""

    def __init__(self,*content,**attributes):
        super(H2, self).__init__("h2",*content,**attributes)
#=========================================================================================
class H3(TAG):
    """An html <h3>..</h3> block."""

    def __init__(self,*content,**attributes):
        super(H3, self).__init__("h3",*content,**attributes)
#=========================================================================================
class H4(TAG):
    """An html <h4>..</h4> block."""

    def __init__(self,*content,**attributes):
        super(H4, self).__init__("h4",*content,**attributes)
#=========================================================================================
class H5(TAG):
    """An html <h5>..</h5> block."""

    def __init__(self,*content,**attributes):
        super(H5, self).__init__("h5",*content,**attributes)
#=========================================================================================
class HEAD(TAG):
    """An html <head>..</head> block."""

    def __init__(self,*content,**attributes):
        super(HEAD, self).__init__("head",*content,**attributes)
#=========================================================================================
class HR(TAG):
    """An html <hr /> block."""

    def __init__(self,*content,**attributes):
        super(HR, self).__init__("hr",*content,**attributes)
#=========================================================================================
class HTML(TAG):
    """An html <html>..</html> block."""

    def __init__(self,*content,**attributes):
        super(HTML, self).__init__("html",*content,**attributes)
#=========================================================================================
class IMG(TAG):
    """An html <img>..</img> block."""

    def __init__(self,*content,**attributes):
        super(IMG, self).__init__("img",*content,**attributes)
#=========================================================================================
class LI(TAG):
    """An html <li>..</li> block."""

    def __init__(self,*content,**attributes):
        super(LI, self).__init__("li",*content,**attributes)
#=========================================================================================
class LINK(TAG):
    """An html <link.. /> block."""

    def __init__(self,*content,**attributes):
        super(LINK, self).__init__("link",*content,**attributes)
#=========================================================================================
class META(TAG):
    """An html <meta>..</meta> block."""

    def __init__(self,*content,**attributes):
        super(META, self).__init__("meta",*content,**attributes)
#=========================================================================================
class P(TAG):
    """An html <p>..</p> block."""

    def __init__(self,*content,**attributes):
        super(P, self).__init__("p",*content,**attributes)
#=========================================================================================
class SCRIPT(TAG):
    """An html <script>..</script> block."""

    def __init__(self,*content,**attributes):
        super(SCRIPT, self).__init__("script",*content,**attributes)
#=========================================================================================
class SPAN(TAG):
    """An html <span>..</span> block."""

    def __init__(self,*content,**attributes):
        super(SPAN, self).__init__("span",*content,**attributes)
#=========================================================================================
class TITLE(TAG):
    """An html <head>..</head> block."""

    def __init__(self,*content,**attributes):
        super(TITLE, self).__init__("title",*content,**attributes)
#=========================================================================================
class UL(TAG):
    """An html <ul>..</ul> block."""

    def __init__(self,*content,**attributes):
        super(UL, self).__init__("ul",*content,**attributes)
#=========================================================================================
