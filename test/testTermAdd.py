# Module for generating test data to POST to /addEvent.
# Just run the script and copy into a REST client

import ModelProcessor as mp
import clingo
from ModelProcessor import Term
import os
from random import randint
import json

m = mp.ModelProcessor()

for subdir, dirs, files in os.walk('../scenarios'):
    for lpFile in files:
        ext = os.path.splitext(os.path.basename(lpFile))[1]
        fileName = os.path.splitext(os.path.basename(lpFile))[0]
        if ext == '.lp' and fileName != 'test' and fileName != 'maxtest':
            with open('../scenarios/' + lpFile,'r') as openLpFile:
                if ( randint(0,3) == 3 ):
                    lines = list(line for line in (l.strip() for l in openLpFile) if line and line[0] != '%')
                    for line in lines:
                        line = line.replace(".", "")
                        f = clingo.parse_term(line)
                        t = Term(m.termDefinitions, f)
                        print json.dumps(t.termJson)
                        print ","
'''
f = clingo.parse_term('event_duration("laundry",90)')
t = Term(m.termDefinitions, f)
print t.termJson'''

