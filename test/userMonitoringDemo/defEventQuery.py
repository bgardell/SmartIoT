import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/objectSensorEventDetector")
print r.text

mainLogic = """
fellDown(Time) :- lyingDown(Time), upright(Time2), Time2-Time < 5.
event("fellDown") :- fellDown(_).
triggerQuery("userStatusQuery") :- event("fellDown").

lyingDown(Time) :- legsOnFloor(Time), upperBodyOnFloor(Time).
upright(Time) :- ypos("rightKnee", YCoord, Time), ypos("leftKnee", YCoord2, Time), YCoord > 3, YCoord2 > 3.
upright(Time) :- ypos("head", YCoord, Time), YCoord > 3.

legsOnFloor(Time) :- ypos("rightKnee", YCoord, Time), ypos("leftKnee", YCoord2, Time), YCoord < 3, YCoord2 < 3.
upperBodyOnFloor(Time) :- ypos("head", YCoord, Time), YCoord < 3.

#show fellDown/1.
#show lyingDown/1.
#show upperBodyOnFloor/1.
#show legsOnFloor/1.
#show event/1.
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
        "name": "ObjectSensor",
        "dataMappings":[{
            "predicateName" : "ypos",
            "mappingVariables": ["JointName", "JointPos", "Time"],
            "recordData":
            {
                "JointName" : "jointName",
                "JointPos" : "ypos",
                "Time" : "time"
            }
        }
        ]
    }
]

knowledgeDependencies = {"externalServices": [],
                         "queries": []
                        }

queryDefinition = {}

queryDefinition["queryName"] = "objectSensorEventDetector"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["knowledgeDependencies"] = knowledgeDependencies
queryDefinition["queryDescription"] = "The query for event detecting for the object sensor"

print queryDefinition
r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
