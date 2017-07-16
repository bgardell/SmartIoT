import requests
import json

r = requests.get("http://localhost:8080/deleteQuery/whatGroceries")
print r.text

mainLogic = """

needItem(GroceryItem) :- not haveItem(GroceryItem), userWants(GroceryItem).

userWants(GroceryItem) :- plannedMeal(Meal), mealIngredient(Meal,GroceryItem), not have(GroceryItem).

mealIngredient("Bread", "Yeast").
plannedMeal("Bread").

#show needItem/1.
"""

queryInput =  { "predicates" : [] }

queryOutput =   {
        "predicates" :
        {
            "needItem": {
                    "arity": 1,
                    "variableNames" : ["GroceryItem"]
            }
        }
}


# { "fridgeHas" : "Milk" }.
devices2 = [
    {
        "name" : "Fridge",
        "dataMappings": [{
            "predicateName" : "haveItem",
            "mappingVariables" : ["GroceryItem"],
            "recordData":
            {
                "GroceryItem" : "fridgeHas"
            }
        }]
    }
]

knowledgeDependencies = {"externalServices": [],
                         "queries": []
                        }


queryDefinition = {}

queryDefinition["queryName"] = "whatGroceries"
queryDefinition["mainLogic"] = mainLogic
queryDefinition["inputDefinition"] = queryInput
queryDefinition["outputDefinition"] = queryOutput
queryDefinition["devicesUsed"] = devices2
queryDefinition["knowledgeDependencies"] = knowledgeDependencies
queryDefinition["queryDescription"] = "Return a list of groceries needed"

r = requests.post("http://localhost:8080/addQuery", json=queryDefinition)

print r.text
