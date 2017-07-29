import clingo
from answerset import JsonAndPredicateProcessor


class QueryDefinitionProcessor:
    answerSetProcessor = JsonAndPredicateProcessor()
    queryOutput = {
        "predicates":
        {
                "queryName": {
                    "arity": 1,
                    "variableNames": ["QueryName"]
                },
                "databaseDependency": {
                    "arity": 2,
                    "variableNames": ["CollectionName", "DataMappingName"]
                },
                "networkDependency": {
                    "arity": 2,
                    "variableNames": ["NetworkLocation", "DataMappingName"]
                },
                "queryDependency": {
                    "arity": 1,
                    "variableNames": ["QueryName"]
                },
        }
    }

    def on_model(self, model):
        print model
        self.symbols = model.symbols()

    def on_finish(self, res):
        print res

    def setupQueryFromDefinition(self):
        prg = clingo.Control()
        prg.load("defTest.lp")
        prg.ground([("definitions", [])])
        solveFuture = prg.solve_async(self.on_model, self.on_finish)
        solveFuture.wait()
        print self.symbols
        jsonOutput = self.answerSetProcessor.answerSetToJson(self.queryOutput, self.symbols)
        print jsonOutput


queryDefiner = QueryDefinitionProcessor()
queryDefiner.setupQueryFromDefinition()
