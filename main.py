import display
import tools
import ledstrip
import config
from time import sleep
from machine import Pin
import micropython

class Wordclock:
  def __init__(self):
    print('Starting Wordclock')
    # Initiate the ledstrip, display and set current time
    self.ledstrip = ledstrip.led_strip()
    self.display = display.Display(self.ledstrip)
    # Initiate buttons
    self.button_ok = Pin(config.button_ok, Pin.IN, Pin.PULL_UP)
    self.button_back = Pin(config.button_back, Pin.IN, Pin.PULL_UP)
    self.button_next = Pin(config.button_next, Pin.IN, Pin.PULL_UP)
    # Force update of the clock to display current time
    self.woordklok_update(True)
    print('Started Wordclock')

  def woordklok_update(self, force=False):
    hour,minute,second = tools.current_time()

    if second%5==0 or force == True:
      # Update each 5 seconds so if clock shows jabberish, it is resolved quickly
      self.display.show_time(hour, minute, True)
      # print(str(hour)+':'+str(minute))

  def run(self):
    while True:
      # Check for button presses
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
      sleep(1)

wordclock = Wordclock()
wordclock.run()
