import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/userStatusQuery")
print r.text

mainLogic = """
unsat(0,"5.000000") :- missedMedication("heartMedicine"), fellDown,not event("heartAttack") .
event("heartAttack") :- missedMedication("heartMedicine"), fellDown, not unsat(0,"5.000000").
:~unsat(0,"5.000000"). [5@0,0]
unsat(1,"5.000000") :- highHeartRate, fellDown,not event("heartAttack") .
event("heartAttack") :- highHeartRate, fellDown, not unsat(1,"5.000000").
:~unsat(1,"5.000000"). [5@0,1]
unsat(2,"5.000000") :- heartProblems, fellDown,not event("heartAttack") .
event("heartAttack") :- heartProblems, fellDown, not unsat(2,"5.000000").
:~unsat(2,"5.000000"). [5@0,2]
unsat(3,"2.000000") :- inadequateSleep, fellDown,not event("fellAsleep") .
event("fellAsleep") :- inadequateSleep, fellDown, not unsat(3,"2.000000").
:~unsat(3,"2.000000"). [2@0,3]
unsat(4,"2.000000") :- consumedAlcohol, fellDown,not event("fellAsleep") .
event("fellAsleep") :- consumedAlcohol, fellDown, not unsat(4,"2.000000").
:~unsat(4,"2.000000"). [2@0,4]
unsat(5,"6.000000") :- missedMedication("seizureMedication"), fellDown,not event("seizure") .
event("seizure") :- missedMedication("seizureMedication"), fellDown, not unsat(5,"6.000000").
:~unsat(5,"6.000000"). [6@0,5]
unsat(6,"6.000000") :- hasEpilepsy, fellDown,not event("seizure") .
event("seizure") :- hasEpilepsy, fellDown, not unsat(6,"6.000000").
:~unsat(6,"6.000000"). [6@0,6]
unsat(7,"3.000000") :- rapidMovements, fellDown,not event("seizure") .
event("seizure") :- rapidMovements, fellDown, not unsat(7,"3.000000").
:~unsat(7,"3.000000"). [3@0,7]
unsat(8,"2.000000") :- fellDown,not event("generalFaint") .
event("generalFaint") :- fellDown, not unsat(8,"2.000000").
:~unsat(8,"2.000000"). [2@0,8]
criticalEvent :- event("seizure");event("heartAttack");event("generalFaint").
nonCriticalEvent :- event("fellAsleep").
highHeartRate.
missedMedication("seizureMedication").
hasEpilepsy.
hasGlaucoma.
fellDown.
1{criticalEvent;nonCriticalEvent}1.
"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "locations" : ["http://localhost:8088/alertDevice"],
        "predicates" :
        {
            "event": {
                    "arity": 1,
                    "variableNames" : ["EventName"]
            }
        }
}

devices = [
]

knowledgeDependencies = {"externalServices": [],
                         "queries": ["userHealthQuery"]
                        }

queryDefinition = {}

queryDefinition["queryName"] = "userStatusQuery"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices
queryDefinition["knowledgeDependencies"] = knowledgeDependencies
queryDefinition["queryDescription"] = "Retrieve a user's current status"

print queryDefinition
r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print json.dumps(r.text, indent=4)
