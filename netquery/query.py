import os

from answersetsolving.solver import ClingoSolver
from database.devicedb import DeviceDatabase
from database.querydb import QueryDatabase
from processors.answerset import JsonAndPredicateProcessor
from network.http import HTTPOperations

class QueryHandler:
    '''
    This class handles query execution and knowledge dependency resolution calls.
    '''
    def __init__(self):
        self.deviceDatabase = DeviceDatabase()
        self.queryDatabase = QueryDatabase()
        self.solver = ClingoSolver()
        self.processor = JsonAndPredicateProcessor()
        self.networkDependencyHandler = HTTPOperations()

    def solveQueryOutputJson(self, queryName):
        '''
        This will solve the query and then process the Answer Sets for network output.
        This will also call the networkHandler to output the JSON to the output device.
        :param queryName:
        :return:
        '''
        solverOutput = self.solveQuery(queryName)
        queryInfo = self.queryDatabase.getQueryInfo(queryName)
        outputDefinition = queryInfo["outputDefinition"]
        jsonOutput = self.processor.answerSetToJson(outputDefinition, solverOutput)
        jsonOutput["rawPredicates"] = str(jsonOutput["rawPredicates"])

        if "locations" in outputDefinition:
            for outputLocation in outputDefinition["locations"]:
                self.networkDependencyHandler.postKnowledgeOutput(jsonOutput["predicatesJSON"], outputLocation)

        return jsonOutput

    def solveQuery(self, queryName):
        '''
        Retrieve all knowledge dependencies, map them to predicates,
        then lastly add them into the main logic module and solve the module.
        '''
        queryInfo = self.queryDatabase.getQueryInfo(queryName)
        queryInputPredicates = []

        if "externalServices" in queryInfo["knowledgeDependencies"]:
            for externalService in queryInfo["knowledgeDependencies"]["externalServices"]:
                print str(externalService) + " RESOLVING "
                externalServiceData = self.networkDependencyHandler.retrieveNetworkDependency(externalService)
                if externalServiceData:
                    self.deviceDatabase.addData(externalService["name"], externalServiceData)

        dataMappingInfo = queryInfo["devicesUsed"]
        databasePredicates = self.deviceDatabase.mapCurrentDataToPredicates(dataMappingInfo)

        queryDependencyOutput = []
        if "queries" in queryInfo["knowledgeDependencies"]:
            for dependentQuery in queryInfo["knowledgeDependencies"]["queries"]:
                dependentQueryOutput = self.solveQuery(dependentQuery)
                for symbol in dependentQueryOutput:
                    queryDependencyOutput.append(str(symbol))

        queryInputPredicates.extend(databasePredicates)
        queryInputPredicates.extend(queryDependencyOutput)

        try:
            fileString = "../scenarios/" + queryInfo["queryName"]

            if not os.path.exists(fileString):
                with open(fileString, "w+") as f:
                    f.write(queryInfo["mainLogic"])

            solverOutput = self.solver.solveProgram(fileString, queryInputPredicates)
            return solverOutput
        except Exception as e:
            print "Exception in query solving"
            print e
            return {"Result": "Failed", "Reason": e.message}