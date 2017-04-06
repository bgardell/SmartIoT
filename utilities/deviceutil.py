from pymongo import MongoClient

class DeviceHandler:
    def __init__(self):
        self.client = MongoClient()
        self.deviceDb = self.client.deviceDb

    # Simply add data to the database to be queried later.
    def addData(self, deviceName, deviceData):
        print "adding " + str(deviceData) + " to " + deviceName
        self.deviceDb[deviceName].insert(deviceData)
        return {"Result" : "Success"}

    def clearDeviceData(self, deviceName):
        self.deviceDb[deviceName].remove({})
        return {"Result" : "Success"}


    # This method maps data to predicates based on data mapping definition typically
    # defined in a query definition. For more information visit the documentation
    def mapCurrentDataToPredicates(self, deviceMappingDefinition):
        predicates = []
        for device in deviceMappingDefinition:
            deviceName = device["name"]
            dataMappings = device["dataMappings"]
            deviceDataCollection = self.deviceDb[deviceName]
            for mapping in dataMappings:
                predicateName = mapping["predicateName"]
                mappingVariables = mapping["mappingVariables"]
                mappedData = {}
                collectionCursor = deviceDataCollection.find({})
                #Iterate through all data records in a data specific collection
                for dataRecord in collectionCursor:
                    for variable in mappingVariables:
                        #Lookup in the definition which data key gives us our variable term atom.
                        dataRecordKey = mapping["recordData"][variable]
                        dataRecordValue = dataRecord[dataRecordKey]
                        #Convert BSON float data to int if needed
                        if type(dataRecordValue) == float:
                            dataRecordValue = int(dataRecordValue)
                        mappedData.update({ variable : dataRecordValue })
                    #Generate Predicate based on variable data mapping
                    predicate = {"name" : predicateName}
                    for variable in mappingVariables:
                        predicate.update({variable : mappedData[variable]})
                    predicates.append(self._convertPredicateToString(predicate, mappingVariables))
                    mappedData = {}
        return predicates


    def _convertPredicateToString(self, predicate, variableOrder):
        predicateString = predicate["name"] + "("
        for variable in variableOrder:
            predicateString += str(predicate[variable]) + ","

        predicateString = predicateString[:-1] +")"

        return predicateString
