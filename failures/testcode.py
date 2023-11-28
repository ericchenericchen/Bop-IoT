from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/switch')
def side():
    return render_template('side.html')

@socketio.on('message_from_client')
def handle_message(message):
    print('Received message:', message)
    socketio.emit('message_from_server', 'Message received!')

if __name__ == '__main__':
    socketio.run(app)