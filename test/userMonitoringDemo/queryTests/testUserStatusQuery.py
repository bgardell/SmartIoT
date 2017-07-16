import json
import requests

medicalDeviceData = [{ "missedMedication" : "seizureMedication" }]

smartWatchData = [
        { "heartRate" : 80, "time": 1 },
        { "heartRate" : 85, "time": 2 },
        { "heartRate" : 90, "time": 3 },
        { "heartRate" : 100, "time": 4 },
        { "heartRate" : 105, "time": 5 },
        { "heartRate" : 110, "time": 6 }
]

r = requests.post("http://localhost:8080/addDeviceData/medicationAdherence", json=medicalDeviceData)

print r.text 
for dataRecord in smartWatchData:
    r = requests.post("http://localhost:8080/addDeviceData/smartWatch", json=dataRecord)
print r.text

r = requests.get("http://localhost:8080/useQueryWithDatabase/userStatusQuery")
print r.text

requests.get("http://localhost:8080/clearDeviceData/smartWatch")
requests.get("http://localhost:8080/clearDeviceData/medicationAdherence")
