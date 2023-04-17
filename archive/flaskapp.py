import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

#M#ESSAGE_LOG_FILE = 'message_log.txt'
MESSAGE_LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'message_log.txt')
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    with open(MESSAGE_LOG_FILE, 'a') as f:
        f.write(message + os.linesep)
    emit('broadcast_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)