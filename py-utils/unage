#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#       untitled.py
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

import os.path
import shutil
import sys

def age_one_file(filename, generation=0, infix="B", *args):
    """Age one file, by renaming it to the next generation number.

    An argument of "unage" works in the opposite direction, it will take the
    generation file and move or copy it back to the previous generation.

    filename    contains the original unmodified file name, eg "myfile.ext"
    generation  the generation of this file to be aged, 0 being the original.
    infix       the backup infix  - see examples:

    age_one_file("myfile.txt") copies/renames "myfile.txt" to "myfile.B1.txt"
    age_one_file("myfile.txt",1) copies/renames "myfile.B1.txt" to "myfile.B2.txt"
    age_one_file("myfile.txt",2) copies/renames "myfile.B2.txt" to "myfile.B2.txt"
        (In all these cases, the infix is "B".)

    Any file copied to will be overwritten without warning, and if the source file does
    not exist, nothing will happen at all. Oher exceptions, and in particular those
    caused by file permission rights, will not be trapped.

    Optional arguments are:
        verbose     Display verification of the rename
        static      When the generation is 0, the original file is copied to
                    generation 1, leaving the original file intact. For all other
                    generations, this keyword is ignored.

    """
    verbose = "verbose" in args
    static = ("static" in args) and generation == 0
    unage = ("unage" in args)
    if unage:
        direction=-1
    else:
        direction=+1
    source = get_backup_name(filename, generation=generation, infix=infix)
    if os.path.exists(source):
        target = get_backup_name(filename, generation=generation + direction, infix=infix)
        if verbose:
            print "Doing " + sys.argv[0] + " " + source + " to " + target + "..."
        if os.path.isdir(filename):
            shutil.copytree(source,target,symlinks=True)
            if not static:
                shutil.rmtree(source,True)
                #True means ignore all errors when deleting the source directory.
        else:
            if static:
                shutil.copy2(source, target)
            else:
                shutil.move(source, target)
        if verbose:
            print "Done.\n"
    return

def get_backup_name(filename, generation=0, infix="B"):
    """Return the backup file name based on a generation number.

    Examples:
    get_backup_name("myfile.txt") returns ("myfile.txt")
    get_backup_name("myfile.txt",1) returns ("myfile.B1.txt")
    get_backup_name("myfile.txt",2) returns ("myfile.B2.txt")
    ...and so on.

    """
    base, ext = splitext(filename)
    if generation == 0:
        return filename
    else:
        return base + "." + infix + str(generation) + ext

def splitext(filename):
    #This is a simple alias of os.path.splitext, but is done this way to allow possible
    #alternative splits which will probably never be implemented.
    """Split a string (usually a filename) returning (base,ext).

    Returns a 2-tuple of (base,ext) where:
        base = all the text to the left of the rightmost dot in the string
        ext = the rightmost dot in the string and all text following it
    The os module will handle leading dots sensibly, so that a file called (for example)
    ".myprofile" will be returned as (".profile","").

    """
    return (os.path.splitext(filename))

def main():
    total_generations = 5
    #Find out if this was called with "age" "sage" or "unage":
    calledby = splitext(os.path.basename(sys.argv[0]))[0]
    #(take off the filename directory prefixes and extension, if any)
    filename = sys.argv[1]
    if (calledby == "age") or (calledby == "sage"):
        #Symbolic links won't be handled, because I'm not sure how they should behave anyway.
        if os.path.islink(filename):
            print "Symbolic link " + filename + " cannot be aged or unaged."
            return -1
        for generation in reversed(range(total_generations)):
            #(start at 4, count down to zero)
            if calledby =="age":
                age_one_file(filename,generation,"B","verbose")
            else:
                age_one_file(filename,generation,"B","verbose","static")
    elif calledby == "unage":
        for generation in range(1,total_generations+1):
            #(start at 1, count up to 5
            age_one_file(filename,generation,"B","verbose","unage")
    else:
        print "Called by unknown command: use age, sage or unage."
        return -1
    return 0

if __name__ == '__main__': main()
