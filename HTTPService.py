import cherrypy
from multiprocessing import Process
from database.devicedb import DeviceDatabase
from database.querydb import QueryDatabase
from netquery.query import QueryHandler
from processors.answerset import JsonAndPredicateProcessor

class HTTPService(Process):
    mProcessor = JsonAndPredicateProcessor()
    deviceDatabase = DeviceDatabase()
    queryDatabase = QueryDatabase()
    queryHandler = QueryHandler()

    @cherrypy.popargs('deviceName')
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def addDeviceData(self, deviceName):
        deviceData = cherrypy.request.json
        addDataResult = self.deviceDatabase.addData(deviceName, deviceData)
        return addDataResult

    @cherrypy.popargs('deviceName')
    @cherrypy.expose
    def clearDeviceData(self, deviceName):
        clearDataResult = self.deviceDatabase.clearDeviceData(deviceName)
        return clearDataResult

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def addQuery(self):
        queryJson = cherrypy.request.json
        addQueryResult = self.queryDatabase.addQuery(queryJson)
        return addQueryResult

    @cherrypy.expose
    @cherrypy.popargs('queryName')
    @cherrypy.tools.json_out()
    def deleteQuery(self, queryName):
        addQueryResult = self.queryDatabase.deleteQuery(queryName)
        return addQueryResult

    @cherrypy.expose
    @cherrypy.popargs('queryName')
    @cherrypy.tools.json_out()
    def getQueryInfo(self, queryName):
        queryInfo = self.queryDatabase.getQueryInfo(queryName)
        return queryInfo

    @cherrypy.expose
    @cherrypy.popargs('queryName')
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def useQueryWithDatabase(self, queryName):
        solverOutput = self.queryHandler.solveQueryOutputJson(queryName)
        print solverOutput
        return solverOutput

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getQueryList(self):
        queryInfo = self.queryHandler.getAllQueries()
        return queryInfo

