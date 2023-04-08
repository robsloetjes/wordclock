import config
import math
import neopixel
import tsl2561
import bh1750
from machine import I2C, Pin
from time import sleep

if config.luxsensor:
    i2c = I2C(sda = Pin(config.sda), scl= Pin(config.scl))
    try:
        if config.luxsensor_type == 'TSL2561':
            luxsensor = tsl2561.TSL2561(i2c)
            print('Luxsensor initiated')
    except:
        print('Error in lux sensor')
        
class led_strip:
    def __init__(self):
        self.total_pixels = config.matrix_width * config.matrix_height + 4  # Height * width + 4 minute leds
        self.ledstrip = neopixel.NeoPixel(Pin(config.ledstrip_pin), self.total_pixels)
        self.color = config.led_color[:]
        self.brightness_color = config.led_color[:]
        self.minute_led_numbers = config.minute_led_numbers
        self.default_brightness = int(config.default_brightness)
        self.brightness = self.default_brightness
        self.min_brightness = int(config.min_brightness)
        self.max_brightness = int(config.max_brightness)
    
    def renew_colors(self,color):
        self.color = [int(color[0]), int(color[1]), int(color[2])]
    
    def reset(self): # turn led strip off
        for i in range(0,self.total_pixels):
            self.ledstrip[i] = (0,0,0)
        self.ledstrip.write()
       
    def getlux(self):
        if config.luxsensor:
            try:
                if config.luxsensor_type == 'TSL2561':
                    lux = luxsensor.read()*2+10
                else:
                    lux = bh1750.sample(i2c)
            except:
                print('Fout in luxsensor 2')
            return lux
        else:
            return '"False"'
    
    def program_pixel(self, ledrange, ledminuterange, refresh_brightness = True): # light up leds according to the current time
        if refresh_brightness:
          if config.luxsensor:
              self.brightness = self.getlux();
              # print("Measured brightness "+ str(self.brightness));
          else:
              self.brightness = self.default_brightness

        # Brightness should remain between 0 and 1
        if self.brightness > self.max_brightness or self.brightness > 100:
            self.brightness = self.max_brightness
        elif self.brightness < self.min_brightness or self.brightness < 0:
            self.brightness = self.min_brightness
        
        # print("Results in "+ str(self.brightness));
        # Convert RGB to range between 0 and 255
        max_color_value = max(self.color[0],self.color[1],self.color[2]);
        self.brightness_color[0] = math.floor(self.color[0] / max_color_value * self.brightness/100 * 255)
        self.brightness_color[1] = math.floor(self.color[1] / max_color_value * self.brightness/100 * 255)
        self.brightness_color[2] = math.floor(self.color[2] / max_color_value * self.brightness/100 * 255)

        # Check for each led (not the minute leds) if it should be turned on or off
        for i in range(2,self.total_pixels-2):
            if i in ledrange:
                # Turn led on
                self.ledstrip[i] = tuple(self.brightness_color)
            else: 
                # Turn led off
                self.ledstrip[i] = (0,0,0)
        
        # Check for each minute leds too
        for i in self.minute_led_numbers:
            if i in ledminuterange: 
                self.ledstrip[i] = tuple(self.brightness_color)
            else: 
                self.ledstrip[i] = (0,0,0)
        
        self.ledstrip.write()
        

def loop_leds():
    # Use this function if you would like to test all leds
    ledstrip = neopixel.NeoPixel(Pin(14), self.total_pixels)
    for i in range(0,self.total_pixels):
        ledstrip[i] = (255,255,255)
        if i>0:
            ledstrip[i-1] = (0,0,0)
        ledstrip.write()
        sleep(0.05)
    for i in range(0,self.total_pixels):
        ledstrip[i] = (0,0,0)
    ledstrip.write()
