Hardware setup
==============

Woodwork
---------
The front of the wordclock shows a matrix of 11x10 characters and 4 dots for indicating the minutes. Behind the characters, regular printing paper takes care of diffusing the light from the leds. Due to the required level of detail, I ordered a laser cut front plate from plywood. The dimensions are 450x450 millimiters. I use a thickness of 2 millimiters to ensure that a wide viewing angle on the clock is possible. See a template in the downloads section.

At the back of the front plate, a raster of slats hold the led strips in place. For a prototype I sawed these slats by hand, but a laser cut is a lot more precise and easier (3mm MDF). See a template in the downloads section. The raster has a height of 18mm. In a prototype I used a height of 15mm, but when de leds are placed 15mm behind the front plate, the middle of a character is a bit more bright than the edges. Therefore I use 18mm thickness now. 

For the outside border I used slats plywood of 4mm thickness. The lengths are 450mm for the left and right side, 450-2x4=442mm for the bottom and 2 times 191mm for the top. In the middle a open space is present for the 3 buttons. The template for the interior matrix contains parts for holding the buttons which can be glued under this cutout. 

**Steps for creating the woodwork:**

1. Paint or varnish the front plate and border slats in a color or varnish of your choice.
2. Cover the backside of the front plate with paper. You can fixate it with regular tape. Picture !!!
3. Put together the matrix of slats for the interior and glue it to the back of the front plate. Picture !!!
4. Put together the pieces for the minute-leds. Glue them to the back of the front plate. Picture !!!
5. Solder all electrical components and mount them in the woodwork, see chapter electrical setup. The template for the buttons can be used to hold them in place and glue them to the front plate when alle electrical components are ready to mount.
6. Glue the 4 blocks to the front plate for screwing the back plate to the frame
7. Place the back plate. Make sure you have a cutout for the DC socket, 4 screwholes for screwing the back plate to the glued blocks and 1 hole for hanging the clock to a wall. Picture !!!

Electrical setup
---------
The fritzing scheme provides an overview how to solder the components. It is most easy to separate the power circuit, led strip connectors and wires for communication. 

**Power circuit:**
It is important to understand that the led strip has contunious circuits for +5v, ground an data transfer. A WS2812B led can draw up to 60mA, which can add up to quite some current. Due to the small wire gauge in the led strip the resistance will grow and cause voltage drop. The leds at the end of the strip will be dimmer than at the beginning. This can be prevented by sourcing power to the led strip at multiple points. 

The 5v power is sourced by the power supply through the female DC plug. After the plug the power wires split into a circuit to the bottom for sourcing the led strip at multiple points and to the top to provide power to the microcontroller and breakout boards. The +5v and ground for the led strip do not have to be continious, the data wire should be. 

The other circuit feeds both leds on the left side (seen from the back) and provide the microcontroller, RTC en luminocity sensor with 5v DC. Also the buttons need to be connected to ground on one side.

**Led strip connectors:**
I use 3 pin ledstrip connectors to easily connect led strips to each other without soldering. To connect the minute leds in the left and right corners, I cut the wires to extend them. Further, each connector wires together adjacent let strips. On the bottom, on 3 locations the 5v and groud wires are stripped to solder the power wires to avoid voltage drop. 

**Data circuit:**
From the microcontroller, several data wires run to the components. I recommend to solder all the wires (use an ESP8266 without GPIO header) to reduce required space and prevent errors due to wires slipping off. See image ...

1. D8 (GPIO 15) is the data in wire for the ledstrip, running to the data in wire at the led on the left bottom (seen from the back)
2. D1 (GPIO 5) is SCL, serial clock for the I2C interface, running to the RTC first and continues to the TSL2561 sensor. These breakout boards can also be connected to parallel to the I2C pins.
3. D2 (GPIO 4) is SDA, serial data for the I2C interface, runs alongside the SCL wire to the RTC and TSL2561.
4. D5 (GPIO 14) is the back botton, most right seen from the back. This pin is pulled up by the program and is pulled to ground when the button is pushed. 
5. D6 (GPIO 12) is the OK button, in the center of the three. Also pulled up by the program.
6. D7 (GPIO 13) is the left button, most left seen from the back. Also pulled up by the program.

It is wise to check for short circuits with a multimeter (+5v should not be in contact with ground). Also make sure that the data wire continues in the same zigzag pattern so that numbering of characters corresponds with the program. 

Mounting electrical components
------------------------
With all components soldered together you can place them in the woodwork. All electrical components can be mounted with a glue gun. The order I perfer:

1. Microcontroller with RTC and TSL2561. It is recommended to write the program to the microcontroller first and test before glueing it together. See page about software setup.
2. Power circuits from the chips to the power plug
3. Power circuit at the bottom of the clock for sourcing the led strips
4. Minute leds can be glued in the pieces. Cover them with duct tape to prevent leakage of light. 
5. The wiring can be glued to the front plate or matrix for better fixation
6. The leds strips, cut in strings of 10 leds, can be connected by led strip connectors and glued to the cut outs in the top and bottom slats. It could be wise to extend the strip with one length a time and test if leds do light up if you plug the power supply. 
7. When all led strips are mounted, cover the back with duct tape. This prevents leakage of light from one character to the other. 
8. Test if your clock works and mount the back plate. See step 6 and 7 in woodwork.

.. image:: https://github.com/robsloetjes/wordclock/blob/main/docs/Hardware%201.jpg?raw=true
:width: 600
:alt: Back of front plate covered with paper
