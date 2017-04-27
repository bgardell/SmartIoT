import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/userHealthQuery")
print r.text

mainLogic = """
highHeartRate :- heartRate(Rate,_), Rate > 100, not userExercising.
lowBloodSugar :- bloodSugar(Level), Level < 70.
highBodyTemp :- bodyTemp(FDegrees), FDegrees > 99.
inadequateSleep :- timeGoneToBed(Time), timeWokeUp(Time2), Time2 - Time < 7.
"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "predicates" :
        {
            "event": {
                    "arity": 1,
                    "variableNames" : ["EventName"]
            }
        }
}

devices = [
    {
        "name": "smartWatch",
        "dataMappings":[{
            "predicateName" : "heartRate",
            "mappingVariables": ["Rate","Time"],
            "recordData":
            {
                "Rate" : "heartRate",
                "Time" : "time"
            }
        }
        ]
    },
    {
        "name": "medicationAdherence",
        "dataMappings": [{
            "predicateName": "missedMedication",
            "mappingVariables": ["MedicationName"],
            "recordData":
                {
                    "MedicationName": "missedMedication"
                }
        }
        ]
    }
]

knowledgeDependencies = {"externalServices": [],
                         "queries": ["medicalProfileQuery", "sleepProfileQuery"]
                        }

queryDefinition = {}

queryDefinition["queryName"] = "userHealthQuery"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["knowledgeDependencies"] = knowledgeDependencies
queryDefinition["queryDescription"] = "Retrieve a user's current health status"

print queryDefinition
r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
