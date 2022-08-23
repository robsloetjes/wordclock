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

Normal operation
----------------

When the power adapter is plugged in, the ESP8266 will boot in about 5 seconds. When it is the first power up, the clock shows the time since putting the battery in the RTC. To change the time, hold the OK button until "HET IS" flashes 3 times. The clock wil enter time setting mode, which is a 4 step proces elaborated in tools.py (function set_time()). 

1. Set the time in hours using de back and forward button. When the correct hour is selected, push the OK button, the time in hours will flash.
2. Set the time in 5 minutes using the back and forward button. When the correct time (rounded down to 5 minutes) is selected, push the OK button, the time will flash.
3. Set the exact time for the minute leds using the back and forward button. When the correct time is selected, push the OK button, "HET IS" and the minute leds will flash.
4. You now can change the yellow value of the clock using the back and forward button. At default the led color in RGB is 255,255,50 but you can change the 50 to the desired type of white to yellow. Push the OK button when ready. The clock wil turn off for 2 seconds and then show the time in the new color. 

When you pull the plug of the power supply, the RTC will keep track of the time using the CR2032 battery. Once power is restored, the correct time should show up.

To compensate for daylight saving time, push the back or forward button once to change the current time by one hour.
