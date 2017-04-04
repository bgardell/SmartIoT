from deviceutil import DeviceHandler

dm = DeviceHandler()
simpleDef = [
            {
                        "name": "WeatherSensor",
                                "dataMappings": [ {
                                                "predicateName" : "temperature",
                                                            "mappingVariables" : ["Degrees", "Time"],
                                                                        "recordData":
                                                                                    {
                                                                                                        "Degrees" : "temperatureRecorded",
                                                                                                                        "Time" : "timeLogged"
                                                                                                                                    }
                                                                                            }]
                                    }

            ]
dm.mapCurrentDataToPredicates(simpleDef)
