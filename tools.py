#tools.py
from machine import I2C, Pin
import DS3231
import config
import time
import math

i2c = I2C(sda = Pin(config.sda), scl=Pin(config.scl))
try:
    ds = DS3231.DS3231(i2c)
    print('RTC initiated')
except:
    print('Problem with RTC')

def current_time():
    try: 
        return ds.Time()[0], ds.Time()[1], ds.Time()[2]
    except:
        print('Cannot collect time')
        return 0,0

def edit_config(old, new):
    fin = open('config.py')
    data = fin.read()
    data = data.replace(old, new)
    fin.close()

    fin = open('config.py', 'w')
    fin.write(data)
    fin.close()

def save_yellow_value(old_yellow_value, new_yellow_value):
    print('led_color = ['+str(config.led_color[0])+','+str(config.led_color[1])+','+str(old_yellow_value)+'] changed in led_color = ['+str(config.led_color[0])+','+str(config.led_color[1])+','+str(new_yellow_value)+']')
    edit_config('led_color = ['+str(config.led_color[0])+','+str(config.led_color[1])+','+str(old_yellow_value)+']','led_color = ['+str(config.led_color[0])+','+str(config.led_color[1])+','+str(new_yellow_value)+']')

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
    display.show_time(new_hour,minute)
    ds.Time([new_hour,minute,0])
    time.sleep(2)
    
def set_hour_forward(display):
    new_hour,minute = current_time()
    new_hour += 1
    if new_hour > 23:
        new_hour = 0    
    display.show_time(new_hour,minute)
    ds.Time([new_hour,minute,0])
    time.sleep(2)

def set_time(display):
    # First set hours
    button_back = Pin(config.button_back, Pin.IN, Pin.PULL_UP)
    button_ok = Pin(config.button_ok, Pin.IN, Pin.PULL_UP)
    button_next = Pin(config.button_next, Pin.IN, Pin.PULL_UP)

    # Blink "HET IS"
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
    
    display.show_time(hour,minute)
    
    while button_ok.value() != config.invert_button_ok:
        # While button OK not pressed

        if button_next.value() == config.invert_button_next:
            new_hour += 1
            if new_hour > 23:
                new_hour = 0
            display.show_time(new_hour,0)
            print('Set time hours:  ',new_hour, ':',new_minute)
            time.sleep_ms(300)

        if button_back.value() == config.invert_button_back:
            new_hour -= 1
            if new_hour < 0:
                new_hour = 23
            display.show_time(new_hour,0)
            print('Set time hours:  ',new_hour, ':',0)
            time.sleep_ms(300)

    print('Set time in 5 minutes')
    # Blink "HET IS [HOUR]"
    for i in range(3):
        display.ledstrip.reset()
        time.sleep(0.1)
        display.show_time(new_hour, 0)
        time.sleep(0.1)
    time.sleep(0.5)
    
    while button_ok.value() != config.invert_button_ok:
        # While button OK not pressed

        if button_next.value() == config.invert_button_next:
            new_minute += 5
            if new_minute > 56:
                new_minute = 0
                new_hour += 1
                if new_hour > 23:
                  new_hour = 0
            display.show_time(new_hour,new_minute)
            print('Set time 5 mins:  ',new_hour, ':',new_minute)
            time.sleep_ms(300)

        if button_back.value() == config.invert_button_back:
            new_minute -= 5
            if new_minute < 0:
                new_minute = 55
                new_hour -= 1
                if new_hour < 0:
                  new_hour = 23
            display.show_time(new_hour,new_minute)
            print('Set time 5 mins:  ',new_hour, ':',new_minute)
            time.sleep_ms(300)

    print('Set minute leds')
    for i in range(3):
        display.minute_leds()
        time.sleep(0.1)
        display.ledstrip.reset()
        time.sleep(0.1)
    
    # Set minute leds
    display.show_time(new_hour,new_minute)
    minute_leds = 0
    
    while button_ok.value() != config.invert_button_ok:
        # While button OK not pressed
        if button_next.value() == config.invert_button_next:
            minute_leds += 1
            if minute_leds >= 5:
                minute_leds = 0
            display.show_time(new_hour,new_minute+minute_leds)
            print('Set minute:  ',new_minute+minute_leds)
            time.sleep_ms(300)

        if button_back.value() == config.invert_button_back:
            minute_leds -= 1
            if minute_leds < 0:
                minute_leds = 4
            display.show_time(new_hour,new_minute+minute_leds)
            print('Set minute:  ',new_minute+minute_leds)
            time.sleep_ms(300)
    
    new_minutes = new_minute + minute_leds
    
    # Write new time to RTC
    ds.Time([new_hour,new_minutes,0])
    
    # Next step: set yellow value of leds (from white to yellow)
    # Blink prefix and minute leds
    for i in range(3):
        display.show_prefix_and_minute_leds()
        time.sleep(0.1)
        display.ledstrip.reset()
        time.sleep(0.1)
    display.show_prefix_and_minute_leds()
    
    print('Set yellow value')
    old_yellow_value = int(config.led_color[2])
    new_yellow_value = old_yellow_value
    while button_ok.value() != config.invert_button_ok:
        if button_next.value() == config.invert_button_next:
            new_yellow_value += 5
            if new_yellow_value > 255:
                new_yellow_value = 255
            save_yellow_value(old_yellow_value, new_yellow_value)
            old_yellow_value = new_yellow_value
            display.ledstrip.renew_colors(config.led_color[0],config.led_color[1],new_yellow_value)
            display.show_prefix_and_minute_leds()
            time.sleep_ms(50)
    
        if button_back.value() == config.invert_button_back:
            new_yellow_value -= 5
            if new_yellow_value < 0:
                new_yellow_value = 0
            save_yellow_value(old_yellow_value, new_yellow_value)
            old_yellow_value = new_yellow_value
            display.ledstrip.renew_colors(config.led_color[0],config.led_color[1],new_yellow_value)
            display.show_prefix_and_minute_leds()   
            time.sleep_ms(50)

    # Ready setting up time and yellow value, reset the clock
    display.ledstrip.reset()
    time.sleep(2)
    display.show_time(new_hour,new_minutes)
