from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import time
import random
import json
import requests

from flask import Flask, request, render_template
from flask_socketio import SocketIO

key = b'452diyhX782Qnkwe4OLbM6dFOvYERO9Jx0IEAotNweg='
f = Fernet(key)
prev = 1
score = 0
maingame = 0
max_score = 0
games = ["Repeat It", "Bop It", "Twist It", "UltrasonIT", "Mix It", "Dim It", "Shout It", "Wordle It"]
next_game = "Bop It"

PORT = 8000
app = Flask(__name__)
socketio = SocketIO(app, port=PORT)

#ROUTES
@app.route('/')
def home():
    return render_template('start.html')

@app.route('/play/start', methods=['GET'])
def start():
    global score
    global maingame
    global prev
    global next_game

    score = 0
    maingame = 0
    prev = 1
    next_game = "Bop It"

    client.publish("bopit/button")

    points = score
    event = "Bop It"
    return render_template('home.html', points=points, event=event)

@app.route('/play/success', methods=['GET'])
def success():
    global score
    global next_game

    points = score
    event = next_game
    status = "SUCCESS"

    return render_template('home.html', points=points, event=event, status = status)

@app.route('/play/failure', methods=['GET'])
def failure():
    global score
    global max_score
    global maingame 
    
    maingame = -1

    if score > max_score:
        max_score = score
    return render_template('end.html', score=score, max_score = max_score)

@app.route('/play/wordle', methods=['GET'])
def wordle():
    # guesses = 0

    link = "https://random-word-api.herokuapp.com/word?length=5"
    response = requests.get(link)
    if response.status_code == 200:
        answer = response.json()[0]
    else:
        print(response.status_code)
    
    # print("O means correct place, # means in word wrong place, X means not in word")
    # while guesses < 6:
    #     guess = input("guess a word") # this is where you would put in the HTML stuff Eric
    #     if WordleCheck(guess, answer):
    #         maingame = 0
    #         client.publish("bopit/complete")
    #     maingame = -1

    socketio.emit('generateword', {'word': answer}, namespace='/test')

    return render_template('wordle.html', target = answer)

#CALLBACKS
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("bopit/complete")
    client.subscribe("bopit/ultrasonicRanger")
    client.subscribe("bopit/potentiometer")
    client.subscribe("bopit/button")
    client.subscribe("bopit/led")
    client.subscribe("bopit/mic")
    client.subscribe("bopit/light")

    # NOT SURE IF WE WANT TO PUBLISH HERE, WE WANT GAME TO START ON START GAME BUTTON FROM FRONTEND
    # print("Bop It")
    # client.publish("bopit/button")

    #subscribe to the bop its

def on_message_Complete(client, userdata, msg):
    decrypt_text = f.decrypt(msg)
    text = str(decrypt_text, "utf-8")
    next = random.randint(0, 8)

    global next_game
    global score
    global prev

    if text == b"Passed":
        next_game = games[next]
        score += 1
        socketio.emit('success', namespace='/test')

        if next == 0:
            print(games[next])
            next = prev
            prev = -1
        if next == 1:
            if prev > 0:
                print(games[next])
            client.publish("bopit/button")
        if next == 2:
            if prev > 0:
                print(games[next])
            client.publish("bopit/potentiometer")
        if next == 3:
            if prev > 0:
                print(games[next])
            client.publish("bopit/ultrasonicRanger")
        if next == 4:
            if prev > 0:
                print(games[next])
            client.publish("bopit/led")
        if next == 5:
            if prev > 0:
                print(games[next])
            client.publish("bopit/light")
        if next == 6:
            if prev > 0:
                print(games[next])
            client.publish("bopit/mic")
        if next == 7:
            if prev > 0:
                print(games[next])
            maingame = 1
            socketio.emit('wordle', namespace='/test')
        
        prev = next

    else:
        maingame = -1
        socketio.emit('failure', namespace='/test')
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


#MAIN
if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.message_callback_add("bopit/complete", on_message_Complete)
    
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)
    client.loop_start()

    socketio.run(app, port=PORT) #start the flask server, blocks out to listen for flask requests (CAN'T WHILE LOOP)

    # while True:
    #     if maingame == -1:
    #         start = input("enter s to restart")
    #         if start == "s":
    #             score = 0
    #             maingame = 0
    #             prev = 1
    #             print("Bop It")
    #             client.publish("bopit/button")
    #     if maingame == 1:
    #         guesses = 0
    #         link = "https://random-word-api.herokuapp.com/word?length=5"
    #         response = requests.get(link)
    #         if response.status_code == 200:
    #             answer = response.json()[0]
    #         print("O means correct place, # means in word wrong place, X means not in word")
    #         while guesses < 6:
    #             guess = input("guess a word") # this is where you would put in the HTML stuff Eric
    #             if WordleCheck(guess, answer):
    #                 print("Correct!") #this is completely pointless and can be removed
    #                 maingame = 0
    #                 client.publish("bopit/complete")
    #     time.sleep(1)     
        
           