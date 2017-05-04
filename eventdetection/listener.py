from threading import Timer
from netquery.query import QueryHandler

class EventListener():
    '''
    This class defines an event listener object which sets to run periodically a query associated with the event.
    '''

    def __init__(self,eventListenerName, period):
        self.queryHandler = QueryHandler()
        self.eventListenerName = eventListenerName
        self.period = period
        self.executeQuery()

    def executeQuery(self):
        triggers = self.queryHandler.solveQueryOutputJson(self.eventListenerName)
        print triggers
        for trigger in triggers["predicatesJSON"]:
            queryOutput = self.queryHandler.solveQueryOutputJson(trigger["QueryName"])
            print queryOutput
        Timer(self.period, self.executeQuery).start()