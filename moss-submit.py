#!/bin/python
from __future__ import print_function
# Author: Theodore Ando
# Institution: Princeton University
# The following script was translated to python from a perl script published by
# http://moss.stanford.edu.  The latest scripts can be found at
# http://moss.stanford.edu/general/scripts.html
# 
# THE ONLY THING YOU SHOULD CHANGE IS THE USERID VARIABLE IMMEDIATELY BELOW THIS LINE.

USERID = 123456789

# Please read all the comments down to the line that says "STOP".
# These comments are divided into three sections:
#
#     1. usage instructions
#     2. installation instructions
#     3. standard copyright
#
# Feel free to share this script with other instructors of programming
# classes, but please do not place the script in a publicly accessible
# place.
#
# IMPORTANT: This script is known to work on Unix.  If the
# script does not work for you, you can try the email-based
# version for Windows (available on the Moss home page).
#

#
#  Section 1. Usage instructions
#
#  moss-submit.py [-l language] [-d] [-b basefile1] ... [-b basefilen] [-m #] [-c "string"] file1 file2 file3 ...
#
# The -l option specifies the source language of the tested programs.
# Moss supports many different languages; see the variable "languages" below for the
# full list.
#
# Example: Compare the lisp programs foo.lisp and bar.lisp:
#
#    moss-submit.py -l lisp foo.lisp bar.lisp
#
#
# The -d option specifies that submissions are by directory, not by file.
# That is, files in a directory are taken to be part of the same program,
# and reported matches are organized accordingly by directory.
#
# Example: Compare the programs foo and bar, which consist of .c and .h
# files in the directories foo and bar respectively.
#
#    moss-submit.py -d foo/*.c foo/*.h bar/*.c bar/*.h
#
# Example: Each program consists of the *.c and *.h files in a directory under
# the directory "assignment1."
#
#    moss-submit.py -d assignment1/*/*.h assignment1/*/*.c
#
#
# The -b option names a "base file".  Moss normally reports all code
# that matches in pairs of files.  When a base file is supplied,
# program code that also appears in the base file is not counted in matches.
# A typical base file will include, for example, the instructor-supplied
# code for an assignment.  Multiple -b options are allowed.  You should
# use a base file if it is convenient; base files improve results, but
# are not usually necessary for obtaining useful information.
#
# IMPORTANT: Unlike previous versions of moss, the -b option *always*
# takes a single filename, even if the -d option is also used.
#
# Examples:
#
#  Submit all of the C++ files in the current directory, using skeleton.cc
#  as the base file:
#
#    moss-submit.py -l cc -b skeleton.cc *.cc
#
#  Submit all of the ML programs in directories asn1.96/* and asn1.97/*, where
#  asn1.97/instructor/example.ml and asn1.96/instructor/example.ml contain the base files.
#
#    moss-submit.py -l ml -b asn1.97/instructor/example.ml -b asn1.96/instructor/example.ml -d asn1.97/*/*.ml asn1.96/*/*.ml
#
# The -m option sets the maximum number of times a given passage may appear
# before it is ignored.  A passage of code that appears in many programs
# is probably legitimate sharing and not the result of plagiarism.  With -m N,
# any passage appearing in more than N programs is treated as if it appeared in
# a base file (i.e., it is never reported).  Option -m can be used to control
# moss' sensitivity.  With -m 2, moss reports only passages that appear
# in exactly two programs.  If one expects many very similar solutions
# (e.g., the short first assignments typical of introductory programming
# courses) then using -m 3 or -m 4 is a good way to eliminate all but
# truly unusual matches between programs while still being able to detect
# 3-way or 4-way plagiarism.  With -m 1000000 (or any very
# large number), moss reports all matches, no matter how often they appear.
# The -m setting is most useful for large assignments where one also a base file
# expected to hold all legitimately shared code.  The default for -m is 10.
#
# Examples:
#
#   moss-submit.py -l pascal -m 2 *.pascal
#   moss-submit.py -l cc -m 1000000 -b mycode.cc asn1/*.cc
#
#
# The -c option supplies a comment string that is attached to the generated
# report.  This option facilitates matching queries submitted with replies
# received, especially when several queries are submitted at once.
#
# Example:
#
#   moss-submit.py -l scheme -c "Scheme programs" *.sch
#
# The -n option determines the number of matching files to show in the results.
# The default is 250.
#
# Example:
#   submit.py -c java -n 200 *.java
# The -x option sends queries to the current experimental version of the server.
# The experimental server has the most recent Moss features and is also usually
# less stable (read: may have more bugs).
#
# Example:
#
#   moss-submit.py -x -l ml *.ml
#


