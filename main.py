from ast import Dict
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
from flask_socketio import join_room, leave_room, send, SocketIO
import random, datetime, sqlite3, json
from string import ascii_lowercase 
from better_profanity import profanity 
# python main-remake.py

app = Flask(__name__) #, template_folder='templates'
app.config["SECRET_KEY"] = "830156"
socketio = SocketIO(app, cors_allowed_origins="*")


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
class Watcher():
    def passthrough(self, msg: str):
        return profanity.censor(msg, '*')      
class API():
    token = "SChatauth4" # !TO-DO!: 1: class room inside house() 2: move get msgs into room()
    def getMessages(self, auth, house, room):
        
        if auth != self.token:
            abort(401, description="Unathorized - Incorrect Key")

        if not house or not room or not auth:
            abort(400, description="'house', 'room', and 'auth' parameters are required.")

        if house not in data["houses"] or room not in data["houses"][house]["rooms"]:
            abort(404, description="House or room not found.")

        return jsonify(data["houses"][house]["rooms"][room]["messages"])
    def getUser(self, auth, user):
        if auth != self.token:
            abort(401, description="Unathorized - Incorrect Key")

        if not auth or not user:
            abort(400, description="'auth' and 'user' parameters are required.")

        if user not in data["users"]:
            abort(404, description="User not found.")
            
        return jsonify(data["users"][user]) 
    class user():
        def __init__(self, name, auth):
            self.name = name
        def houses(self):
            return jsonify(data["users"][self.name]["houses"])
    class house():
        def __init__(self, auth, house):
            self.house = house
        def rooms(self):
            return jsonify(data["houses"][self.house]["rooms"])
class AI():
    def __init__(self):
        pass

ai = AI()
data: dict = readJSON("data.json")
cookies = {}
gen = Generator()
w = Watcher()
api = API()

# pages
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
            username = w.passthrough(username)
            if username in data["users"]:
                return render_template("home.html", error="Username is in use.", username=username, password=password)
            data["users"][username] = {
                "id": gen.id(4),
                "password": password,
                "role": "user",
                "houses": ["orgin"]
            }
            print(f"Created account {username}: {password}")
            data["houses"]["orgin"]["users"].append(username)

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
        print(f"{session.get('username')} now in room {session.get('house')}: {session.get('room')}")
    except:
        print(f"User not logged in")
        return redirect(url_for("home"))
    data["houses"][session.get("house")]["rooms"][session.get("room")]["members"].append(session.get("username"))
    return render_template("room.html", house=session.get("house"), room=session.get("room"), username=session.get("username"), state="active", data=data)

@app.route("/create/room", methods=["POST", "GET"])
def createRoom():
    if session.get("loggedin") != True:
        return render_template(url_for("home"))
    
    return render_template("create-room.html")

@app.route("/create/house", methods=["POST", "GET"])
def createHouse():
    if session.get("loggedin") != True:
        return render_template(url_for("home"))
    
    return render_template("create.html")

# sockets
@socketio.on("data")
def message(Data):
    room = session.get("room")
    time = Data.get("time")
    message = Data.get("data")
    role = data["users"][session.get("username")]["role"]
    message = w.passthrough(message)
    print(f"[*] {session.get('username')}: {message} ({time})")
    content = {
        "name": session.get("username"),
        "message": message,
        "time": time,
        "role": role
    }
    send(content, to=room)
    data["houses"][session.get("house")]["rooms"][session.get("room")]["messages"].append(content)
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

# API (private)
@app.route("/api/msgs", methods=["GET"])
def returnMSGS():
    house = request.args.get('house')
    room = request.args.get('room')
    auth = request.args.get('auth')
    
    return api.getMessages(auth, house, room)

@app.route("/api/user", methods=["GET"])
def returnUSER():
    user = request.args.get('user')
    auth = request.args.get('auth')
    
    return api.getUser(auth, user)

@app.route("/api/roms", methods=["GET"])
def returnROMS():
    auth = request.args.get('auth')
    house = request.args.get('auth')
    
    return api.house(auth, house).rooms()

# API (public)
@app.route("/api/public", methods=["GET"])
def apiConnection():
    return "Connected"
# Later add API keys

if __name__  == "__main__":
    socketio.run(app)
    #port = int(os.environ.get("PORT", 5000))
    #socketio.run(app, host="0.0.0.0", port=port)
    #socketio.run(app, allow_unsafe_werkzeug=True)
