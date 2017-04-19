event("lieDown") :- legsOnFloor, headOnFloor.

triggerQuery("userStatusQuery") :- event("lieDown").