#
# Section 2.  Installation instructions.
#
# You may need to change the very first line of this script
# if python is not in /bin on your system.  Just replace /bin
# with the pathname of the directory where python resides.
#
# Also note that this script is written for python 2.7.  If this is not the
# default on your system, you may have to change the first line of this
# file to point to the python 2.7 interpreter. 
#

#
#  3. Standard Copyright
#
# Copyright (c) 1997 The Regents of the University of California.
# All rights reserved.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose, without fee, and without written agreement is hereby granted,
# provided that the above copyright notice and the following two
# paragraphs appear in all copies of this software.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT
# OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF
# CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
# ON AN "AS IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATION TO
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
#
# STOP.  It should not be necessary to change anything below this line
# to use the script.

import click
import os
import socket

LANGUAGES = ["c", "cc", "java", "ml", "pascal", "ada", "lisp", "scheme",
             "haskell", "fortran", "ascii", "vhdl", "perl", "matlab",
             "python", "mips", "prolog", "spice", "vb", "csharp", "modula2",
             "a8086", "javascript", "plsql"]

SERVER = 'moss.stanford.edu'
PORT = 7690
NOREQ = "Request not sent."


@click.command()
@click.option("--language", "-l", default="c", help="Source file language")
@click.option("--maxmatches", "-m", default=10, help="Max number of occurences of a block before it is ignored")
@click.option("--groupbydir/--no-groupbydir", "-d/", default=False, help="Files grouped according to user in directories")
@click.option("--experimental", "-x", is_flag=True, default=False, help="Enable experimental features")
@click.option("--comment", "-c", default="", help="Comment")
@click.option("--show", "-n", default=250, help="Number of results to show")
@click.option("--base", "-b", default=[], multiple=True, help="A file of source code common to all submissions")
@click.argument("src", nargs=-1)
def cli(language, maxmatches, groupbydir, experimental, comment, show, base, src):
    submit(src, l=language, m=maxmatches, d=groupbydir, x=experimental, c=comment, n=show, b=list(base))


def are_valid(files):
    """Check if a set of files are valid uploads"""
    return files_exist(files) and files_readable(files) and files_not_dirs(files)


def files_exist(files):
    """Check if a set of files all exist"""
    for f in files:
        if not os.path.exists(f):
            return False
    return True


def files_readable(files):
    """Check if a set of files are all readable"""
    for f in files:
        if not os.access(f, os.R_OK):
            return False
    return True


def files_not_dirs(files):
    """Check if a set of files are all regular files"""
    for f in files:
        if not os.path.isfile(f):
            return False
    return True


def upload_file(sock, filepath, fileid, lang):
    """Upload a file to socket"""
    print("Uploading %s... " % filepath, end="")
    size = os.stat(filepath).st_size
    sock.send("file %d %s %d %s\n" % (fileid, lang, size, filepath))
    with open(filepath) as f:
        for line in f:
            sock.send(line)
    print("done.")


def configure_moss(sock, l, m, d, x, n):
    """Configure the connection according to user options"""
    sock.send("moss %d\n" % USERID)
    sock.send("directory %d\n" % d)
    sock.send("X %d\n" % x)
    sock.send("maxmatches %d\n" % m)
    sock.send("show %d\n" % n)
    # Check if language really supported (This was in perl script, idk why though)
    sock.send("language %s\n" % l)
    msg = sock.recv(32).strip()
    if msg == "no":
        sock.send("end\n")
        raise Exception("Invalid language.")


def submit(src, l="c", m=10, d=False, x=False, c="", n=250, b=None):
    """Submit a set of files to the moss server.  Returns the link"""
    if l not in LANGUAGES:
        raise Exception("Invalid language: " + repr(l))
    if not isinstance(m, int):
        raise Exception("m must be an integer: " + repr(m))
    if not isinstance(b, list):
        raise Exception("b must be a list: " + repr(b))
    if not isinstance(c, basestring):
        raise Exception("c must be a comment string: " + repr(c))
    if not isinstance(n, int):
        raise Exception("n must be an integer: " + repr(n))

    if not are_valid(b):
        raise Exception("b contain only readble files")
    if not are_valid(src):
        raise Exception("A submitted file is not a readable file.")

    sock = socket.socket(family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    sock.settimeout(None)
    sock.connect((SERVER, PORT))
    configure_moss(sock, l=l, m=m, d=d, x=x, n=n)

    # upload any base files
    for base_file in b:
        upload_file(sock, base_file, 0, l)

    # upload source files
    for i, source_file in enumerate(src):
        upload_file(sock, source_file, i+1, l)

    sock.send("query 0 %s\n" % c)
    print("Query submitted.  Waiting for the server's response...")
    msg = sock.recv(4096)
    print(msg)
    sock.send("end\n")
    sock.close()
    return msg

if __name__=="__main__":
    cli()
