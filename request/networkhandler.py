import requests

class NetworkDependencyHandler():

    def resolveNetworkDependency(self, networkDependency):
        r = requests.get(networkDependency)
        return r.json()