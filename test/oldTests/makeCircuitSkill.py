import requests
import base64

mainLogic = """
{ edge(P1, P2, Weight) : distance(P1, P2, Weight) }.

distance("Phoenix", "San Diego", 50).
distance("San Diego", "Seattle", 250).
distance("Seattle", "Phoenix", 300).

:- 2{edge(P1,Outbound,_) : place(Outbound)}, place(P1).
:- 2{edge(Inbound,P1,_) : place(Inbound)}, place(P1).

hasPath(P1,P2) :- edge(P1,P2,_).
hasPath(P1,P2) :- hasPath(P1,P3), hasPath(P3,P2).

:- not hasPath(P1,P2), place(P1), place(P2).

#minimize { X : edge(_,_,X) }.

#show edge/3."""

skillInput =  { "predicates" : [
    { "place": {
        "name": "place",
        "arity": 1,
        "variableNames" : ["PlaceName"]
    }}
]
}

skillOutput =   { "predicates" : [
{"edge": {
        "name": "edge",
        "arity": 3,
        "variableNames" : ["PlaceNameA", "PlaceNameB", "Weight"]
}}
                                 ]
}


commonKnowledge = { "predicates" : [
{
"predicateName" : "distance",
"arity": 3,
"input" : ["StartPlace", "EndPlace"],
"output" : ["Distance"],
"Parameterized": True,
"parameterizedGeneratorService": "http://googleapi/getDistances/StartPlace/EndPlace"
} ]
}



skillDefinition = {}

skillDefinition["skillName"] = "CircuitSkill"
skillDefinition["mainLogic"] = mainLogic
skillDefinition["inputDefinition"] = skillInput
skillDefinition["outputDefinition"] = skillOutput
skillDefinition["commonKnowledge"] = commonKnowledge
skillDefinition["skillDescription"] = "Generate a Hamiltonian Circuit"
print skillDefinition

r = requests.post("http://localhost:8080/userName/addSkill", json=skillDefinition)

print r.text
