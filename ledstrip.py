import config
import math
import neopixel
from machine import I2C, Pin
from time import sleep

if config.luxsensor:
    i2c = I2C(sda = Pin(config.sda), scl= Pin(config.scl))
    if config.luxsensor_type == 'TSL2561':
        try:
            import tsl2561

            luxsensor = tsl2561.TSL2561(i2c)
        except:
            print('Fout in luxsensor')
    else:
        import bh1750
        
class led_strip:
    def __init__(self):
        self.totaal_pixels = 114
        self.ledstrip = neopixel.NeoPixel(Pin(config.ledstrip_pin), self.totaal_pixels) #ledstrip aanmaken
        self.r_alg = int(config.kleuralgemeen[0])
        self.g_alg = int(config.kleuralgemeen[1])
        self.b_alg = int(config.kleuralgemeen[2])
        self.helderheidsfactor = int(config.helderheidsfactor)
        self.min_helderheid = int(config.min_helderheid)
        self.max_helderheid = int(config.max_helderheid)
        self.ledrange_oud = []
        self.ledrange_min_oud = []
    
    def renew_colors_algemeen(self,r,g,b):
        self.r_alg = int(r)
        self.g_alg = int(g)
        self.b_alg = int(b)
        print('nieuwe blauwwaarde is '+str(self.b_alg))
    
    def reset(self): # ledstrip uitzetten
        for i in range(0,self.totaal_pixels):
            self.ledstrip[i] = (0,0,0)
        self.ledrange_oud = []
        self.ledrange_min_oud = []
        self.ledstrip.write()
       
    def getlux(self):
        if config.luxsensor:
            if config.luxsensor_type == 'TSL2561':
                try:
                    lux = luxsensor.read()
                except:
                    print('Fout in luxsensor')
                return lux
            elif config.luxsensor_type == 'BH1750':
                lux = bh1750.sample(i2c)
                return math.sqrt(lux)/2
        else:
            return '"False"'
    
    def program_pixel(self, ledrange, ledminuutrange): # ledstrip programmeren

        if config.luxsensor:
            try:
                if config.luxsensor_type == 'TSL2561':
                    lux = luxsensor.read()
                elif config.luxsensor_type == 'BH1750':
                    luxread = bh1750.sample(i2c)
                    lux = math.sqrt(luxread)/2
                helderheid = lux * self.helderheidsfactor / 100
            except:
                print('Fout in luxsensor')
                helderheid = self.helderheidsfactor / 50
        else:
            helderheid = self.helderheidsfactor / 50

        if helderheid > self.max_helderheid/100 or helderheid > 1:
            helderheid = self.max_helderheid/100
        elif helderheid < self.min_helderheid/100 or helderheid < 0:
            helderheid = self.min_helderheid/100
            
        r_led = math.floor(self.r_alg / max(self.r_alg,self.g_alg,self.b_alg) * helderheid * 255) # de waarden van RGB naar verhouding t.o.v. 255 brengen, 
        g_led = math.floor(self.g_alg / max(self.r_alg,self.g_alg,self.b_alg) * helderheid * 255) # waarbij helderheid factor tussen 0 en 1
        b_led = math.floor(self.b_alg / max(self.r_alg,self.g_alg,self.b_alg) * helderheid * 255) # en vermenigvuldigen met helderheid

        for i in range(2,112):
            if i in ledrange:
                # Led moet aan, dus sowieso vernieuwen voor juiste helderheid
                self.ledstrip[i] = (r_led,g_led,b_led)
                #print(str(i)+' moet aan maar stond dit nog niet')
            if i not in ledrange and i in self.ledrange_oud:
                # Led stond aan maar moet uit
                self.ledstrip[i] = (0,0,0)
                #print(str(i)+' moet uit maar stond dit nog niet')
        
        
        for i in [0,1, 112, 113]:
            if i in ledminuutrange:
                # Led moet aan, dus sowieso vernieuwen voor juiste helderheid
                self.ledstrip[i] = (r_led,g_led,b_led)
                #print(str(i)+' moet aan maar stond dit nog niet')
            if i not in ledminuutrange and i in self.ledrange_min_oud:
                # Led stond aan maar moet uit
                self.ledstrip[i] = (0,0,0)
                #print(str(i)+' moet uit maar stond dit nog niet')

        
        self.ledstrip.write()
        
        self.ledrange_oud = ledrange
        self.ledrange_min_oud = ledminuutrange

def loop_leds():
    ledstrip = neopixel.NeoPixel(Pin(14), 114)
    for i in range(0,114):
        ledstrip[i] = (255,255,255)
        if i>0:
            ledstrip[i-1] = (0,0,0)
        ledstrip.write()
        sleep(0.05)
    for i in range(0,114):
        ledstrip[i] = (0,0,0)
    ledstrip.write()







