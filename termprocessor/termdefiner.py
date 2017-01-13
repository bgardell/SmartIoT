# Goal is to generate term definitions based on a textfile input
# schedule("Event_Name", 0, date) as an example. 
# Any non-integer variable outside of quotes is treated as a function and requires definition prior to use
from clingo import parse_term

def defineTerm(termDef):
    funcSym = parse_term(termDef)
    for arg in funcSym.arguments:
        print arg
