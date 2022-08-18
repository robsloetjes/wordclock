Troubleshooting
===============

* Wordclock doesn't turn on
Probably there is something wrong in the power circuit. Check with a multimeter if the there are no short circuits and all parts get 5v DC supplied. When the power supplie is plugged in, the onboard led of the ESP8266 should flash once. When the power circuit is not the problem, a software issue could be present. You can connect the microcontroller to a computer and read out the serial output of the program (for example use uPyCraft). Be aware that you keep the power supply plugged in, since the ESP8266 cannot provide enough power when accidentally many leds light up. 

* The ledstrip only partially works
Or the data wire is interrupted (between the parts that work and don't) or a part of the led strip recieves no or not enough power.

* The clock shows strange colors
Probably a small shortage is present beween the 5v wand the data wires, or the led strip gets insufficient power at some point to pass through the information in the data wire.

* Some characters are more dim than others
Too much voltage drop is present. Check if you source the led strip with 5v DC at multiple points.

* Wrong characters light up
Does the wiring follow the diagram as provided in the hardware section?
