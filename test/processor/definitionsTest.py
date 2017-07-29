import clingo

class QueryDefinitionProcessor:
    def on_model(self, model):
        print model

    def on_finish(self, res):
        print res

    def setupQueryFromDefinition(self):
        prg = clingo.Control()
        prg.load("defTest.lp")
        prg.ground([("definitions", [])])
        solveFuture = prg.solve_async(self.on_model, self.on_finish)
        solveFuture.wait()


queryDefiner = QueryDefinitionProcessor()
queryDefiner.setupQueryFromDefinition()
