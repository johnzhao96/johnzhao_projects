#!/usr/bin/env python

"""
Jiayang Zhao
run_translator: Script for running pptx_to_html on multiple PowerPoints at once.
"""

import sys
import os
from os import listdir
from os.path import isfile, join

"""
Usage:
'./run_translator.py <presentations directory> <logfiles directory>'
"""

offset = 0
    
if len(sys.argv) - offset < 2:
    print("Error: not enough arguments")
    exit(-1)

presdir = sys.argv[offset + 1]
logsdir = sys.argv[offset + 2]

presentations = [f for f in listdir(presdir) if (isfile(join(presdir, f)) and f[-5:] == '.pptx')]

for pres in presentations:
    os.system('python pptx_to_html.py "{}" "{}{}.html"'.format(
        join(presdir, pres), 
        join(logsdir,'log_'), 
        pres[:-5])
    )
