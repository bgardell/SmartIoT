needItem(GroceryItem) :- not haveItem(GroceryItem), userWants(GroceryItem).

userWants(GroceryItem) :- plannedMeal(Meal), mealIngredient(Meal,GroceryItem), not have(GroceryItem).

mealIngredient("Bread", "Yeast").
plannedMeal("Bread").

#show needItem/1.
