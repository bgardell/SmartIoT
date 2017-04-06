from clingo import *
from symbolprocessor.processor import Predicate, ModelProcessor
from deviceutil import DeviceHandler
import os.path

class ClingoSolver(object):
    mProcessor = ModelProcessor()

    def validateInput(self, inputDef, input):
        pass

    def solveQueryWithInput(self, queryInfo, queryInput):

        queryInputDef = queryInfo["inputDefinition"]
        queryOutputDef = queryInfo["outputDefinition"]
        queryFile = queryInfo["mainLogic"]

        for inputDefinition in queryInfo["inputDefinition"]["predicates"]:
            self.mProcessor.termDefinitions.update(inputDefinition)

        for outputDefinition in queryInfo["outputDefinition"]["predicates"]:
            self.mProcessor.termDefinitions.update(outputDefinition)

        prg = Control()
        try:
            prg.load("../scenarios/" + queryInfo["queryName"])
        except Exception, e:
            print e.message
            print e.args
            return {"Result" : "Failure", "Reason" : "Could not load file"}

        with prg.builder() as prgBuilder:
            for inputPredicate in queryInput["predicates"]:
                termObject = Predicate()
                termObject.fromInputJson(self.mProcessor.termDefinitions, inputPredicate)
                symTerm = '' + str(termObject.toSymbol(self.mProcessor)) + '.'
                parse_program(symTerm, lambda addTerm: prgBuilder.add(addTerm))
        try:
            solverOutput = self.mProcessor.solveControl(prg)
            return solverOutput
        except Exception as e:
            print e
            return {"Result": "Failed", "Reason": e.message}

    def solveQueryWithDeviceDatabase(self, queryInfo):
        deviceHandler = DeviceHandler()
        prg = Control()
        fileString = "../scenarios/" + queryInfo["queryName"]

        try:
            if os.path.exists(fileString):
                prg.load(fileString)
            else:
                with open(fileString, "w+") as f:
                    f.write(queryInfo["mainLogic"])
                prg.load(fileString)
        except Exception, e:
            print e.message
            print e.args
            return {"Result" : "Failure", "Reason" : "Could not load main logic"}

        dataMappingInfo = queryInfo["devicesUsed"]
        databasePredicates = deviceHandler.mapCurrentDataToPredicates(dataMappingInfo)
        with prg.builder() as prgBuilder:
            for dbPredicate in databasePredicates:
                parse_program(dbPredicate + '.', lambda addTerm: prgBuilder.add(addTerm))
        try:
            print "--- SOLVING WITH OUTPUT DEFINITION --- "
            print queryInfo["outputDefinition"]
            solverOutput = self.mProcessor.solveControlRawOutput(queryInfo["outputDefinition"][u'predicates'], prg)

            return solverOutput
        except Exception as e:
            print e
            return {"Result": "Failed", "Reason": e.message}