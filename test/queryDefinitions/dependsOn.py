import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/testQuery")
print r.text

mainLogic = """
testPredicate(1).
"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "predicates" :
        {
            "testPredicate": {
                    "arity": 1,
                    "variableNames" : ["Number"]
            }
        }
}


devices = []

dependsOn = []

queryDefinition = {}

queryDefinition["queryName"] = "testQuery"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["dependsOn"] = dependsOn
queryDefinition["queryDescription"] = "Test Query For Dependency System"

r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
