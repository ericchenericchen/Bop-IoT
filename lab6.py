import requests
import sys
import time

# sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')
# #sys.path.append('/home/pi/Dexter/GrovePi/Software/Python/grove_rgb_lcd')


# import grovepi
# import grove_rgb_lcd as lcd

# Modules for my apps
import my_reddit
import my_weather
import my_spotify  # TODO: Create my_app.py using another API, following the examples as a template

PORT_BUZZER = 2     # D2
PORT_BUTTON = 4     # D4
PORT_POTENTIOMETER = 1 # D1

LCD_LINE_LEN = 16

# Setup
# grovepi.pinMode(PORT_BUZZER, "OUTPUT")
# grovepi.pinMode(PORT_BUTTON, "INPUT")
# grovepi.pinMode(PORT_POTENTIOMETER, "INPUT")

# Installed Apps!
APPS = [
    my_weather.WEATHER_APP,
    my_reddit.QOTD_APP,
    # TODO: Add your new app here
    my_spotify.SPOTIFY_APP
]

# Cache to store values so we save time and don't abuse the APIs
CACHE = [''] * len(APPS)
for i in range(len(APPS)):
    # Includes a two space offset so that the scrolling works better
    CACHE[i] = '  ' + APPS[i]['init']()

app = 0     # Active app
ind = 0     # Output index

old_potentiometer = 0
new_potentiometer = 0

while True:
    try:
        # Check for input
        if grovepi.digitalRead(PORT_BUTTON):
            # BEEP!
            grovepi.digitalWrite(PORT_BUZZER, 1)

            # Switch app
            app = (app + 1) % len(APPS)
            ind = 0

        time.sleep(0.1)

        grovepi.digitalWrite(PORT_BUZZER, 0)

        # Check potentiometer, have range measurement from 0-99
        new_potentiometer = grovepi.analogRead(PORT_POTENTIOMETER) % 100

        # if potentiometer measurement changed, check to change LCD color
        if(new_potentiometer != old_potentiometer):
            old_potentiometer = new_potentiometer

            if new_potentiometer < 20:
                lcd.setRGB(0, 128, 0) #base color
            elif new_potentiometer < 40:
                lcd.setRGB(255, 0, 0) #red
            elif new_potentiometer < 60:
                lcd.setRGB(0, 255, 0) #green
            elif new_potentiometer < 80:
                lcd.setRGB(0, 0, 255) #blue
            else:
                lcd.setRGB(255, 0, 255) #purple

        # Display app name
        lcd.setText_norefresh(APPS[app]['name'])
        # print(APPS[app]['name'])

        # Scroll output
        lcd.setText_norefresh('\n' + CACHE[app][ind:ind+LCD_LINE_LEN])
        # print('\n' + CACHE[app][ind:ind+LCD_LINE_LEN])

        # TODO: Make the output scroll across the screen (should take 1-2 lines of code)
        if ind+LCD_LINE_LEN < len(CACHE[app]) - 1:
            ind = ind + 1
        else:
            ind = 0

    except KeyboardInterrupt:
        # Gracefully shutdown on Ctrl-C
        lcd.setText('')
        lcd.setRGB(0, 0, 0)

        # Turn buzzer off just in case
        grovepi.digitalWrite(PORT_BUZZER, 0)

        break

    except IOError as ioe:
        if str(ioe) == '121':
            # Retry after LCD error
            time.sleep(0.25)

        else:
            raise
