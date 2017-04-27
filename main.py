from HTTPHandler import HTTPService
from MQTTHandler import MQTTService
from eventdetection.listener import EventListener
import cherrypy

def startHTTP():
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HTTPService())

def startMQTT():
    MQTTService()

def startEventListeners():
    el = EventListener("objectSensorEventDetector", 2)

startHTTP()