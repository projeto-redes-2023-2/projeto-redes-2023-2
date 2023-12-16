from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/room')
def room():
    return render_template('room.html')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    emit('message', f'Server received: {message}')

if __name__ == 'main':
    app.config['DEBUG'] = True
    socketio.run(app, debug=True)