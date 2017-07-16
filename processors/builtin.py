from definitions.builtin import DefinitionsMapping
from answerset import JsonAndPredicateProcessor

class DefinitionsProcessor:

    answerSetProcessor = JsonAndPredicateProcessor()
    defMapping = DefinitionsMapping()

    def definitionsToJSON(self, definitionsAnswerSet):
        definitionsJSON = self.answerSetProcessor.answerSetToJson(self.defMapping.definitionsMapping, definitionsAnswerSet)
        print definitionsJSON