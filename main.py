from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random, datetime, os
from string import ascii_uppercase, ascii_lowercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "3789"
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

def GenerateUniqueCode(Length):
    while True:
        code = ""
        for _ in range(Length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
        
    return code

@app.route("/", methods=["POST", "GET"])
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
            room = GenerateUniqueCode(4)
            print(f"Created room: {room}")
            rooms[room] = {"members": 0, "messages": []}
            print(rooms)
        elif code not in rooms:
            return render_template("home.html", error=f"Room: {room} does not exist.", code=code, name=name)
        
        session["room"] = room
        session["room"] = name
        return redirect(url_for("room"))
    
    return render_template("home.html")

@app.route("/room", methods=["POST", "GET"])
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    
    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("data")
def message(data):
    time = data.get("time")
    messageContent = data.get("data")
    print(f"[*] {session.get('name')}: {data['data']} ({time})")
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name": session.get("name"),
        "message": messageContent,
        "time": time
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    
    

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
    send({"token": "[+] ", "name": name, "message": "has connected"}, to=room)
    rooms[room]["members"] += 1
    print(f"[+] {name} connected to {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
            # print(f"{rooms[room]} has been deleted.") This errors and I'm not sure why
    
    send({"token": "[-] ", "name": name, "message": "has disconnected"}, to=room)
    print(f"[-] {name} has disconnected from {room}")



if __name__  == "__main__":
    #socketio.run(app)
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
    #socketio.run(app, allow_unsafe_werkzeug=True)
    