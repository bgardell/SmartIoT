import threading
from queries.query import QueryHandler

class EventListener():
    '''
    This class defines an event listener object which sets to run periodically a query associated with the event.

    '''
    def __init__(self,eventListenerName):
        self.queryHandler = QueryHandler()
        self.eventListenerName = eventListenerName
        self.run()

    def executeQuery(self):
        triggers = self.queryHandler.solveQueryOutputJson(self.eventListenerName)["predicatesJSON"]
        print triggers

    def run(self):
        threading.Timer(30, self.executeQuery).start()


