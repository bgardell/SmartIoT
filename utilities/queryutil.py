from pymongo import MongoClient
import base64
import os

from validators.queryvalidator import QueryValidator
from validators.validationerror import ValidationError

class QueryHandler:
    def __init__(self):
        self.client = MongoClient()
        self.queryDb = self.client.queryDatabase
        self.queryCollection = self.queryDb["queries"]
        self.queryValidator = QueryValidator()

    def addQuery(self, queryInfo):
        queryName = queryInfo["queryName"]
        try:
            self.queryValidator.validateInput(queryInfo)
        except ValidationError, e:
            return {"Result" : "Failure", "Reason" : e.message}

        if self.queryCollection.find({"queryName" : queryName}).count() > 0:
            return { "Result " : "Failure", "Reason" : "Query Already Exists!"}

        queryInfo["mainLogic"] = str(queryInfo["mainLogic"])
        newQuery = Query(queryInfo)
        queryId = self.queryCollection.insert_one(newQuery.toJson()).inserted_id
        return {"Result" : "Success", "QueryId" : str(queryId)}

    def deleteQuery(self, queryName):
        try:
            removeResult = self.queryCollection[queryName].remove({"queryName" : queryName })
            fileString = "../scenarios/" + queryName
            if os.path.exists(fileString):
                os.remove(fileString)
        except Exception as e:
            print "Could not delete query " + e.message
            return {"Result" : "Failure", "Reason" : e.message}
        print "Deleted --- " + str(removeResult)
        return {"Result" : "Success"}

    def getQueryInfo(self, queryName):
        queryBson = self.queryCollection.find_one({"queryName": queryName})
        queryJson = Query(queryBson).toJson()
        return queryJson

    def getAllQueries(self):
        allQueries = {"queries":[]}
        queriesBson = self.queryCollection.find()
        for query in queriesBson:
            allQueries["queries"].append(self.queryToJson(query))
        return allQueries

    def queryToJson(self, query):
        if type(query) == dict and "id" in query:
            query.pop("_id")
        return query

class Query:
    queryName = ""
    queryLogic = ""
    queryInput = {}
    queryOutput = {}

    def __init__(self, queryJson):
        self.queryJson = queryJson
        self.queryName = queryJson["queryName"]
        self.queryLogic = queryJson["mainLogic"]
        self.queryInput = queryJson["inputDefinition"]
        self.queryOutput = queryJson["outputDefinition"]
        self.devicesUsed = queryJson["devicesUsed"]

    def toJson(self):
        queryJson = {}
        queryJson["queryName"] = self.queryName
        queryJson["mainLogic"] = self.queryLogic
        queryJson["inputDefinition"] = self.queryInput
        queryJson["outputDefinition"] = self.queryOutput
        queryJson["devicesUsed"] = self.devicesUsed
        return queryJson
