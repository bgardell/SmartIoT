import requests
import base64


skillInput =  { "predicates" : [
    { 
        "predicateName": "place",
        "PlaceName" : "Phoenix"
    },
    { 
        "predicateName": "place",
        "PlaceName" : "San Diego"
    },
    { 
        "predicateName": "place",
        "PlaceName" : "Seattle"
    }
]
}

r = requests.post("http://localhost:8080/useSkill/CircuitSkill", json=skillInput)

print r.text
