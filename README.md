# EE250 Final Project:
# Bop IoT

# Ryder Baez, Eric Chen

# Included minigames:
- Bop it        (button : press the button)
- Twist it      (potentiometer : twist the potentiometer at least 300 from what it was)
- Mix it        (led : use potentiometer to match the color)
- Dim it        (light sensor : cover the light sensor)
- Shout it      (sound sensor : shout into the sound sensor, you can also just tap i guess but that's lame)
- ULTRASONit    (ultrasonic ranger : make the ultrasonic sensor read 100 cm difference from what it was before)
- Wordle it     (wordle on the frontend: win at wordle)
- Repeat it     (repeat the previous game)

# Instructions for use
- Connect all the grovepi sensors and devices to the grovepi on one raspberry pi
- Connect the light snsor and the sound sensor to the pcb board on another raspberry pi
- `python3 rpi_pub_and_sub.py` on the grovepi raspberry pi
- `python3 rpi_analog_pub_and_sub.py` on the pcb board raspberry pi
- `python3 vm subscriber.py` on ubuntu VM (will subscribe to MQTT bop its and start flask server, open at http://127.0.0.1:8000 (it is port 8000, server may vary check terminal))
- Press buttons on flask frontend, bop it points and current game will be displayed and updated
- On loss, max score of session and last score are displayed, play again button can be pressed to restart

# NO THOUGHTS HEAD EMPTY
Fulfills:
- At least 3 nodes (raspberry pi 1 (analog sensors), raspberry pi 2 (grovepi sensors), MQTT server, you could also count flask server as a separate node)
- At least 2 physical sensors (potentiometer, ultrasonic ranger, button, 3 leds, RGB LCD screen, light sensor (on PCB), sound sensor (on PCB))
- EXTRA: 1 virtual API sensor (5 letter word API: `https://random-word-api.herokuapp.com/home`)
- Simple event processing and encryption (win/loss of bop it, no cheating in bop it)
- Data transfer between nodes (MQTT pub/sub)
- Data transfer between nodes (uses socket to send signals to flask frontend from MQTT callbacks)
- Web frontend (flask and flask_socketIO)

External Libraries (check files):
- MQTT Paho
- Flask
- Flask socketio
- Fernet (cryptography)
