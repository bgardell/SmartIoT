from pymongo import MongoClient

class UserHandler:
    def __init__(self):
        self.client = MongoClient()
        self.termDb = self.client.terms

    def addTerm(self, userName, term):
        term_id = self.termDb[userName].insert_one(term.termJson).inserted_id
        return term_id

    def getAllTerms(self, userName):
        return self.termDb[userName]

class User:
    name = ""
    token = ""
