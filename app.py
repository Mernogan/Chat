from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

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
    socketio.run(app)