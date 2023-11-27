# EE250 Final Project:
# Bop It

# Ryder Baez, Eric Chen

# Included minigames:
- Bop it        (button : press the button)
- Twist it      (potentiometer : twist the potentiometer at least 300 from what it was)
- Mix it        (led : use potentiometer to match the color)
- Dim it        (light sensor : cover the light sensor)
- Shout it      (sound sensor : shout into the sound sensor, you can also just tap i guess but that's lame)
- ULTRASONit    (ultrasonic ranger : make the ultrasonic sensor read 100 cm difference from what it was before)
- Wordle it     (wordle on the frontend: win at wordle)

# Instructions for use
- Connect all the sensors and devices to the grovepi and the pcb shield
- start rpi pub and sub.py
- start rpi analog pub and sub.py
- start vm subscriber.py
- starting vm subscriber.py with `python3 vm_subscriber.py` will start the flask server
    - since i can't test it i'm not sure if the flask server will work with mqtt but i think it should since it will run on a different thread
- pray it works.

# NO THOUGHTS HEAD EMPTY
- OK let's think about this project structure.
    - currently we have 3 nodes. the bop it, the local machine, and MQTT server (and i guess the api call can be another sensor as well)
    - 


Fulfills:
- 3 nodes
- 2 physical sensors
- 1 virtual API sensor (hopefully)
- Simple event processing and encryption
- Data transfer between nodes (do we want to use cloud?)
- Web frontend