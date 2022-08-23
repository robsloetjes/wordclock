Software setup
=================
The program for the ESP8266 runs on micropython. See next chapter for more information how to program the python files (https://github.com/robsloetjes/wordclock) to the microcontroller.

On power up, the ESP8266 loops through main.py, which contains the main program. 

The modules you need to run the wordclock work as follows:

* main.py - Program starts with initiating the different parts/modules. When started an infinite loop is run through in which the program checks if a button is pressed (to change the time). If not it updates the time. When the time (in hours and minutes) is unchanged, nothing happens.
* display.py - Module that takes care of translating the current time into ranges of leds that need to light up (currently Dutch matrix layout only). It also interacts with the led strip using module ledstrip.py. 
* ledstrip.py - Makes shure that the leds will light up, also in the right color and brightness. Uses values from config.py and illuminance values from the TSL2561 sensor using tsl2561.py
* tools.py - Contains several modules to get and set the time and led color.
* config.py - Contains variables which mostly can be altered to change some functionalities.
* tsl2561.py - Driver for the TSL2561 luminosity sensor.
* DS3231.py - Diver for the RTC which tracks the time more precise than an ESP8266 can.

Writing program to ESP8266 & debug
----------------------------------
The program for the ESP8266 runs on micropython. See https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html for more information and the firmware. The firmware can be flashed by the ESPtool (https://github.com/espressif/esptool/), but I use a program called uPyCraft (https://randomnerdtutorials.com/install-upycraft-ide-windows-pc-instructions/) to burn the firmware and write the program to the microcontroller. Use the option 'Burn firmware' to write the Micropython firmware to the ESP8266. The computer needs to be connected by USB to the ESP8266. When the firmware is burned, create a serial connection through the COM port (e.g. using uPyCraft). 

Copy the python files to the workSpace folder or create new files and copy the content. Each file needs to be written separately to the ESP8266 (Tools -> Download).

When downloading is complete, push the reset button on the ESP board. While the serial connection is live, you can read the print outs of the program, which makes debugging possible. It is therefore recommended to test the program with all components connected to the microcontroller before glueing it all into the frame. 
