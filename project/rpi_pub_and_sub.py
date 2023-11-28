"""Run rpi_pub_and_sub.py on your Raspberry Pi."""
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import time
import sys
import random
sys.path.append('../../lab-02-grovepi-sensors-RyderBaez/Software/Python/') #make sure this is okay later
sys.path.append('../../lab-02-grovepi-sensors-RyderBaez/Software/Python/grove_rgb_lcd')
from grove_rgb_lcd import *
import grovepi
key = b'452diyhX782Qnkwe4OLbM6dFOvYERO9Jx0IEAotNweg='
f = Fernet(key)
PORT = 4
ultrasonic_ranger = 4
potentiometer = 2 #where to plug everything in
redled = 3
greenled = 7
blueled = 8
button = 2
full_angle = 1027
grovepi.pinMode(redled, "OUTPUT")
grovepi.pinMode(greenled, "OUTPUT")
grovepi.pinMode(blueled, "OUTPUT")
grovepi.pinMode(button, "INPUT")

grovepi.pinMode(potentiometer,"INPUT")
grovepi.pinMode(ultrasonic_ranger,"INPUT")
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("bopit/complete")
    client.subscribe("bopit/ultrasonicRanger")
    client.subscribe("bopit/potentiometer")
    client.subscribe("bopit/button")
    client.subscribe("bopit/led")
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message_Ultrasonic(client, userdata, msg):
    ultradistance = grovepi.ultrasonicRead(PORT)
    timepassed = 0
    value = 0
    time.sleep(.2)
    while timepassed < 20:
        value = grovepi.ultrasonicRead(PORT)
        if abs(value - ultradistance) > 50:
            encoded_text = f.encrypt(b"Passed")
            client.publish("bopit/complete", encoded_text)
            return
        timepassed += 1
        time.sleep(.2)
    encoded_text = f.encrypt(b"Failed")
    client.publish("bopit/complete", encoded_text)
        
def on_message_Potentiometer(client, userdata, msg):
    sensor_value = grovepi.analogRead(potentiometer)
    timepassed = 0
    value = 0
    time.sleep(.2)
    while timepassed < 20:
        value = grovepi.analogRead(potentiometer)
        if abs(value - sensor_value) > 150:
            encoded_text = f.encrypt(b"Passed")
            client.publish("bopit/complete", encoded_text)
            return
        timepassed += 1
        time.sleep(.2)
    encoded_text = f.encrypt(b"Failed")
    client.publish("bopit/complete", encoded_text)
        
def on_message_Button(client, userdata, msg): #1st possible bop
    timepassed = 0
    while timepassed < 500:
        if grovepi.digitalRead(button):
            encoded_text = f.encrypt(b"Passed")
            client.publish("bopit/complete", encoded_text)
            return
        timepassed += 1
        #print("hey")
        time.sleep(.01)
    encoded_text = f.encrypt(b"Failed")
    client.publish("bopit/complete", encoded_text)
    
#def on_message_LCD(client, userdata, msg):
 #   if str(msg.payload, "utf-8") == 'w' or str(msg.payload, "utf-8") == 's' or str(msg.payload, "utf-8") == 'a' or str(msg.payload, "utf-8") == 'd': 
  #      buf = str(msg.payload, "utf-8") + "               "
   #     setText_norefresh(buf)
def on_message_LED(client, userdata, msg):
    colorchoice = random.randint(0,30)
    if colorchoice % 2 == 0: #50% chance
        redval = 1
        grovepi.digitalWrite(redled, 1)
    else:
        redval = 0
        grovepi.digitalWrite(redled, 0)
    if colorchoice % 3 == 0 or colorchoice % 5 == 0:#50% chance
        greenval = 1
        grovepi.digitalWrite(greenled, 1)
    else:
        greenval = 0
        grovepi.digitalWrite(greenled, 0)
    if colorchoice < 15:#50% chance
        blueval = 1
        grovepi.digitalWrite(blueled, 1)
    else:
        blueval = 0
        grovepi.digitalWrite(blueled, 0)     
    timepassed = 0
    while timepassed < 80:
        sensor_value = grovepi.analogRead(potentiometer)
        if sensor_value > (7 * full_angle / 9):
            setRGB(128, 128, 128)
            redset = 1
            greenset = 1
            blueset = 1
        elif sensor_value > (6 * full_angle / 9):
            setRGB(128, 0, 128)
            redset = 1
            greenset = 0
            blueset = 1
        elif sensor_value > (5 * full_angle / 9):
            setRGB(0, 128, 128)
            redset = 0
            greenset = 1
            blueset = 1
        elif sensor_value > (4 * full_angle / 9):
            setRGB(128, 128, 0)
            redset = 1
            greenset = 1
            blueset = 0
        elif sensor_value > (3 * full_angle / 9):
            setRGB(0, 0, 128)
            redset = 0
            greenset = 0
            blueset = 1
        elif sensor_value > (2*full_angle / 9):
            setRGB(128, 0, 0)
            redset = 1
            greenset = 0
            blueset = 0
        elif sensor_value > (full_angle/9):
            setRGB(0, 128, 0)
            redset = 0
            greenset = 1
            blueset = 0
        else:       #Player is actually getting shafted if the random number is 17 or 19 or 23 or 29
            setRGB(0, 0, 0)
            redset = 0
            greenset = 0
            blueset = 0
        if grovepi.digitalRead(button) and redset == redval and greenset == greenval and blueset == blueval:
            encoded_text = f.encrypt(b"Passed")
            client.publish("bopit/complete", encoded_text)
            return
        timepassed += 1
        time.sleep(.05)
    encoded_text = f.encrypt(b"Failed")
    client.publish("bopit/complete", encoded_text)



def on_message_Complete(client, userdata, msg):  
    pass 
def on_message(client, userdata, msg):
        
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
       

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    #client.message_callback_add("rbbaez/lcd", on_message_LCD)
    client.message_callback_add("bopit/led", on_message_LED)
    client.message_callback_add("bopit/ultrasonicRanger", on_message_Ultrasonic)
    client.message_callback_add("bopit/potentiometer", on_message_Potentiometer)
    client.message_callback_add("bopit/button", on_message_Button)
    client.message_callback_add("bopit/complete", on_message_Complete)
    client.loop_start()
    setRGB(0,0,0)
    grovepi.pinMode(button,"INPUT")
    while True:
        time.sleep(1)
            

