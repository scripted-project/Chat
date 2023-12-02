from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random, datetime, sqlite3, json
from string import ascii_lowercase, ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "830156"
socketio = SocketIO(app)

def readJSON(path):
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
    def id(len):
        while True:
            id = ""
            for _ in range(len):
                id += random.randint(1, 9)
            if id in data["users"]:
                break
        
        return id
class Watcher():
    def watch(censor: list):
        pass
    def censor():
        pass

data = readJSON("./data.json")
cookies = {}

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login = request.form.get("login", False)
        signup = request.form.get("signup", False)
        
        if username and password != None:
            if login != False:
                isthere = False
                for user in data["users"]:
                    if username == user["name"]:
                        isthere = False
                        break
                    else:
                        continue
                if isthere == True:
                    redirect(url_for("app"))
                else:
                    pass
            elif signup != False:
                pass

if __name__ == "__main__":
    socketio.run(app)