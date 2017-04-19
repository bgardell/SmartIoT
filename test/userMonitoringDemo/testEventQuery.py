import json
import requests

objectSensorData = [

{"jointName" : "rightKnee", "ypos" : 3, "time" : 1},
{"jointName" : "leftKnee" , "ypos" : 3, "time" : 1},
{"jointName" : "rightFoot" , "ypos" : 1, "time" : 1},
{"jointName" : "leftFoot" , "ypos" : 1, "time" : 1},
{"jointName" : "rightHand" , "ypos" : 9, "time" : 1},
{"jointName" : "leftHand" , "ypos" : 9, "time" : 1},
{"jointName" : "head",  "ypos" : 10, "time" : 1},

{"jointName" : "rightKnee" , "ypos" : 3, "time" : 2},
{"jointName" : "leftKnee" , "ypos" : 3, "time" : 2},
{"jointName" : "rightFoot" , "ypos" : 1, "time" : 2},
{"jointName" : "leftFoot" , "ypos" : 1, "time" : 2},
{"jointName" : "rightHand", "ypos" : 9, "time" : 2},
{"jointName" : "leftHand", "ypos" : 9, "time" : 2},
{"jointName" : "head", "ypos" : 10, "time" : 2},

{"jointName" : "rightKnee", "ypos" : 3, "time" : 3},
{"jointName" : "leftKnee", "ypos" : 3, "time" : 3},
{"jointName" : "rightFoot", "ypos" : 1, "time" : 3},
{"jointName" : "leftFoot", "ypos" : 1, "time" : 3},
{"jointName" : "rightHand", "ypos" : 6, "time" : 3},
{"jointName" : "leftHand", "ypos" : 6, "time" : 3},
{"jointName" : "head", "ypos" : 10, "time" : 3},

{"jointName" : "rightKnee", "ypos" : 0, "time" : 4},
{"jointName" : "leftKnee", "ypos" : 0, "time" : 4},
{"jointName" : "rightFoot", "ypos" : 0, "time" : 4},
{"jointName" : "leftFoot", "ypos" : 0, "time" : 4},
{"jointName" : "rightHand", "ypos" : 4, "time" : 4},
{"jointName" : "leftHand", "ypos" : 4, "time" : 4},
{"jointName" : "head", "ypos" : 8, "time" : 4},

{"jointName" : "rightKnee", "ypos" : 0, "time" : 5},
{"jointName" : "leftKnee", "ypos" : 0, "time" : 5},
{"jointName" : "rightFoot", "ypos" : 0, "time" : 5},
{"jointName" : "leftFoot", "ypos" : 0, "time" : 5},
{"jointName" : "rightHand", "ypos" : 4, "time" : 5},
{"jointName" : "leftHand", "ypos" : 4, "time" : 5},
{"jointName" : "head", "ypos" : 8, "time" : 5},

{"jointName" : "rightKnee", "ypos" : 0, "time" : 6},
{"jointName" : "leftKnee", "ypos" : 0, "time" : 6},
{"jointName" : "rightFoot", "ypos" : 0, "time" : 6},
{"jointName" : "leftFoot", "ypos" : 0, "time" : 6},
{"jointName" : "rightHand", "ypos" : 2, "time" : 6},
{"jointName" : "leftHand", "ypos" : 0, "time" : 6},
{"jointName" : "head",  "ypos" : 2, "time" : 6}]


for dataRecord in objectSensorData:
    r = requests.post("http://localhost:8080/addDeviceData/ObjectSensor", json=dataRecord)

r = requests.get("http://localhost:8080/useQueryWithDatabase/objectSensorEventDetector")

print r.text

requests.get("http://localhost:8080/clearDeviceData/ObjectSensor")

