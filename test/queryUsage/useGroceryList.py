import requests
import base64

fridgeData = [
        {"fridgeHas" : "\"Milk\""},
        {"fridgeHas" : "\"Eggs\""},
        {"fridgeHas" : "\"Wine\""},
        {"fridgeHas" : "\"Flour\""},
        {"fridgeHas" : "\"Butter\""}
]

for dataRecord in fridgeData:
    r = requests.post("http://localhost:8080/addDeviceData/Fridge", json=dataRecord)

r = requests.get("http://localhost:8080/useQueryWithDatabase/whatGroceries")

print r.text

requests.get("http://localhost:8080/clearDeviceData/Fridge")
