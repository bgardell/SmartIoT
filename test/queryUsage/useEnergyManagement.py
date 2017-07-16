import requests

# Current Devices Used Posts To Hub In Regular Intervals
print "Simulating Devices In Use Information"
currentDevices = {
        "deviceName" : "AirConditioner"
}
r = requests.post("http://localhost:8080/addDeviceData/DevicesUsed", json=currentDevices)

print r.text

# Post 3D Sensor Logging to service
print "Simulating Object-Sensing device"
movementSensorData = [{
            "registeredObject" : "John",
            "dayMinute" : 360
            },
            {
            "registeredObject" : "John",
            "dayMinute" : 390
            }
]

for dataRecord in movementSensorData:
    r = requests.post("http://localhost:8080/addDeviceData/3DSensor", json=dataRecord)

print r.text

print "Simulating Outdoor Thermometer Sensor device"
weatherData = [ 
  {"temperatureRecorded" : 78, "timeLogged": 1100 },
  {"temperatureRecorded" : 76, "timeLogged": 1115 },
  {"temperatureRecorded" : 74, "timeLogged": 1125 },
  {"temperatureRecorded" : 70, "timeLogged": 1135 },
  {"temperatureRecorded" : 68, "timeLogged": 1145 }
]

for dataRecord in weatherData:
    r = requests.post("http://localhost:8080/addDeviceData/WeatherSensor", json=dataRecord)
print r.text

print "Querying service to determine if the air conditioner can be turned off to save energy"
r = requests.get("http://localhost:8080/useQueryWithDatabase/deviceNeededQuery")

print r.text

print "Deleting simulated test data"
# Clear Data for fresh use
requests.get("http://localhost:8080/clearDeviceData/DevicesUsed")
requests.get("http://localhost:8080/clearDeviceData/3DSensor")
requests.get("http://localhost:8080/clearDeviceData/WeatherSensor")
