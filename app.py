from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfsdhsdhsgfhsfsfgjsfkdh'
socketio = SocketIO(app)

users = set()  # Множество для хранения никнеймов

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('set_username')
def set_username(username):
    if username in users:
        emit('username_error', 'Этот никнейм уже занят. Пожалуйста, выберите другой.', broadcast=False)
    else:
        users.add(username)
        emit('username_success', username, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    msg = data['message']
    print(f'Message from {username}: {msg}')
    emit('message', {'username': username, 'message': msg}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use PORT from environment or default to 10000
    socketio.run(app, host='0.0.0.0', port=port)
