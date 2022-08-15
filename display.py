import math
import config

class layout:
    # The layout contains the positions of all words, starting at the top left and continue counting after each row
    def __init__(self):
        # "HET IS" (Dutch for IT IS) always lit
        self.prefix = list(range(0,3)) + list(range(4,6))
        
        # Minutes from "VIJF OVER" (5 past) to "VIJF VOOR" (5 to)
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
        
        # Hours from "EEN" (one) to "TWAALF" (twelve)
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
        
        # "UUR" (hour) in case of the full hour
        self.full_hour= list(range(107,110))

    def get_timerange(self, timehour, timeminute):
        return self.prefix + self.minutes[int(timeminute/5)] + self.hours[timehour%12+(0 if timeminute/5 < 4 else 1)] + (self.full_hour if (timeminute < 5) else [])

class Display:
    def __init__(self, ledstrip):
        self.timeranges = layout()
        self.prefix = config.prefix
        self.width = config.matrix_width
        self.height = config.matrix_height
        self.ledstrip = ledstrip
        
    def show_time(self, hour, minute):
        # Create range of all words that need to light up
        timeranges = self.timeranges.get_timerange(hour, minute)
        
        # Convert range to coordinates
        # First list minute leds to light up
        ledminuterange = []
        if minute%5 == 1:
            ledminuterange = [self.width*self.height+3]
        elif minute%5 == 2:
            ledminuterange = [self.width*self.height+3,1]
        elif minute%5 == 3:
            ledminuterange = [self.width*self.height+3,1,self.width*self.height+2]
        elif minute%5 == 4:
            ledminuterange = [self.width*self.height+3,1,self.width*self.height+2,0]
        
        ledrange = []
        for i in timeranges:
            # Convert horizontal position number to led number in the led string
            x = (self.width-i%self.width)
            y = math.floor(i/self.width) + 1
            if x%2 == 1:  # Numbering depends on even or odd columns due to wiring
                ledrange.append((x-1) * self.height + y + 1)
            else:
                ledrange.append((x-1) * self.height + self.height -y + 2)
            
        self.ledstrip.program_pixel(ledrange, ledminuterange)
    
    def show_prefix(self):
        self.ledstrip.program_pixel(self.prefix, [])
        
    def minute_leds(self):
        self.ledstrip.program_pixel([],[self.width*self.height+3,1,self.width*self.height+2,0])
        
    def show_prefix_and_minute_leds(self):
        self.ledstrip.program_pixel(self.prefix, [self.width*self.height+3,1,self.width*self.height+2,0])




