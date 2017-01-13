from pymongo import MongoClient

class UserHandler:
    def __init__(self):
        self.client = MongoClient()
        self.termDb = client.terms

    def addTerm(self, userName, term):
        term_id = self.termDb[userName].insert_one(term).inserted_id
        return term_id

class User:
    name = ""
    token = ""
