import sys
from clingo import Control, parse_program

import cherrypy
import json
from bson import json_util

from termprocessor.processor import ModelProcessor, Term
from utilities.userutil import UserHandler

@cherrypy.popargs('user')
class ASPWeb(object):
    terms = []
    mProcessor = ModelProcessor()
    userHandler = UserHandler()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def addTerm(self, user):
        kbJson = cherrypy.request.json
        try:
            for term in kbJson["terms"]:
                termAdded = Term()
                termAdded.termFromJson(self.mProcessor.termDefinitions, term)
                self.userHandler.addTerm(user, termAdded)
            return { "Result" : "Success" }
        except Exception as e:
            return { "Result" : "Failed", "Reason" : e.message }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def showTerms(self, user):
        allTerms = json.dumps(self.userHandler.getAllTerms(user), default=json_util.default)
        print allTerms
        return allTerms

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def getOptimumModel(self, user):
        prg = Control()
        prg.load("../scenarios/test.lp")
        self.terms = self.userHandler.getAllTerms(user)
        print self.terms

        with prg.builder() as prgBuilder:
            for termBson in self.terms:
                print termBson
                termObject = Term()
                termObject.termFromJson(self.mProcessor.termDefinitions, termBson)
                symTerm = '' + str(termObject.toSymbol(self.mProcessor)) + '.'
                parse_program(symTerm, lambda addTerm: prgBuilder.add(addTerm))
        self.userHandler.clearCollection(user)
        try:
            solverOutput = self.mProcessor.solveControl(prg)
            return solverOutput
        except Exception as e:
            print e
            return { "Result" : "Failed", "Reason" : e.message }

cherrypy.server.socket_host =  '0.0.0.0'
cherrypy.quickstart(ASPWeb())