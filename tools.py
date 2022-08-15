#tools.py
from machine import I2C, Pin
import DS3231
import config
import time
import math

i2c = I2C(sda = Pin(config.sda), scl=Pin(config.scl))
#i2c = I2C(sda = Pin(4), scl=Pin(5))
try:
    ds = DS3231.DS3231(i2c)
except:
    print('Probleem met RTC')

def current_time():
    try: 
        return ds.Time()[0], ds.Time()[1]
    except:
        print('Probleem met tijd ophalen')
        return 0,0

def edit_config(old, new):
    fin = open('config.py')
    data = fin.read()
    data = data.replace(old, new)
    fin.close()

    fin = open('config.py', 'w')
    fin.write(data)
    fin.close()

def save_geelwaarde(oude_geelwaarde, nieuwe_geelwaarde):
    print('kleuralgemeen = ['+str(config.kleuralgemeen[0])+','+str(config.kleuralgemeen[1])+','+str(oude_geelwaarde)+'] wordt kleuralgemeen = ['+str(config.kleuralgemeen[0])+','+str(config.kleuralgemeen[1])+','+str(nieuwe_geelwaarde)+']')
    edit_config('kleuralgemeen = ['+str(config.kleuralgemeen[0])+','+str(config.kleuralgemeen[1])+','+str(oude_geelwaarde)+']','kleuralgemeen = ['+str(config.kleuralgemeen[0])+','+str(config.kleuralgemeen[1])+','+str(nieuwe_geelwaarde)+']')

def limit(value, min, max):
    if int(value) < int(min):
        limitvalue = int(min)
    elif int(value) > int(max):
        limitvalue = int(max)
    else:
        limitvalue = int(value)
    return limitvalue

def set_hour_back(display):
    new_hour,minute = current_time()
    new_hour -= 1
    if new_hour < 0:
        new_hour = 23    
    display.tijd_weergeven(new_hour,minute)
    ds.Time([new_hour,minute,0])
    time.sleep(2)
    
def set_hour_forward(display):
    new_hour,minute = current_time()
    new_hour += 1
    if new_hour > 23:
        new_hour = 0    
    display.tijd_weergeven(new_hour,minute)
    ds.Time([new_hour,minute,0])
    time.sleep(2)

def set_time(display):
    # Eerst uren instellen
    button_back = Pin(config.button_back, Pin.IN, Pin.PULL_UP)
    button_ok = Pin(config.button_ok, Pin.IN, Pin.PULL_UP)
    button_next = Pin(config.button_next, Pin.IN, Pin.PULL_UP)
    
    #print(button_ok.value())
    #print(button_back.value())
    #print(button_next.value())
    # Het is laten knipperen
    for i in range(3):
        display.ledstrip.reset()
        time.sleep(0.1)
        display.show_prefix()
        time.sleep(0.1)
    time.sleep(0.5)
    
    

    print('Start set time mode')
    hour,minute = current_time()
    new_hour = hour
    new_minute = 0
    
    display.tijd_weergeven(hour,minute)
    
    while button_ok.value() != config.invert_button_ok:
        #Zolang button niet ingedrukt

        if button_next.value() == config.invert_button_next:
            new_hour += 1
            if new_hour > 23:
                new_hour = 0
            display.tijd_weergeven(new_hour,0)
            print('Set time hours:  ',new_hour, ':',new_minute)
            time.sleep_ms(300)

        if button_back.value() == config.invert_button_back:
            new_hour -= 1
            if new_hour < 0:
                new_hour = 23
            display.tijd_weergeven(new_hour,0)
            print('Set time hours:  ',new_hour, ':',0)
            time.sleep_ms(300)

    print('Set time in 5 minutes')
    for i in range(3):
        display.ledstrip.reset()
        time.sleep(0.1)
        display.tijd_weergeven(new_hour, 0)
        time.sleep(0.1)
    time.sleep(0.5)
    
    while button_ok.value() != config.invert_button_ok:
        #Zolang button niet ingedrukt

        if button_next.value() == config.invert_button_next:
            new_minute += 5
            if new_minute > 56:
                new_minute = 0
                new_hour += 1
                if new_hour > 23:
                  new_hour = 0
            display.tijd_weergeven(new_hour,new_minute)
            print('Set time 5 mins:  ',new_hour, ':',new_minute)
            time.sleep_ms(300)

        if button_back.value() == config.invert_button_back:
            new_minute -= 5
            if new_minute < 0:
                new_minute = 55
                new_hour -= 1
                if new_hour < 0:
                  new_hour = 23
            display.tijd_weergeven(new_hour,new_minute)
            print('Set time 5 mins:  ',new_hour, ':',new_minute)
            time.sleep_ms(300)

    print('Set minute leds')
    for i in range(3):
        display.minute_leds()
        time.sleep(0.1)
        display.ledstrip.reset()
        time.sleep(0.1)
    
    # Tijd in minuten instellen
    display.tijd_weergeven(new_hour,new_minute)
    minute_leds = 0
    
    while button_ok.value() != config.invert_button_ok:

        if button_next.value() == config.invert_button_next:
            minute_leds += 1
            if minute_leds >= 5:
                minute_leds = 0
            display.tijd_weergeven(new_hour,new_minute+minute_leds)
            print('Set minute:  ',new_minute+minute_leds)
            time.sleep_ms(300)

        if button_back.value() == config.invert_button_back:
            minute_leds -= 1
            if minute_leds < 0:
                minute_leds = 4
            display.tijd_weergeven(new_hour,new_minute+minute_leds)
            print('Set minute:  ',new_minute+minute_leds)
            time.sleep_ms(300)
    
    new_minutes = new_minute + minute_leds
    
    # Definitieve tijd naar RTC schrijven
    ds.Time([new_hour,new_minutes,0])
    
    # Geelwaarde algemeen instellen
    for i in range(3):
        display.show_prefix_and_minute_leds()
        time.sleep(0.1)
        display.ledstrip.reset()
        time.sleep(0.1)
    display.show_prefix_and_minute_leds()
    
    print('Set geelwaarde algemeen')
    geelwaarde_oud = int(config.kleuralgemeen[2])
    geelwaarde_nieuw = geelwaarde_oud
    while button_ok.value() != config.invert_button_ok:
        if button_next.value() == config.invert_button_next:
            geelwaarde_nieuw += 5
            if geelwaarde_nieuw > 255:
                geelwaarde_nieuw = 255
            save_geelwaarde(geelwaarde_oud, geelwaarde_nieuw)
            geelwaarde_oud = geelwaarde_nieuw
            display.ledstrip.renew_colors_algemeen(config.kleuralgemeen[0],config.kleuralgemeen[1],geelwaarde_nieuw)
            display.show_prefix_and_minute_leds()
            time.sleep_ms(50)
    
        if button_back.value() == config.invert_button_back:
            geelwaarde_nieuw -= 5
            if geelwaarde_nieuw < 0:
                geelwaarde_nieuw = 0
            save_geelwaarde(geelwaarde_oud, geelwaarde_nieuw)
            geelwaarde_oud = geelwaarde_nieuw
            display.ledstrip.renew_colors_algemeen(config.kleuralgemeen[0],config.kleuralgemeen[1],geelwaarde_nieuw)
            display.show_prefix_and_minute_leds()   
            time.sleep_ms(50)

    # Instellen klaar, resetten en tijd weergeven.
    display.ledstrip.reset()
    time.sleep(2)
    display.tijd_weergeven(new_hour,new_minutes)




