from flask import Flask
from flask import send_from_directory, request
from flask import render_template
from flask_socketio import SocketIO
import webbrowser

score = 0
max_score = 0
points = 0
PORT = 8000
app = Flask(__name__)
socketio = SocketIO(app)

# LIST OF OBJECTIVES:
#     retrieve points, event; store to use later
#     when the button navigates to start, we want to start vm_subscriber?
#     when subscriber posts success/fail, we want it to display
#     when wordle game starts, we want it to display
#     when flappy bird game starts, we want it to display

#     Answers:
    # What if we make frontend.py a separate node.
    # Then, we make vm_subscriber publish, and have frontend.py subscribe to vm_subscriber
    # - publish what?
    #     - points
    #     - game name
    #     - win/lose


    #ANSWER 1:
    # how do we restart? we publish to bopit/button

@app.route('/')
def home():
    return render_template('start.html')

@app.route('/play/start')
def start():
    ##UPDATE POINTS
    #UPDATE EVENT 
    points = 0
    event = ""
    return render_template('home.html', points=points, event=event)

@app.route('/play/success')
def success():
    global points

    points += 1
    event = ""
    status = "SUCCESS" 
    return render_template('home.html', points=points, event=event, status=status)

@app.route('/play/failure')
def failure():
    #STORE THE CURRENT SCORE VALUE, COMPARE TO MAX SCORE, IF HIGHER, UPDATE
    global score
    global max_score
    score += 1
    if score > max_score:
        max_score = score
    return render_template('end.html', score=score, max_score = max_score)

@app.post('/wordle')
def wordle():
    return

@app.post('/flappy')
def flappy():
    return

if __name__ == '__main__':
    socketio.run(app, debug=True)