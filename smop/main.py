# SMOP -- Simple Matlab/Octave to Python compiler
# Copyright 2011-2016 Victor Leikehman
from os.path import splitext,basename
import version
import sys,cPickle,glob,os
import getopt,re
import lexer
import parse
import resolve
import backend
import options
import node,graphviz
import callgraph
import networkx as nx
import pickle
import readline
import graphviz

def main():
    if not options.filelist:
        options.parser.print_help()
        return
    if options.output == "-":
        fp = sys.stdout
    elif options.output:
        fp = open(options.output, "w")
    else:
        assert not options.output
        filename,filetype = splitext(basename(options.filelist[0]))
        options.output = filename+".py"
        fp = open(options.output, "w")

    print >> fp, "# Autogenerated with SMOP " + version.__version__
    print >> fp, "from __future__ import division"
    print >> fp, "from smop.core import *"
    if options.link:
        print >> fp, "from %s import *" % options.link
    print >> fp, "#", options.filename
            
    for i, options.filename in enumerate(options.filelist):
        try:
            if not options.filename.endswith((".m",".tst")):
                print "\tIgnored file: '%s' (unexpected file type)" % options.filename
                continue
            if os.path.basename(options.filename) in options.xfiles:
                print "\tExcluded file: '%s'" % options.filename
                continue
            if options.verbose:
                print options.filename
            buf = open(options.filename).read().replace("\r\n","\n")
            stmt_list=parse.parse(buf if buf[-1]=='\n' else buf+'\n')
            #assert None not in stmt_list                  
            if not stmt_list and options.strict:
                return
            if not options.no_resolve:
                G = resolve.resolve(stmt_list)
            if not options.no_backend:
                s = backend.backend(stmt_list)
                print >> fp, s
        except Exception as e:
            print e
            if options.strict:
                raise

if __name__ == "__main__":
    main()
