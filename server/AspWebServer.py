import cherrypy
import json
import sys
sys.path.insert(0, "/home/chrx/smartHome/testFiles/aspWeb/ModelProcessor")
from ModelProcessor import ModelProcessor, Term
from clingo import Control, parse_program

class ASPWeb(object):
    terms = []
    mProcessor = ModelProcessor()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def addFact(self):
        kbJson = cherrypy.request.json
        try:
            for term in kbJson["terms"]:
                termAdded = Term()
                termAdded.termFromJson(self.mProcessor.termDefinitions, term)
                self.terms.append(termAdded)
            
            return { "Result" : "Success" }
        except Exception as e:
            return { "Result" : "Failed", "Reason" : e.message } 

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def showFacts(self):
        eventsToSchedule = {}
        for event in self.terms:
            eventsToSchedule.update( event.termJson )

        return eventsToSchedule

    
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def getOptimumModel(self):
        prg = Control()
        prg.load("../../scenarios/test.lp")
        with prg.builder() as prgBuilder: 
            for term in self.terms:
                symTerm = '' + str(term.toSymbol(self.mProcessor)) + '.'
                parse_program(symTerm, lambda addTerm: prgBuilder.add(addTerm))
        try:
            solverOutput = self.mProcessor.solveControl(prg)
            return solverOutput
        except Exception as e:
            print e
            return { "Result" : "Failed", "Reason" : e.message }


cherrypy.quickstart(ASPWeb())
