Overview
========

As mentioned in the introduction, this wordclock is based on the Bernd Krolla implementation of the original QLOCKTWO. Krolla's wordclock runs on a Raspberry Pi. I was searching for the most affordable implementation of a wordclock, therefore I ended up with the bare minimum of electrical components. The ESP8266 microcontroller is mostly shipped with firmware to run Arduino language. However, it also runs a port of Micropython which works great for this type of project. 

To show the time in words, a led strip is placed behind a laser cut matrix of characters. The hardware can be divided in woodwork and electrical components. After some iterations I ended up with a wooden frame made out of laser cut slats that make sure if a led lights up, adjacent characters will not be illuminated. 

The electrical component consist of a ESP8266 NodeMCU microcontroller, DS3231 Real Time Clock to remember the time (the ESP8266's internal clock is not constant enough), TSL2561 luminocity sensor to adjust the brightness of the clock to the ambient light. Three small push buttons provide the function to set the time and adjust the color of the leds. A 5v DC power supply of 2A should be sufficient but I use a 3A version to be sure. The leds used are a WS2812B adressable led strip, in which each led can be controlled separately. The components are wired together with electrical wire and led strip connector (to save a lot of soldering).

Shopping list
-------------
Electrical components:
- ESP8266 (NodeMCU) microcontroller
- DS3231 Real Time Clock (RTC)
- TSL2561 luminocity sensor
- 3A 5V DC power supply
- Ledstrip with 114 WS2812B leds (30 leds/m)
- 13 led strip connectors
- 1 female DC plug
- 3 small push buttons
- Electrical wire !!! mm2/ !!! AWG

Woodwork:
- Laser cut front plate of 450x450mm
- Interior matrix made out of laser cut slats
- Slats for the border
- 4 small blocks to fixate screw on back plate
- Back plate (+- 440x440mm)
