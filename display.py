#tijd_weergeven.py
import math
import config

class layout:
    def __init__(self):
        self.prefix = list(range(0,3)) + list(range(4,6))
        self.minutes=[[], \
            list(range(7,11)) + list(range(40,44)), \
            list(range(11,15)) + list(range(40,44)), \
            list(range(28,33)) + list(range(40,44)), \
            list(range(11,15)) + list(range(18,22)) + list(range(33,37)), \
            list(range(7,11)) + list(range(18,22)) + list(range(33,37)), \
            list(range(33,37)), \
            list(range(7,11)) + list(range(22,26)) + list(range(33,37)), \
            list(range(11,15)) + list(range(22,26)) + list(range(33,37)), \
            list(range(28,33)) + list(range(44,48)), \
            list(range(11,15)) + list(range(44,48)), \
            list(range(7,11)) + list(range(44,48)) ]
        self.hours= [list(range(99,105)), \
            list(range(51,54)), \
            list(range(55,59)), \
            list(range(62,66)), \
            list(range(66,70)), \
            list(range(70,74)), \
            list(range(74,77)), \
            list(range(77,82)), \
            list(range(88,92)), \
            list(range(83,88)), \
            list(range(91,95)), \
            list(range(96,99)), \
            list(range(99,105))]
        self.full_hour= list(range(107,110))

    def get_tijdsrange(self, tijduur, tijdminuut):
        return self.prefix + self.minutes[int(tijdminuut/5)] + self.hours[tijduur%12+(0 if tijdminuut/5 < 4 else 1)] + (self.full_hour if (tijdminuut < 5) else [])

class tijdsweergave:
    def __init__(self, ledstrip):
        self.tijdsranges = layout()
        self.breedte = 11
        self.hoogte = 10
        self.ledstrip = ledstrip
        
    def tijd_weergeven(self, hour, minute):
        
        tijdsranges = self.tijdsranges.get_tijdsrange(hour, minute)
        # Range omzetten naar coordinaten en uitvoeren
        
        ledminuutrange = []
        if minute%5 == 1:
            ledminuutrange = [self.breedte*self.hoogte+3]
        elif minute%5 == 2:
            ledminuutrange = [self.breedte*self.hoogte+3,1]
        elif minute%5 == 3:
            ledminuutrange = [self.breedte*self.hoogte+3,1,self.breedte*self.hoogte+2]
        elif minute%5 == 4:
            ledminuutrange = [self.breedte*self.hoogte+3,1,self.breedte*self.hoogte+2,0]
        
        ledrange = []
        for i in tijdsranges:
            
            # kolom is volledige breedte minus het residu als je door breedte deelt
            x = (self.breedte-i%self.breedte)
            # rij is: i/breedte, afgerond naar beneden
            y = math.floor(i/self.breedte) + 1
            #print(letterlijst[i]+ ': '+str(i)+' is '+str(x)+','+str(y))
            if x%2 == 1:
                # oneven kolommen, van boven naar beneden
                ledrange.append((x-1) * self.hoogte + y + 1)
            else:
                ledrange.append((x-1) * self.hoogte + self.hoogte -y + 2)
            
        # print(ledrange, ledminuutrange)
        self.ledstrip.program_pixel(ledrange, ledminuutrange)
    
    def show_prefix(self):
        self.ledstrip.program_pixel([102,101,82,62,61], [])
        
    def minute_leds(self):
        self.ledstrip.program_pixel([],[self.breedte*self.hoogte+3,1,self.breedte*self.hoogte+2,0])
        
    def show_prefix_and_minute_leds(self):
        self.ledstrip.program_pixel([102,101,82,62,61], [self.breedte*self.hoogte+3,1,self.breedte*self.hoogte+2,0])




