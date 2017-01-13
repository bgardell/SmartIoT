''' 
    ModelProcessor python module for clingo5.
    This module is designed to process Models from clingo5 output
    into JSON format for web API / external application usage.
    
    This can be expanded on to reason about other services over low-
    energy bluetooth devices or other file formats
'''

from clingo import Symbol, SymbolType, Function, Number, String, parse_term
import json

class ModelProcessor:
    termDefinitions = {}
    modelTerms = []
    models = []

    def __init__(self):
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

    def addSymbol(self, symbol):
        term = Term(self.termDefinitions, symbol)
        self.modelTerms.append(term)

    def solveControl(self, control):
        try:
            control.ground([("base", [])])
            solveFuture = control.solve_async(self._on_model, self._on_finish)
            solveFuture.wait()
            for term in self.modelSymbols[0]:
                self.addSymbol(term)

            modelJson = []
            for term in self.modelTerms:
                modelJson.append( term.termJson )
            print modelJson
            print " Model JSON: "
            self.modelTerms = []
            return modelJson
        except Exception as e:
            print "Term not defined or input incorrect! Issue was with " + e.message
        
        return []
    
    def _on_model(self, model):
        self.modelSymbols = []
        self.modelSymbols.append( model.symbols(terms=True, shown=True) )

    def _on_finish(self, res, didCancel=False):
        print res
    
    
    def jsonToSymbol(self, jsonSymbol):
        symbolName = jsonSymbol["name"]
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

class Term:
    name = ""
    termJson = {}

    def __init__(self, termDefinitions=None, symbol=None):
        if termDefinitions != None and symbol != None:
            self.termJson = {}
            self.name = ""
            if symbol.type == SymbolType.Function:
                self.name = symbol.name
                self.termDefinition = termDefinitions[self.name]
                symArgs = symbol.arguments # Actual Values

                varNames = termDefinitions[self.name]["variableNames"] # Name Lookup
                self.termJson.update({"name": self.name})

                for ix in range(0, len(symArgs)):
                    if symArgs[ix].type == SymbolType.String:
                        self.termJson.update({varNames[ix] : symArgs[ix].string})
                    elif symArgs[ix].type == SymbolType.Number:
                        self.termJson.update({varNames[ix]: symArgs[ix].number})
                    else:
                        funcTerm = Term(termDefinitions, symArgs[ix])
                        self.termJson.update({varNames[ix] : funcTerm.termJson })

    def termFromJson(self, termDefinitions, symbolJson):
        self.termJson = symbolJson
        self.name = symbolJson["name"]
    
    def toSymbol(self, modelProcessor):
        return modelProcessor.jsonToSymbol(self.termJson)
