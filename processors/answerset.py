''' 
    ModelProcessor python module for clingo5.
    This module is designed to process Models from clingo5 output
    into JSON format for web API / external application usage.
    
    This can be expanded on to reason about other services over low-
    energy bluetooth devices or other file formats
'''

from clingo import Symbol, SymbolType, Function, Number, String, parse_term
import json

class JsonAndPredicateProcessor:
    termDefinitions = {}
    modelTerms = []
    models = []
    modelSymbols = []

    def __init__(self, fromFile=False):
        if fromFile:
            self.loadTermDefinitions()

    def loadTermDefinitions(self):
        with open('terms.json') as termDefFile:
            termDefs = json.load(termDefFile)
            for termDef in termDefs:
                self.termDefinitions.update({termDef: termDefs[termDef]})

    def addTermDefinition(self, termDefinition):
        symFunc = parse_term(termDefinition)
        self.termDefinitions[symFunc.name] = {}
        self.termDefinitions[symFunc.name]["type"] = "Function"
        self.termDefinitions[symFunc.name]["variableNames"] = []
        for varName in symFunc.arguments:
            self.termDefinitions[symFunc.name]["variableNames"] = varName.__str__()
        self.termDefinitions[symFunc.name]["arity"] = len(symFunc.arguments)
        self.termDefinitions[symFunc.name]["terms"] = {}

        for name in symFunc.arguments:
            nameStr = str(name)
            if nameStr in self.termDefinitions:
                self.termDefinitions[symFunc.name]["terms"].update({nameStr: "Function"})
            else:
                if name.type == SymbolType.Number:
                    self.termDefinitions[symFunc.name]["terms"].update({nameStr : "Number"})
                elif name.type == SymbolType.String:
                    self.termDefinitions[symFunc.name]["terms"].update({nameStr: "String"})
        with open('terms.json', 'w') as termFile:
            json.dump(self.termDefinitions, termFile, indent=4)

    def answerSetToJson(self, outputDefinition, answerSetSymbols):
        modelJson = {"predicatesJSON" : [], "rawPredicates": []}
        print outputDefinition
        for symbol in answerSetSymbols:
            print "-- " + str(symbol)
            if symbol.name in outputDefinition["predicates"]:
                try:
                    predicateToAdd = Predicate(outputDefinition["predicates"], symbol)
                    modelJson["predicatesJSON"].append( predicateToAdd.termJson )
                except Exception, e:
                    print "--- Unable to add predicate in answer set ---"
                    print e
            else:
                modelJson["rawPredicates"].append(symbol)

        return modelJson

    def jsonToSymbols(self, jsonSymbols, inputDefinition):
        pass
 
    def jsonToSymbol(self, jsonSymbol):
        symbolName = jsonSymbol["predicateName"]
        symbolArgs = []
        for varName in self.termDefinitions[symbolName]["variableNames"]:
            symVar = jsonSymbol[varName]
            symType = type(symVar)
            if symType == str or symType == unicode:
                symbolArgs.append(String(symVar))
            elif symType == int:
                symbolArgs.append(Number(symVar))
            elif symType == dict:
                funcJson = dict(symVar)
                funcJson.update( { "name" : varName } )
                funcSym = self.jsonToSymbol( funcJson )
                symbolArgs.append(funcSym)
        
        funcSymbol = Function(symbolName, symbolArgs)
        return funcSymbol

class Predicate:
    name = ""
    termJson = {}

    def __init__(self, termDefinitions=None, symbol=None):
        if termDefinitions != None and symbol != None:
            print "--- CONVERTING SYMBOL ---"
            print termDefinitions
            self.termJson = {}
            self.name = ""
            if symbol.type == SymbolType.Function:
                self.name = symbol.name
                self.termDefinition = termDefinitions[self.name]
                symArgs = symbol.arguments # Actual Values
                varNames = termDefinitions[self.name]["variableNames"] # Name Lookup

                if len(varNames) != len(symArgs):
                    raise Exception("Output definition did not match up with logic program output!")

                self.termJson.update({"name": self.name})

                for ix in range(0, len(symArgs)):
                    if symArgs[ix].type == SymbolType.String:
                        self.termJson.update({varNames[ix] : symArgs[ix].string})
                    elif symArgs[ix].type == SymbolType.Number:
                        self.termJson.update({varNames[ix]: symArgs[ix].number})
                    else:
                        funcTerm = Predicate(termDefinitions, symArgs[ix])
                        self.termJson.update({varNames[ix] : funcTerm.termJson })

    def predicateFromJson(self, termDefinitions, symbolJson):
        self.termJson = symbolJson
        self.name = self.termJson['name']

    def fromInputJson(self, termDefinitions, predicateJson):
        self.name = predicateJson["predicateName"]
        self.termJson = predicateJson
    
    def predicateFromBson(self, termDefinitions, symbolJson):
        self.termJson = json.loads(symbolJson)
        self.name = self.termJson['name']
    
    def toSymbol(self, modelProcessor):
        return modelProcessor.jsonToSymbol(self.termJson)
