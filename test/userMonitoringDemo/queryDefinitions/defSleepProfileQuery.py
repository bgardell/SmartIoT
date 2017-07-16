import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/sleepProfileQuery")
print r.text

mainLogic = """
inadequateSleep.
"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "predicates" : []
}

devices = [
]

knowledgeDependencies = {"externalServices": [],
                         "queries": []
                        }

queryDefinition = {}

queryDefinition["queryName"] = "sleepProfileQuery"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["knowledgeDependencies"] = knowledgeDependencies
queryDefinition["queryDescription"] = "Retrieve a user's sleep profile knowledge"

print queryDefinition
r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
