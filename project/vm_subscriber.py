from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import time
import random
import json
import requests
key = b'452diyhX782Qnkwe4OLbM6dFOvYERO9Jx0IEAotNweg='
f = Fernet(key)
prev = 1
score = 0
maingame = 0
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("bopit/complete")
    client.subscribe("bopit/ultrasonicRanger")
    client.subscribe("bopit/potentiometer")
    client.subscribe("bopit/button")
    client.subscribe("bopit/led")
    client.subscribe("bopit/mic")
    client.subscribe("bopit/light")
    print("Bop It")
    client.publish("bopit/button")
    #subscribe to the bop its
def on_message_Complete(client, userdata, msg):
    decrypt_text = f.decrypt(msg)
    text = str(decrypt_text, "utf-8")
    next = random.randint(0, 8)
    if text == b"Passed":
        score += 1
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
        if next == 7:
            if prev > 0:
                print("Wordle It")
            maingame = 1 # idk why this is greyed out it should be fine it is global
    else:
        maingame = -1
        print("Couldn't keep up")
            
def WordleCheck(guess, answer):
    compare = ""
    for i in range(0,5):
        max = 0
        for j in range(0,5):
            if guess[i] == answer[j] and i == j:
                max = 3
            elif guess[i] == answer[j] and max < 3:
                max = 2
            elif max < 2:
                max = 1
        if max == 3:
            compare += "O"
        elif max == 2:
            compare += "#"
        elif max == 1:
            compare += "X"
    print(compare)
    if compare == "OOOOO":
        return True
    return False
            
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
        if maingame == -1:
            start = input("enter s to restart")
            if start == "s":
                score = 0
                maingame = 0
                prev = 1
                print("Bop It")
                client.publish("bopit/button")
        if maingame == 1:
            guesses = 0
            link = "https://random-word-api.herokuapp.com/word?length=5"
            response = requests.get(link)
            if response.status_code == 200:
                answer = response.json()[0]
            print("O means correct place, # means in word wrong place, X means not in word")
            while guesses < 6:
                guess = input("guess a word") # this is where you would put in the HTML stuff Eric
                if WordleCheck(guess, answer):
                    print("Correct!") #this is completely pointless and can be removed
                    maingame = 0
                    client.publish("bopit/complete")
        time.sleep(1)     
        
           