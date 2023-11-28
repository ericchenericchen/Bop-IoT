"""Run rpi_pub_and_sub.py on your Raspberry Pi."""
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import time
import sys
import random
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
key = b'452diyhX782Qnkwe4OLbM6dFOvYERO9Jx0IEAotNweg='
f = Fernet(key)
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
lowlight = 250
tapped = 250
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("bopit/complete")
    client.subscribe("bopit/mic")
    client.subscribe("bopit/light")
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
        
def on_message_Mic(client, userdata, msg):
    timepassed = 0
    while timepassed < 20:
        value = mcp.read_adc(1)
        if(value > tapped):
            encoded_text = f.encrypt(b"Passed")
            client.publish("bopit/complete", encoded_text)
            return
        timepassed += 1
        time.sleep(.2)
    encoded_text = f.encrypt(b"Failed")
    client.publish("bopit/complete", encoded_text)
        
def on_message_Light(client, userdata, msg): #1st possible bop
    timepassed = 0
    while timepassed < 80:
        value = mcp.read_adc(0)
        if(value < lowlight):
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

    client.message_callback_add("bopit/complete", on_message_Complete)
    client.message_callback_add("bopit/mic", on_message_Mic)
    client.message_callback_add("bopit/light", on_message_Light)
    client.loop_start()
    #setRGB(0,255,0)
    while True:
        #print("delete this line")
        time.sleep(1)
            

