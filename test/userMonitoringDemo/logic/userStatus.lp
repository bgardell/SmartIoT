5 heartAttack :- missedMedication("heartMedicine"), fellDown.
5 heartAttack :- highHeartRate, fellDown.
5 heartAttack :- heartProblems, fellDown.

2 fellAsleep :- inadequateSleep, fellDown.
2 fellAsleep :- consumedAlcohol, fellDown.
-1 fellAsleep :- not inadequateSleep, fellDown.

6 seizure :- missedMedication("seizureMedication"), fellDown.
6 seizure :- epilepsy, fellDown.
3 seizure :- rapidMovements, fellDown.

generalFaint :- fellDown, not fellAsleep, not heartAttack, not seizure.

1{fellAsleep;heartAttack;seizure;generalFaint}1.
