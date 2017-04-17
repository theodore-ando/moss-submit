# MOSS Submit

This script is a python implementation of the submission script for MOSS (Measure of Software Similarity).  

## Contents

1. [Getting Started](https://github.com/theodore-ando/moss-submit#getting-started)
2. [Authors](https://github.com/theodore-ando/moss-submit#authors)
3. [License](https://github.com/theodore-ando/moss-submit#license)
4. [Acknowledgements](https://github.com/theodore-ando/moss-submit#acknowledgements)

## Getting Started

These steps will get you working either locally for development purposes or in a production pipeline.

### Prerequisites

You will need the python library [`click`](http://click.pocoo.org/5/) to use this script.  To install, simply `pip install click`.

You will also need a MOSS account, which you can get by following the instructions [here](http://moss.stanford.edu). 

### Installation

No installation needed, just copy the script wherever you want or add it to your python path.

### Usage

```
submit.py [-l language] [-d] [-b basefile1] ... [-b basefilen] [-m #] [-c "string"] file1 file2 file3 ...
```

The `-l` option specifies the source language of the tested programs.
Moss supports many different languages; see the variable "languages" below for the
full list.

Example: Compare the lisp programs foo.lisp and bar.lisp:
```
   submit.py -l lisp foo.lisp bar.lisp
```
The `-d` option specifies that submissions are by directory, not by file.
That is, files in a directory are taken to be part of the same program,
and reported matches are organized accordingly by directory.

Example: Compare the programs foo and bar, which consist of .c and .h
files in the directories foo and bar respectively.
```
   submit.py -d foo/*.c foo/*.h bar/*.c bar/*.h
```
Example: Each program consists of the *.c and *.h files in a directory under
the directory "assignment1."
```
   submit.py -d assignment1/*/*.h assignment1/*/*.c
```
The `-b` option names a "base file".  Moss normally reports all code
that matches in pairs of files.  When a base file is supplied,
program code that also appears in the base file is not counted in matches.
A typical base file will include, for example, the instructor-supplied
code for an assignment.  Multiple -b options are allowed.  You should
use a base file if it is convenient; base files improve results, but
are not usually necessary for obtaining useful information.

IMPORTANT: Unlike previous versions of moss, the -b option *always*
takes a single filename, even if the -d option is also used.

Examples:

 Submit all of the C++ files in the current directory, using skeleton.cc
 as the base file:

   submit.py -l cc -b skeleton.cc *.cc

 Submit all of the ML programs in directories asn1.96/* and asn1.97/*, where
 asn1.97/instructor/example.ml and asn1.96/instructor/example.ml contain the base files.

   submit.py -l ml -b asn1.97/instructor/example.ml -b asn1.96/instructor/example.ml -d asn1.97/*/*.ml asn1.96/*/*.ml

The -m option sets the maximum number of times a given passage may appear
before it is ignored.  A passage of code that appears in many programs
is probably legitimate sharing and not the result of plagiarism.  With -m N,
any passage appearing in more than N programs is treated as if it appeared in
a base file (i.e., it is never reported).  Option -m can be used to control
moss' sensitivity.  With -m 2, moss reports only passages that appear
in exactly two programs.  If one expects many very similar solutions
(e.g., the short first assignments typical of introductory programming
courses) then using -m 3 or -m 4 is a good way to eliminate all but
truly unusual matches between programs while still being able to detect
3-way or 4-way plagiarism.  With -m 1000000 (or any very
large number), moss reports all matches, no matter how often they appear.
The -m setting is most useful for large assignments where one also a base file
expected to hold all legitimately shared code.  The default for -m is 10.

Examples:

  submit.py -l pascal -m 2 *.pascal
  submit.py -l cc -m 1000000 -b mycode.cc asn1/*.cc


The -c option supplies a comment string that is attached to the generated
report.  This option facilitates matching queries submitted with replies
received, especially when several queries are submitted at once.

Example:

  submit.py -l scheme -c "Scheme programs" *.sch

The -n option determines the number of matching files to show in the results.
The default is 250.

Example:
  submit.py -c java -n 200 *.java
The -x option sends queries to the current experimental version of the server.
The experimental server has the most recent Moss features and is also usually
less stable (read: may have more bugs).

Example:

  submit.py -x -l ml *.ml


## Authors

## License

## Acknowledgements