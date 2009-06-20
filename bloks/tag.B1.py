#       tag.py
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
#
# BLOKS application TAG module
#
# sjt 20090514 bloks/tag.py

class Error(Exception):
    pass

class TagError(Error):
    def __init__(self, message):
        self.message = message
    def __unicode__(self, message):
        print self.message

class Blok(object):
    '''Base class for html blocks.

    Properties are:-
    tag         The tag of the block, eg "span", "h1", etc.
    attributes  A list containing 2-tuples of attribute name, attribute value,
                    eg [("id","main"),("class","special"),]
    content     A sequential list of things to output, usually either strings or
                other block objects. Each object must support the __unicode__ method.
    indent      When output, each line will be indented by 4*indent spaces
                ** not yet implemented
    preamble    A string (or object) to be output before the opening tag.

    Methods are:-
    add_item(item)
                add an item to the content part
    '''

    # For the class as a whole, define list of allowable tags TODO
    taglist=(
        "h1","h2","h3","h4","h5","body","head","html"
    )
    #TODO - error checking for legal tags
    #TODO - indentation or obfuscation

    def __init__(self,tag,*content,**attributes):
        super(Blok,self).__init__()
        #initalize the data attributes of the object
        self.tag=tag
        self.preamble=""; self.attributes={}
        #attributes is a dictionary of keyword, value pairs. Generally each keyword will
        #be a valid python identifier, however, some attributes (e.g. "xml:lang) are not
        #valid python identifiers, so these are represented in a dict with an arbitrary
        #name, so attributes may contain something like:
        #{"style":"some style","href":"some href","extra":("xml:lang","en")} - the dicts
        #have to be handled differently when unpacking the attributes...
        if attributes:
            for keyw,attr in attributes.iteritems():

                if isinstance(attr,dict):
                #if the inner attribute itself is a dictionary, then use this to set
                #keywords.
                    for innerk,innera in attr.iteritems():
                        self.attributes[innerk]=innera
                else:
                #use the keyword and attribute given in the function parameters
                    self.attributes[keyw]=attr

        else:
            self.attributes={}
        if content:
            self.content=[t for t in content]
                #(sequential list of content for the object, each item can
                #be either a line of text, or another block object.)
        else:
            self.content = []

    def __unicode__(self):
        res = ""
        if self.preamble: res += self.preamble

        if self.tag:
            #the outermost block may not have a tag, the first tag might be in the
            #content, so don't bother with the attributes if there"s no tag...
            #Unpack the attributes into a list of strings, of the form 'key="value", escaping
            #quotation marks in the value
            attlist=[k+'="'+v.replace('"','\\"')+'"' for k,v in self.attributes.iteritems()]
            #Put the list of attributes into one string, separated by spaces
            attstring=" ".join(attlist)
            #Compose the tag block in the form:
            #<tag att1="abc" att2="def">content</tag> or if no content,
            #like <tab att1="abc" att2="def"/>
            res += "<" + self.tag
            if attstring: res += " " + attstring
            if self.content:
                res += ">\n"

        for item in self.content:
            #put each line of text into res, if the line is a block, then the block
            #should by default return its own text
            res += unicode(item)
            #if the item is a string, put in a newline, to make the source html
            #prettier.
            if isinstance(item,str): res += "\n"

        #close the tag, if there was one
        if self.tag:
            if self.content:
                res += "</" + self.tag + ">\n"
            else:
                #there is no content, so end the tag with short form
                res += "/>\n"

        return res

    def add(self,item):
        self.content.append(item)
#=========================================================================================
class A(Blok):
    """An html <a>..</a> block."""

    def __init__(self,*content,**attributes):
        super(A, self).__init__("a",*content,**attributes)
#=========================================================================================
class BODY(Blok):
    """An html <body>..</body> block."""

    def __init__(self,*content,**attributes):
        super(BODY, self).__init__("body",*content,**attributes)
#=========================================================================================
class BR(Blok):
    """An html <br /> block."""

    def __init__(self,*content,**attributes):
        super(BR, self).__init__("br",*content,**attributes)
#=========================================================================================
class DIV(Blok):
    """An html <div>..</div> block."""

    def __init__(self,*content,**attributes):
        super(DIV, self).__init__("div",*content,**attributes)
#=========================================================================================
class H1(Blok):
    """An html <h1>..</h1> block."""

    def __init__(self,*content,**attributes):
        super(H1, self).__init__("h1",*content,**attributes)
#=========================================================================================
class H2(Blok):
    """An html <h2>..</h2> block."""

    def __init__(self,*content,**attributes):
        super(H2, self).__init__("h2",*content,**attributes)
#=========================================================================================
class H3(Blok):
    """An html <h3>..</h3> block."""

    def __init__(self,*content,**attributes):
        super(H3, self).__init__("h3",*content,**attributes)
#=========================================================================================
class H4(Blok):
    """An html <h4>..</h4> block."""

    def __init__(self,*content,**attributes):
        super(H4, self).__init__("h4",*content,**attributes)
#=========================================================================================
class H5(Blok):
    """An html <h5>..</h5> block."""

    def __init__(self,*content,**attributes):
        super(H5, self).__init__("h5",*content,**attributes)
#=========================================================================================
class HEAD(Blok):
    """An html <head>..</head> block."""

    def __init__(self,*content,**attributes):
        super(HEAD, self).__init__("head",*content,**attributes)
#=========================================================================================
class HR(Blok):
    """An html <hr /> block."""

    def __init__(self,*content,**attributes):
        super(HR, self).__init__("hr",*content,**attributes)
#=========================================================================================
class HTML(Blok):
    """An html <html>..</html> block."""

    def __init__(self,*content,**attributes):
        super(HTML, self).__init__("html",*content,**attributes)
#=========================================================================================
class LI(Blok):
    """An html <li>..</li> block."""

    def __init__(self,*content,**attributes):
        super(LI, self).__init__("li",*content,**attributes)
#=========================================================================================
class META(Blok):
    """An html <meta>..</meta> block."""

    def __init__(self,*content,**attributes):
        super(META, self).__init__("meta",*content,**attributes)
#=========================================================================================
class P(Blok):
    """An html <p>..</p> block."""

    def __init__(self,*content,**attributes):
        super(P, self).__init__("p",*content,**attributes)
#=========================================================================================
class SPAN(Blok):
    """An html <span>..</span> block."""

    def __init__(self,*content,**attributes):
        super(SPAN, self).__init__("span",*content,**attributes)
#=========================================================================================
class TITLE(Blok):
    """An html <head>..</head> block."""

    def __init__(self,*content,**attributes):
        super(TITLE, self).__init__("title",*content,**attributes)
#=========================================================================================
class UL(Blok):
    """An html <ul>..</ul> block."""

    def __init__(self,*content,**attributes):
        super(UL, self).__init__("ul",*content,**attributes)
#=========================================================================================
