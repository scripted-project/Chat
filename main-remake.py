from ast import Dict
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random, datetime, sqlite3, json
from string import ascii_lowercase, ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "830156"
socketio = SocketIO(app)

def readJSON(path) -> dict or None:
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
def saveJSON(path, data):
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
    except FileNotFoundError:
        return None
class Generator():
    def code(len):
        while True:
            code = ""
            for _ in range(len):
                code += random.choice(ascii_lowercase)
            if code in data["houses"]:
                break
        return code
    def id(self, len):
        while True:
            id: int = 0
            isthere: bool = False
            for _ in range(len):
                id += random.randint(1, 9)
            for user in data["users"]:
                if data[user]["id"] == id:
                    isthere = True
            if isthere == True:
                break
            
            return id
class Watcher():
    def watch(censor: list):
        pass
    def censor():
        pass

data: dict = readJSON("./data.json")
cookies = {}
gen = Generator()

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login = request.form.get("login", False)
        signup = request.form.get("signup", False)
        
        if not username or not password:
            return render_template("home.html", error="Enter all info.", username=username, password=password)

        if signup != False:
            if username in data["users"]:
                return render_template("home.html", error="Username is in use.", username=username, password=password)
            data["users"][username] = {
                "id": gen.id(4),
                "password": password
            }
            print(f"Created account {username}: {password}")
        
        if username not in data["users"] or data["users"][username]["password"] != password:
            return render_template("home.html", error="Incorrect user info.", username=username, password=password)
                
        
        session["username"] = username
        session["password"] = password
        saveJSON("data.json", data)
        return redirect(url_for("room"))
    
    return render_template("home.html")

@app.route("/app")
def room():
    return render_template("room.html")

if __name__ == "__main__":
    socketio.run(app)