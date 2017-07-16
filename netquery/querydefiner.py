from answersetsolving.solver import ClingoSolver


class QueryDefiner:
    solver = ClingoSolver()

    def solveQueryDefinitions(self, queryDefinitionName):
        with open("../queryDefinitions/" + queryDefinitionName + ".lp") as f:
