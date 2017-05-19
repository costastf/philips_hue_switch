# Philips hue switch
Micropython code that toggles a philips hue lamp using wemos d1 mini or esp8266 01s

This project is to be used with a hardware switch making that existing wall
switch not cutting the current off but using the api to toggle the lamp's
state.

Some electrical assembly required :)

# WARNING
Only mess with high current if you really really know what you are doing. If
not certified to do so please refrain from it. It can definitely kill you,
which is not a desired outcome for any hobby project.


# Problem statement
Philips hue lamps are amazing, providing a wonderful solution for home
lighting. The only problem is that the way they are operated leaves some
things to be desired.

When the traditional switch is off the lamps of course
can not be operated through the app, but only using the app is not realistic
for all lights and all conditions. Also people coming over do not have access
to the app and many people in a house create confusion.
 
The current solution is to purchase a separate wireless switch from
Philips to use with the lamps but that can get really expensive really quick
if you want one for each lamp and of course that does not solve the
problem of the traditional switches that either will disrupt the usage of
the lights or have to be taken out. Not fun.

# Solution
All lights can be operated through the api provided by the hue bridge.
Instead of using the switch to cut the power to the lamp leaving it useless,
we rewire the lamp to be constantly powered and the switch to an esp8266
board to toggle the lamp through the api. That way our switch works as before
for all, toggling the state of the lamp and the lamp continues to be
accessible through the app all the time. Sweet right?

so we want to go from this initial state:

![alt text](schematics/initial_state.png "Initial state schematic")

to this state (schematic depicting an esp01s):

![alt text](schematics/esp8266_01s_schem.png "esp01s 
schematic")

# Requirements
[Enable hue api access to your bridge](https://www.developers.meethue.com/documentation/getting-started)
