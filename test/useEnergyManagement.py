import requests
import base64


r = requests.post("http://localhost:8080/useSkill/CircuitSkill", json=skillInput)

print r.text
