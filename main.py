from HTTPHandler import HTTPService
from MQTTHandler import MQTTService

import cherrypy

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'tools.staticdir.on': True,
                'tools.staticdir.dir':
                '/home/ubuntu/aspWeb/schedulerHTML'
                               })

cherrypy.quickstart(HTTPService())
MQTTService()