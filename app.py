from flask import Flask, render_template, request, redirect, url_for, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import json
import os
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)



users = {}

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


try:
    with open("users.json", "r") as file:
        users = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    print("O arquivo users.json está vazio ou não contém um JSON válido.")

@app.route('/cadastro.html', methods=['GET', 'POST'])
def cadastro():
    error_message = None

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        dialogue_type = request.form.get('dialogue_type')

        if password != confirm_password:
            error_message = "As senhas não coincidem."
        else:
            if nickname in users:
                error_message = "Este nome de usuário já está em uso. Escolha outro."
            else:
                users[nickname] = {"password": password, "dialogue_type": dialogue_type}

                with open("users.json", "w") as file:
                    json.dump(users, file)

                return redirect(url_for('login'))

    return render_template('cadastro.html', error_message=error_message)


@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        nome = request.form.get('nickname')
        senha = request.form.get('password')

        print(nome)
        print(senha)
        
        if nome in users and users[nome]["password"] == senha:
            user = User(id=nome, password=users[nome]["password"], dialogue_type=users[nome]["dialogue_type"])            
            login_user(user)
            session["user"] = nome
            session["just_logged_in"] = True
            return redirect(url_for('index'))
        else:

            error_message = "Usuário ou senha incorretos"

    return render_template('login.html', error_message=error_message)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', endpoint='index')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    emit('message', f'Server received: {message}')



        


# Definição da classe User
class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    dialogue_type = db.Column(db.String(20), nullable=False)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/home", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

    app.config['DEBUG'] = True
    app.run(debug=True ,port=5000,use_reloader=False)
    socketio.run(app, debug=True)

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


if __name__ == '__main__':
    socketio.run(app, debug=True)