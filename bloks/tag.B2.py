# BLOKS application BLOK_CLASSES module
#
# sjt 20090514 bloks/blok_classes.py

class Blok(object):
    '''Base class for html blocks.

    content     A list to be output: each item is either text, or another blok instance
    indent      When output, each line will be indented by 4*indent spaces
    atts        A dictionary of attributes and their values
    tag         The tag text of this block, e.g. "div", "p"
    class       The class name of this object
    id          The unique id, if any of this object
    '''

    # For the class as a whole, define list of allowable tags
    taglist=(
        "h1","h2","h3","h4","h5","body","head","html"
    )
    #TODO - error checking for legal tags
    #TODO - indentation or obfuscation

    def __init__(self,tag,attributes={},*args):
        super(Blok,self).__init__()
        #initalize the data attributes of the object
        self.content=[]     #sequential list of content for the object, each item can
                            #be either a line of text, or another block object.
        self.tag=tag
        self.preamble=""
        self.attributes=""

    def __unicode__(self):
        res = ""
        if self.preamble: res += self.preamble + "\n"
        if self.tag:
            res += "<" + self.tag
            if self.attributes: res += " " + self.attributes
            res += ">\n"
        for item in self.content:
            res += unicode(item) + "\n"
        #(puts each line of text into res, if the line is a block, then the block
        #should by default return its own text)
        if self.tag: res += "</" + self.tag + ">"
        return res

    def addItem(self,item):
        self.content.append(item)

#=========================================================================================
class Body(Blok):
    """The main body of the page."""

    def __init__(self, txt=""):
        super(Body, self).__init__()
        self.content=[]
        self.tag="body"
#=========================================================================================
class H1(Blok):
    """Heading block"""

    def __init__(self, txt="A heading"):
        super(H1, self).__init__()
        self.content=[txt]
        self.tag="h1"
#=========================================================================================
class H2(Blok):
    """Heading block"""

    def __init__(self, txt="A heading"):
        super(H2, self).__init__()
        self.content=[txt]
        self.tag="h2"
#=========================================================================================
class H3(Blok):
    """Heading block"""

    def __init__(self, txt="A heading"):
        super(H3, self).__init__()
        self.content=[txt]
        self.tag="h3"
#=========================================================================================
class H4(Blok):
    """Heading block"""

    def __init__(self, txt="A heading"):
        super(H4, self).__init__()
        self.content=[txt]
        self.tag="h4"
#=========================================================================================
class H5(Blok):
    """Heading block"""

    def __init__(self, txt="A heading"):
        super(H5, self).__init__()
        self.content=[txt]
        self.tag="h5"
#=========================================================================================
class Head(Blok):
    """The head section of the page."""

    def __init__(self, txt=""):
        super(Head, self).__init__()
        self.content=[]
        self.tag="head"
        self.addItem("<title>" + txt + "</title>")
        self.addItem('<meta http-equiv="content-type" content="text/html;charset=utf-8" />')
        self.addItem('<meta name="generator" content="html bloks module" />')
#=========================================================================================
class Html(Blok):
    """The whole page, including the doctype"""

    def __init__(self, txt=""):
        super(Html, self).__init__()
        self.content=[]
        self.tag="html"
        self.preamble='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        self.attributes='xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"'
