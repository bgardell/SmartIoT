import requests

class HTTPOperations():

    def retrieveNetworkDependency(self, networkDependency):
        try:
            r = requests.get(networkDependency["url"])
            retrievedJson = r.json()
            return retrievedJson
        except Exception, e:
            print e
            print "Failed to reach network dependency"
            return {}

    def postKnowledgeOutput(self, knowledge, outputLocation):
        try:
            r = requests.post(outputLocation, json=knowledge)
            return {"Result" : "Success"}
        except Exception, e:
            print e
            print "Failed to send knowledge to output location"
            return {"Result" : "Success"}