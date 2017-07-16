import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/medicalProfileQuery")
print r.text

mainLogic = """
hasEpilepsy.
hasGlaucoma.
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

queryDefinition["queryName"] = "medicalProfileQuery"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["knowledgeDependencies"] = knowledgeDependencies
queryDefinition["queryDescription"] = "Retrieve a user's medical profile knowledge"

print queryDefinition
r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
