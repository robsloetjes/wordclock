# Variables free to change (no operational issues expected):

brightness_factor = 30  # Brightness in percents
min_brightness = 10  # 0-100%
max_brightness = 80  # 0-100%
led_color = [255,255,50]

luxsensor = True  # Change to false if no light sensor is connected, brightness will remain at 50% all time
luxsensor_type = 'BH1750' # 'TSL2561' or 'BH1750'

scl = 5 # D1
sda = 4 # D2
ledstrip_pin = 15 # D8
button_back = 14 #D5
invert_button_back = False
button_ok = 12 # D6
invert_button_ok = False
button_next = 13 # D7
invert_button_next = False

# Variables that will cause trouble if changed
matrix_width = 11
matrix_height = 10
prefix = [102,101,82,62,61]
minute_led_numbers = [0, 1, 112, 113]






























