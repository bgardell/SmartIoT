import cherrypy

from symbolprocessor.processor import ModelProcessor
from utilities.deviceutil import DeviceHandler
from utilities.queryutil import QueryHandler
from utilities.clingoutil import ClingoSolver

class ASPWeb(object):
    terms = []
    mProcessor = ModelProcessor()
    deviceHandler = DeviceHandler()
    queryHandler = QueryHandler()
    clingoSolver = ClingoSolver()

    @cherrypy.expose
    @cherrypy.popargs('deviceName')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def addDeviceData(self, deviceName):
        print "test"
        deviceData = cherrypy.request.json
        print deviceData
        addDataResult = self.deviceHandler.addData(deviceName, deviceData)
        return addDataResult

    @cherrypy.popargs('deviceName')
    @cherrypy.expose
    def clearDeviceData(self, deviceName):
        clearDataResult = self.deviceHandler.clearDeviceData(deviceName)
        return clearDataResult

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def addQuery(self):
        queryJson = cherrypy.request.json
        addQueryResult = self.queryHandler.addQuery(queryJson)
        return addQueryResult

    @cherrypy.expose
    @cherrypy.popargs('queryName')
    @cherrypy.tools.json_out()
    def getQueryInfo(self, queryName):
        queryInfo = self.queryHandler.getQueryInfo(queryName)
        queryInfo.pop("mainLogic")
        return queryInfo

    @cherrypy.expose
    @cherrypy.popargs('queryName')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def useQueryWithInput(self, queryName):
        queryInput = cherrypy.request.json

        queryInfo = self.queryHandler.getQueryInfo(queryName)
	if queryInfo is None:
            return {"Result" : "Failure", "Reason" : "Unable to fetch query info. Does this query exist?"}

        solverOutput = self.clingoSolver.solveSkillWithInput(queryInfo, queryInput)
        return solverOutput

    @cherrypy.expose
    @cherrypy.popargs('queryName')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def useQueryWithDatabase(self, queryName):
        queryInfo = self.queryHandler.getQueryInfo(queryName)

        if queryInfo is None:
            return {"Result": "Failure", "Reason": "Unable to fetch query info. Does this query exist?"}

        solverOutput = self.clingoSolver.solveQueryWithDeviceDatabase(queryInfo)
        return {"output" : str(solverOutput)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getQueryList(self):
        queryInfo = self.queryHandler.getAllQueries()
        return queryInfo
    
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'tools.staticdir.on': True,
                'tools.staticdir.dir':
                '/home/ubuntu/aspWeb/schedulerHTML'
                               })

cherrypy.quickstart(ASPWeb())
