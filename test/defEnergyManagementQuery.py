import requests
import base64

mainLogic = """
canTurnOff("AirConditioner") :- userNotHome, deviceOn("AirConditioner"), decreasingTemp.
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
            "mappingName" : "deviceOn",
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
print queryDefinition

r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print r.text
