import os.path
from clingo import *

from database.devicedb import DeviceDatabase
from processors.answerset import Predicate, JsonAndPredicateProcessor


class ClingoSolver(object):
    mProcessor = JsonAndPredicateProcessor()
    #queryHandler = QueryHandler()

    def validateInput(self, inputDef, input):
        pass

    def solveProgram(self, logicFile=None, predicatesList=None):
        prg = Control()
        self.modelSymbols = []
        try:
            prg.load(logicFile)
        except Exception, e:
            print "Exception in Clingo solver when trying to load program"
            print e.message
            print e.args
            return {"Result" : "Failure", "Reason" : "Could not load main logic"}

        with prg.builder() as prgBuilder:
            for predicate in predicatesList:
                parse_program(predicate + '.', lambda symbol: prgBuilder.add(symbol))
        try:
            print "--- Solving Program ---"
            prg.ground([("base", [])])
            solveFuture = prg.solve_async(self._on_model, self._on_finish)
            solveFuture.wait()
            return self.modelSymbols.pop()
        except Exception as e:
            print "Exception in Clingo solver when trying to solve the program"
            print e
            return {"Result": "Failed", "Reason": e.message}

    def _on_model(self, model):
        self.modelSymbols.append( model.symbols(terms=True, shown=True) )

    def _on_finish(self, res, didCancel=False):
        pass

