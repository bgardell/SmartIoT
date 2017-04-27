import json
import requests

requests.get("http://localhost:8080/clearDeviceData/ObjectSensor")

r = requests.get("http://localhost:8080/useQueryWithDatabase/objectSensorEventDetector")

print r.text
