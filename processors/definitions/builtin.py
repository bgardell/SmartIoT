class DefinitionsMapping:

    definitionsMapping = {
        "predicates":
            {
                "queryName": {
                    "arity": 1,
                    "variableNames" : ["QueryName"]
                },
                "databaseDependency": {
                    "arity": 2,
                    "variableNames" : ["CollectionName", "MappingName"]
                },
                "queryDependency": {
                    "arity": 1,
                    "variableNames" : ["QueryName"]
                },
                "networkDependency": {
                    "arity" : 2,
                    "variableNames" : ["NetworkLocation", ""]
                }
            }
    }