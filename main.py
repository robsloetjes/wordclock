#try: 

import display
import tools
import ledstrip
import config
from time import sleep
from machine import Pin
import micropython


class Woordklok:
  def __init__(self):
      print('Begin opstartsequentie')
      self.ledstrip = ledstrip.led_strip()
      self.display = display.tijdsweergave(self.ledstrip)
      self.hour,self.minute = tools.current_time()
      self.button_ok = Pin(config.button_ok, Pin.IN, Pin.PULL_UP)
      self.button_back = Pin(config.button_back, Pin.IN, Pin.PULL_UP)
      self.button_next = Pin(config.button_next, Pin.IN, Pin.PULL_UP)
      self.woordklok_update(True)
      print('Einde opstartsequentie')
      
  def woordklok_update(self, force=False):
      hour,minute = tools.current_time()
      
      if self.hour != hour or self.minute != minute or force == True:
          gc.collect()
          if force == True:
              print('Geforceerd tijd vernieuwen en weergeven')
          self.hour = hour
          self.minute = minute
          self.display.tijd_weergeven(hour, minute)
          print(str(hour)+':'+str(minute))

  def run(self):
      while True:              
          #print(self.button_back.value())
          #print(self.button_ok.value())
          #print(self.button_next.value())
          
          if self.button_ok.value() == config.invert_button_ok:
              print('Button pushed, in set time mode')
              tools.set_time(self.display)
          if self.button_back.value() == config.invert_button_back:
              print('Button back pushed, set one hour back')
              tools.set_hour_back(self.display)
          if self.button_next.value() == config.invert_button_next:
              print('Button next pushed, set one hour forward')
              tools.set_hour_forward(self.display)
          self.woordklok_update()
          sleep(.25)

Woordklok = Woordklok()
Woordklok.run()

#except Exception as e:
    #print('Foutmelding, herstarten: {}'.format(str(e)))
    #logf = open("error.txt", "w")
    #logf.write("Foutmelding: {}\n".format(str(e)))
    #logf.close()
    #import time
    #time.sleep(15)
    #import machine
    #machine.reset()

