from pymongo import MongoClient

class UserHandler:
    def __init__(self):
        self.client = MongoClient()
        self.termDb = self.client.terms

    def addTerm(self, userName, term):
        term_id = self.termDb[userName].insert_one(term.termJson).inserted_id
        return term_id

    def clearCollection(self, userName):
        try:
            self.termDb[userName].remove({})
        except Exception as e:
            print "Could not clear collection"

    def getAllTerms(self, userName):
        allTerms = []
        for term in self.termDb[userName].find():
            allTerms.append(term)
        return allTerms

class User:
    name = ""
    token = ""
