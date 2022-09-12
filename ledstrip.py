import config
import math
import neopixel
import tsl2561
from machine import I2C, Pin
from time import sleep

if config.luxsensor:
    i2c = I2C(sda = Pin(config.sda), scl= Pin(config.scl))
    try:
        if config.luxsensor_type == 'TSL2561':
            luxsensor = tsl2561.TSL2561(i2c)
            print('Luxsensor initiated')
        else:
            luxsensor = 
    except:
        print('Error in lux sensor')
        
class led_strip:
    def __init__(self):
        self.total_pixels = config.matrix_width * config.matrix_height + 4  # Height * width + 4 minute leds
        self.ledstrip = neopixel.NeoPixel(Pin(config.ledstrip_pin), self.total_pixels)
        self.r = int(config.led_color[0])
        self.g = int(config.led_color[1])
        self.b = int(config.led_color[2])
        self.minute_led_numbers = config.minute_led_numbers
        self.brightness_factor = int(config.brightness_factor)
        self.min_brightness = int(config.min_brightness)
        self.max_brightness = int(config.max_brightness)
        self.ledrange_old = []
        self.ledrange_minutes_old = []
    
    def renew_colors(self,r,g,b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
    
    def reset(self): # turn led strip off
        for i in range(0,self.total_pixels):
            self.ledstrip[i] = (0,0,0)
        self.ledrange_old = []
        self.ledrange_minutes_old = []
        self.ledstrip.write()
       
    def getlux(self):
        if config.luxsensor:
            try:
                if config.luxsensor_type == 'TSL2561':
                    lux = luxsensor.read()
                else
                    lux = bh1750.sample(i2c)
            except:
                print('Fout in luxsensor')
            return lux
        else:
            return '"False"'
    
    def program_pixel(self, ledrange, ledminuterange): # light up leds according to the current time
        if config.luxsensor:
            try:
                lux = luxsensor.read()
                brightness = lux * self.brightness_factor / 100
            except:
                print('Fout in luxsensor')
                brightness = self.brightness_factor / 50
        else:
            brightness = self.brightness_factor / 50

        # Brightness should remain between 0 and 1
        if brightness > self.max_brightness/100 or brightness > 1:
            brightness = self.max_brightness/100
        elif brightness < self.min_brightness/100 or brightness < 0:
            brightness = self.min_brightness/100
        
        # Convert RGB to range between 0 and 255 
        r_led = math.floor(self.r / max(self.r,self.g,self.b) * brightness * 255)
        g_led = math.floor(self.g / max(self.r,self.g,self.b) * brightness * 255)
        b_led = math.floor(self.b / max(self.r,self.g,self.b) * brightness * 255)

        # Check for each led (not the minute leds) if it should be turned on or off
        for i in range(2,self.total_pixels-2):
            if i in ledrange:
                # Turn led on
                self.ledstrip[i] = (r_led,g_led,b_led)
            if i not in ledrange and i in self.ledrange_old:
                # Turn led off
                self.ledstrip[i] = (0,0,0)
                #print(str(i)+' moet uit maar stond dit nog niet')
        
        # Check for each minute leds too
        for i in self.minute_led_numbers:
            if i in ledminuterange:
                self.ledstrip[i] = (r_led,g_led,b_led)
            if i not in ledminuterange and i in self.ledrange_minutes_old:
                self.ledstrip[i] = (0,0,0)
        
        self.ledstrip.write()
        
        self.ledrange_old = ledrange
        self.ledrange_minutes_old = ledminuterange

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
