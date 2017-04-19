from database.devicedb import DeviceDatabase
from queries.query import QueryHandler

class EventListener:

    def __init__(self):
        self.deviceDatabase = DeviceDatabase()
        self.queryHandler = QueryHandler()
