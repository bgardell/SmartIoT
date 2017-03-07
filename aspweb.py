import sys
from clingo import Control, parse_program

import cherrypy
import json
from bson import json_util

from termprocessor.processor import ModelProcessor, Term
from utilities.userutil import UserHandler
from utilities.skillutil import SkillHandler

@cherrypy.popargs('user')
class ASPWeb(object):
    terms = []
    mProcessor = ModelProcessor()
    userHandler = UserHandler()
    skillHandler = SkillHandler()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def addSkill(self, user):
        skillJson = cherrypy.request.json
        addSkillResult = self.skillHandler.addSkill(skillJson)
        return addSkillResult

    @cherrypy.expose
    @cherrypy.popargs('skillName')
    @cherrypy.tools.json_out()
    def skill(self, skillName):
        skillInfo = self.skillHandler.getSkill(skillName)
        return skillInfo

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllSkills(self):
        skillInfo = self.skillHandler.getAllSkills()
        print skillInfo
        return skillInfo

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
        allTerms = self.userHandler.getAllTerms(user)
        allTermsJson = {"terms": []} 
        
        for term in allTerms:
            allTermsJson["terms"].append(term)
       
        print allTermsJson
        return allTermsJson


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def clearTerms(self, user):
        self.userHandler.clearCollection(user)
        return { "Result" : "Success" }


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def getOptimumModel(self, user):
        prg = Control()
        prg.load("../scenarios/simpTest.lp")
        self.terms = self.userHandler.getAllTerms(user)

        with prg.builder() as prgBuilder:
            for termBson in self.terms:
                termObject = Term()
                termObject.termFromBson(self.mProcessor.termDefinitions, termBson)
                symTerm = '' + str(termObject.toSymbol(self.mProcessor)) + '.'
                parse_program(symTerm, lambda addTerm: prgBuilder.add(addTerm))
        try:
            solverOutput = self.mProcessor.solveControl(prg)
            return solverOutput
        except Exception as e:
            print e
            return { "Result" : "Failed", "Reason" : e.message }
    
    @cherrypy.expose
    def index(self):
        return file("schedulerHTML/viewEvents.html")

cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'tools.staticdir.on': True,
                'tools.staticdir.dir':
                '/home/ubuntu/aspWeb/schedulerHTML'
                               })


cherrypy.quickstart(ASPWeb())
