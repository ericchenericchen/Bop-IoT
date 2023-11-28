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
max_score = 0
games = ["Repeat It", "Bop It", "Twist It", "UltrasonIT", "Mix It", "Dim It", "Shout It", "Wordle It"]
next_game = "Bop It"
flag = 1

PORT = 8000
app = Flask(__name__)
socketio = SocketIO(app, port=PORT, engineio_logger=True, logger=True)

#ROUTES
@app.route('/')
def home():
    return render_template('start.html')

@app.route('/play/start')
def start():
    global score
    global prev
    global next_game

    score = 0
    prev = 1
    next_game = "Bop It"

    client.publish("bopit/button")

    points = score
    event = "Bop It"

    print("STARTED GAME!")
    
    return render_template('home.html', points=points, event=event)

@app.route('/play/success')
def success():
    global score
    global next_game

    points = score
    event = next_game
    status = "SUCCESS"

    if event == "Wordle It":
        client.publish("bopit/button")
        points = score + 1
        event = "Bop It"
    
    return render_template('home.html', points=points, event=event, status = status)

@app.route('/play/failure')
def failure():
    global score
    global max_score
    
    if score > max_score:
        max_score = score
    return render_template('end.html', score=score, max_score = max_score)

@app.route('/play/wordle')
def wordle():
    return render_template('wordle.html')

# Testing socketio works correctly!
#
# @socketio.on('test')
# def test():
#     socketio.emit('wordle')

@socketio.on('giveword')
def handle_wordle():
    link = "https://random-word-api.herokuapp.com/word?length=5"
    response = requests.get(link)
    if response.status_code == 200:
        answer = response.json()[0].upper()
    else:
        answer = response.status_code

    socketio.emit('generateword', {'word': answer})
    return

@socketio.on('endwhile')
def handle_success():
    global flag
    flag = 0
    return

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
    #subscribe to the bop its

def on_message_Complete(client, userdata, msg):
    decrypt_text = f.decrypt(msg.payload)
    text = str(decrypt_text, "utf-8")
    next = random.randint(0, 7)

    global next_game
    global score
    global prev
    global flag

    if text == "Passed":
        next_game = games[next]
        score += 1

        if next_game != "Wordle It":
            socketio.emit('success')
            while(flag):
                pass
            flag = 1
        
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
            socketio.emit('wordle')
        
        prev = next
    else:
        print(text)
        socketio.emit('failure')
        #print("Couldn't keep up")
            
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

    socketio.run(app, port=PORT, debug=True) #start the flask server, blocks out to listen for flask requests (CAN'T WHILE LOOP)