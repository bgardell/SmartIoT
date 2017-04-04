import requests
import json

mainLogic = """
canTurnOff("AirConditioner") :- userNotHome, deviceOn("AirConditioner"), decreasingTemp.
decreasingTemp :- temperature(Degrees, Time), temperature(Degrees1, Time1), Time > Time1, Degrees < Degrees1.
userNotHome :- movement("John", Time), movement("John", Time1), Time > Time1, currentTime(CTime), CTime-Time > 90.

currentTime(1180).
"""

queryInput =  { "predicates" : [] }

queryOutput =   { "predicates" : [
{"canTurnOff": {
        "name": "canTurnOff",
        "arity": 1,
        "variableNames" : ["DeviceName"]
}}
                                 ]
}


devices = [{
        "name": "3DSensor",
        "dataMappings":[{
            "predicateName" : "movement",
            "mappingVariables": ["ObjectName", "Time"],
            "recordData":
            {
                "ObjectName" : "registeredObject",
                "Time" : "dayMinute"
            }
        }
        ]
    },
    {
        "name": "WeatherSensor",
        "dataMappings": [ {
            "predicateName" : "temperature",
            "mappingVariables" : ["Degrees", "Time"],
            "recordData":
            {
                "Degrees" : "temperatureRecorded",
                "Time" : "timeLogged"
            }
        }]
    },
    {
        "name" : "DevicesUsed",
        "dataMappings": [ {
            "predicateName" : "deviceOn",
            "mappingVariables" : ["DeviceName"],
            "database":
            {
                "DeviceName" : "deviceName"
            }
        }]
    }
]

queryDefinition = {}

queryDefinition["queryName"] = "deviceNeededQuery"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["queryDescription"] = "Determine if a device can be switched off"
print json.dumps(queryDefinition, indent=4, sort_keys=False)

r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print r.text
