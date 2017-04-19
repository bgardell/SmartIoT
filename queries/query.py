import os

from answersetsolving.solver import ClingoSolver
from database.devicedb import DeviceDatabase
from database.querydb import QueryDatabase
from processors.answerset import JsonAndPredicateProcessor

class QueryHandler:
    def __init__(self):
        self.deviceDatabase = DeviceDatabase()
        self.queryDatabase = QueryDatabase()
        self.solver = ClingoSolver()
        self.processor = JsonAndPredicateProcessor()

    def solveQueryOutputJson(self, queryName):
        solverOutput = self.solveQuery(queryName)
        queryInfo = self.queryDatabase.getQueryInfo(queryName)
        jsonOutput = self.processor.answerSetToJson(queryInfo["outputDefinition"], solverOutput)
        jsonOutput["rawPredicates"] = str(jsonOutput["rawPredicates"])
        return jsonOutput

    def solveQuery(self, queryName):
        queryInfo = self.queryDatabase.getQueryInfo(queryName)
        queryInputPredicates = []

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
            print e
            return {"Result": "Failed", "Reason": e.message}