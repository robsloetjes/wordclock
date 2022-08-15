try: 
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
      self.hour,self.minute = tools.current_time()
      # Initiate buttons
      self.button_ok = Pin(config.button_ok, Pin.IN, Pin.PULL_UP)
      self.button_back = Pin(config.button_back, Pin.IN, Pin.PULL_UP)
      self.button_next = Pin(config.button_next, Pin.IN, Pin.PULL_UP)
      # Force update of the clock to display current time
      self.woordklok_update(True)
      print('Started Wordclock')

    def woordklok_update(self, force=False):
      hour,minute = tools.current_time()

      if self.hour != hour or self.minute != minute or force == True:
        # Change in time, change clock
        self.hour = hour
        self.minute = minute
        self.display.show_time(hour, minute)
        print(str(hour)+':'+str(minute))

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
        sleep(.25)

  wordclock = Wordclock()
  wordclock.run()

except Exception as e:
  print('Critical error, restart wordclock: {}'.format(str(e)))
  # First try to log error to file since not always a terminal is connected
  logf = open("error.txt", "w")
  logf.write("Critical error: {}\n".format(str(e)))
  logf.close()
  import time
  time.sleep(15)
  import machine
  machine.reset()

