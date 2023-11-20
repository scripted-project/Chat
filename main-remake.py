from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random, datetime, sqlite3
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "3789486422468452213841556468465462132484878"
socketio = SocketIO(app)

rooms = {}  # unused
houses = {}
users = {} 

housesConnection = sqlite3.connect("data/houses.db")
housesCrsr = housesConnection.cursor()

usersConnection = sqlite3.connect("data/users.db")
usersCrsr = usersConnection.cursor()

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]



def GenerateUniqueCode(Length, type):
    if type == "ascii":
        while True:
            code = ""
            for _ in range(Length):
                code += random.choice(ascii_uppercase)
            if code in houses:
                break
    if type == "number":
        while True:
            code = ""
            for _ in range(Length):
                code += random.choice(numbers)
            if code in users: # This needs to be fixed
                break
        
    return code

def CreateHouse(name, owner):
    houses[name] = {
        "owner": owner,
        "rooms": {}
        
    }
    houses[name]["rooms"]["main"] = {"messages": []}

def serverStart():
    
    usersCrsr.execute('''SELECT * FROM users''')
    output = usersCrsr.fetchall()
    CreateHouse("orgin", "Jewels")

serverStart()
@app.route("/", methods=["POST", "GET"])
def home():
    if session["account"] in users:
        session["account"] = users["{username}"]
        session["houses"] = users["{username}"]["houses"]
        session["room"] = houses["orgin"]["rooms"]["main"]
        
        return redirect(url_for("room"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login = request.form.get("login")
        signup = request.form.get("sign-up")
        
        if not username:
            return render_template("home.html", error="Enter your username.", password=password, username=username)
        if not password:
            return render_template("home.html", error="Enter your password.", password=password, username=username)
        
        if login != False:
            if username in users:
                if password == users["{username}"]["password"]:
                    session["account"] = users["{username}"]
                    session["houses"] = users["{username}"]["houses"]
                    session["room"] = houses["orgin"]["main"]
                    session["house"] = houses["orgin"]
                    return redirect(url_for("room"))
                else:
                    return render_template("home.html", error="Incorrect password", password=password, username=username)
            else:
                return render_template("home.html", error="User does not exist", password=password, username=username)
        if signup != False:
            # Use datetime
            users["{username}"] = {
                "password": "{password}",
                "id": GenerateUniqueCode(6, "number"),
                "houses": ["orgin"],
                "date-joined": "",
                "last-online": "",
                "roles":["user"],
                "online": True
            }
            
    return redirect(url_for("room"))

@app.route("/room")
def room():
    room = session.get("room")
    return render_template("room.html", room=session.get("room"), house=session.get("house"), messages=houses[session.get("house")][session.get("room")]["messages"])


if __name__  == "__main__":
    socketio.run(app)
    #socketio.run(app, host="0.0.0.0", port=5000)
    #socketio.run(app, allow_unsafe_werkzeug=True)
    
housesConnection.close()
usersConnection.close()