from ast import Dict
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random, datetime, sqlite3, json
from string import ascii_lowercase, ascii_uppercase
# python main-remake.py

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
            json.dump(data, file, indent=4)
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
            print(id)
            for user in data["users"]:
                if data["users"][user]["id"] == id:
                    isthere = True
            if isthere == True:
                break
            
            return id
#class Watcher():
 #   pf = ProfanityFilter()
#    def passthrough(msg: str):
#        profs = pf.get_profane_words(msg)
#        returned = msg
 #       for word in profs:
 #           isSlur = pf.is_slur(word)
 #           
  #          if isSlur:
 #               returned = returned.replace(word, '*' * len(word))
 #           else:
 #               returned = returned.replace(word, word[0] + '*' * (len(word) - 1))
 #       return returned

data: dict = readJSON("data.json")
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
                "password": password,
                "role": "user"
            }
            print(f"Created account {username}: {password}")
        
        if username not in data["users"] or data["users"][username]["password"] != password:
            return render_template("home.html", error="Incorrect user info.", username=username, password=password)
                
        
        session["username"] = username
        session["password"] = password
        session["house"] = "orgin"
        session["room"] = "main"
        session["loggedin"] = True
        print(f"User {username} has logged in.")
        saveJSON("data.json", data)
        print(f"{username} redirected to \"room\"")
        return redirect(url_for("room"))
    
    return render_template("home.html")

@app.route("/app", methods=["POST", "GET"])
def room():
    if session.get("loggedin") != True:
        print(f"User not logged in")
        return redirect(url_for("home"))
    try:
        print(f"{session.get("username")} now in room {session.get("house")}: {session.get("room")}")
    except:
        print(f"User not logged in")
        return redirect(url_for("home"))
    return render_template("room.html", house=session.get("house"), room=session.get("room"), username=session.get("username"), state="active", msgs=data["houses"][session.get("house")]["rooms"][session.get("room")]["messages"])

@socketio.on("data")
def message(Data):
    room = session.get("room")
    time = Data.get("time")
    message = Data.get("data")
    print(f"[*] {session.get('username')}: {message} ({time})")
    content = {
        "name": session.get("username"),
        "message": message,
        "time": time
    }
    send(content, to=room)
    data["houses"][session.get("house")]["rooms"][session.get("room")]["messages"].append(f"{session.get('username')}: {message} ({time})")
    saveJSON("data.json", data)

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("username")
    join_room(room)
    
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("username")
    join_room(room)

if __name__ == "__main__":
    socketio.run(app)