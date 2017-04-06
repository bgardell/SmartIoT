import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/deviceNeededQuery")
print r.text

mainLogic = """
canTurnOff("AirConditioner") :- userNotHome, deviceOn("AirConditioner"), decreasingTemp.

decreasingTemp :- temperature(Degrees, Time), temperature(Degrees1, Time1), Time > Time1, Degrees < Degrees1.
userNotHome :- movement("John", Time), movement("John", Time1), Time > Time1, currentTime(CTime), CTime-Time > 90.

currentTime(1180).
"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "predicates" :
        {
            "canTurnOff": {
                    "arity": 1,
                    "variableNames" : ["DeviceName"]
            }
        }
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
            "recordData":
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

r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
