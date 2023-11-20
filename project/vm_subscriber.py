"""Run vm_subscriber.py in a separate terminal on your VM."""

from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import time
import random

key = b'452diyhX782Qnkwe4OLbM6dFOvYERO9Jx0IEAotNweg='
f = Fernet(key)
prev = random.randint(0, 7)

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("bopit/complete")
    client.subscribe("bopit/ultrasonicRanger")
    client.subscribe("bopit/potentiometer")
    client.subscribe("bopit/button")
    client.subscribe("bopit/led")
    client.subscribe("bopit/mic")
    client.subscribe("bopit/light")
    #subscribe to the bop its
def on_message_Complete(client, userdata, msg):
    decrypt_text = f.decrypt(msg)
    text = str(msg.payload, "utf-8")
    next = random.randint(0, 7)
    if text == b"Passed":
        if next == 0:
            next = prev
            prev = -1
            print("Repeat It")
        if next == 1:
            if prev > 0:
                print("Bop It")
            client.publish("bopit/button")
        if next == 2:
            if prev > 0:
                print("Twist It")
            client.publish("bopit/potentiometer")
        if next == 3:
            if prev > 0:
                print("UltrasonIT")
            client.publish("bopit/ultrasonicRanger")
        if next == 4:
            if prev > 0:
                print("Mix It")
            client.publish("bopit/led")
        if next == 5:
            if prev > 0:
                print("Dim It")
            client.publish("bopit/light")
        if next == 6:
            if prev > 0:
                print("Shout It")
            client.publish("bopit/mic")
            
        
            
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    pass

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.message_callback_add("bopit/complete", on_message_Complete)
    
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(1)        