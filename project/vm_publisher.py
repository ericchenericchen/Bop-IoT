"""Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("rbbaez/led")
    client.subscribe("rbbaez/lcd")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':
        print("w")
        client.publish("rbbaez/lcd", 'w')
        #send "w" character to rpi
    elif k == 'a':
        print("a")
        client.publish("rbbaez/lcd", 'a')
        # send "a" character to rpi
        client.publish("rbbaez/led", "LED_ON")
        #send "LED_ON"
    elif k == 's':
        print("s")
        client.publish("rbbaez/lcd", 's')
        # send "s" character to rpi
    elif k == 'd':
        print("d")
        client.publish("rbbaez/lcd", 'd')
        # send "d" character to rpi
        client.publish("rbbaez/led", "LED_OFF")
        # send "LED_OFF"

if __name__ == '__main__':
    #setup the keyboard event listeners
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        on_press(input(""))
        time.sleep(1)