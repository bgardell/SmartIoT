import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/objectSensorEventDetector")
print r.text

mainLogic = """
fellDown :- lyingDown(Time), upright(Time2), Time2-Time < 5.
triggerQuery("userStatusQuery") :- fellDown.

lyingDown(Time) :- legsOnFloor(Time), upperBodyOnFloor(Time).
upright(Time) :- ypos("rightKnee", YCoord, Time), ypos("leftKnee", YCoord2, Time), YCoord > 3, YCoord2 > 3.
upright(Time) :- ypos("head", YCoord, Time), YCoord > 3.

legsOnFloor(Time) :- ypos("rightKnee", YCoord, Time), ypos("leftKnee", YCoord2, Time), YCoord < 3, YCoord2 < 3.
upperBodyOnFloor(Time) :- ypos("head", YCoord, Time), YCoord < 3.

"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "predicates" :
        {
            "triggerQuery": {
                    "arity": 1,
                    "variableNames" : ["QueryName"]
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

knowledgeDependencies = {"externalServices": [
                        {   "url" : "http://localhost:8088/getObjectSensorData", 
                            "name": "ObjectSensor",
                            "data": 
                            {
                              "type" : "list", 
                              "structureDepth": ["data"]
                            },
                            "dataMapping":
                            {
                                "predicateName" : "ypos",
                                "mappingVariables": ["JointName", "JointPos", "Time"],
                                "recordData":
                                {
                                    "JointName" : "jointName",
                                    "JointPos" : "ypos",
                                    "Time" : "time"
                                }
                            }
                        }],
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
