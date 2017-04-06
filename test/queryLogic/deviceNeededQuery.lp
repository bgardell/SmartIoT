canTurnOff(Device) :- notNeeded(Device).

notNeeded("AirConditioner") :- sunSetting, userNotHome.

sunSetting :- currentTime(Time), Time > 1080.
userLeftHome :- userHome(Time), currentTime(Time2), Time2-Time > 30.

temperatureDecreasing :- temperature(Temp, Time), temperature(Temp2, Time2), Time > Time2, Temp < Temp2.
lightsOff :- power("Lights", 0).
userHome(Time) :- movement(Time).
