import flask
import json, secrets, os, string, random, time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

"""
Text Color:

Black: \033[30m
Red: \033[31m
Green: \033[32m
Yellow: \033[33m
Blue: \033[34m
Magenta: \033[35m
Cyan: \033[36m
White: \033[37m

Background Color:

Black: \033[40m
Red: \033[41m
Green: \033[42m
Yellow: \033[43m
Blue: \033[44m
Magenta: \033[45m
Cyan: \033[46m
White: \033[47m

Text Attributes:

Reset all attributes: \033[0m
Bold: \033[1m
Italic: \033[3m
Underline: \033[4m
Blink (slow): \033[5m
Blink (fast): \033[6m
Reverse video: \033[7m

Cursor Control:

Move cursor to beginning of line: \033[0G or \033[G
Move cursor to specified position (row, column): \033[<row>;<column>H
Save cursor position: \033[s
Restore cursor position: \033[u
Hide cursor: \033[?25l
Show cursor: \033?25h

Clear Screen:

Clear screen from cursor down: \033[0J
Clear screen from cursor up: \033[1J
Clear entire screen: \033[2J
Clear line from cursor right: \033[0K
Clear line from cursor left: \033[1K
Clear entire line: \033[2K"""


def save(filepath: str, type: str, data, cc=False) -> dict:
    """
    docstring
    """ # TODO: Finish docstring for save()
    if type == "json":
        if os.path.exists(filepath):
            try:
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=4)
                request = {
                    "path": filepath,
                    "type": type
                    }
                response = {
                    "data": None,
                    "code": 200,
                    "description": "Saved data."
                    }
                if cc == True:
                    printCC(success(request, response))
                return request, response
            except Exception as e:
                print(e)
        else:
            request = {
                "path": filepath,
                "type": type
                }
            response = {
                "data": None,
                "code": 404,
                "description": "File not found."
                }
            print(error(request, response))
            return request, response       
def get(filepath: str, type: str, cc=False) -> dict:
    """
    REMEMBER: To unpack only 1 var, use: `_, var` or `var, _`
    
    Returns:
    - `request` 
        - `path`: Path from args
        - `type`: Type from args
    - `response`
        - `data`: Data returned by function
        - `code`: Success/Error code
        - `description`: Success/Error description
    - Also prints some logging things
    """ #TODO: Finish docstring for get()
    if type == "json":
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    jsonData = json.load(f)
                request = {
                    "path": filepath,
                    "type": type
                    }
                response = {
                    "data": jsonData,
                    "code": 200,
                    "description": "Returned data."
                    }
                if cc == True:
                    printCC(success(request, response))
                else: 
                    print(success(request, response))
                return request, response
            except Exception as e:
                print(e)
        else:
            request = {
                "path": filepath,
                "type": type
                }
            response = {
                "data": None,
                "code": 404,
                "description": "File not found."
                }
            print(error(request, response))
            return request, response
def printCC(text, delay=0.05, colors=True):
    buffer = ""
    #TODO: add cc color support
    for char in text:
        print(char, end='', flush=True)
        buffer = buffer + char
        #if colorList in buffer:
        #    
        time.sleep(delay)
    print()
def error(request: dict, response: dict):
    return f"{c.red}Request: {c.end}{c.purple}{request['type']}: {request['path']} {c.end} -> {c.red}Response: {c.end}{c.purple}{response['code']}: {response['description']}{c.end}"
def success(request: dict, response: dict): 
    if request.get("type") == "newc":
        return f"{c.green}Request: {c.end}{c.blue}{request['type']}: {request['account']} {c.end} -> {c.green}Response: {c.end}{c.cyan}{response['code']}: {response['description']}{c.end}"
    elif request.get("type") == "file": 
        return f"{c.green}Request: {c.end}{c.blue}{request['type']}: {request['path']} {c.end} -> {c.green}Response: {c.end}{c.cyan}{response['code']}: {response['description']}{c.end}"
def highlightChar(target: list, text: str, color): 
    # TODO: Fix highlightChar()
    # TODO: Add docstring for highlightChar()
    if color not in colorList:
        return None
    data = []
    for char in text:
        if char in target:
            data.append(f"{color}{char}{c.end}")
        else:
            data.append(f"char")
    return f''.join(map(str, data))
class Colors():
    """
    Generates Colors
    """
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    purple = "\033[35m"
    cyan = "\033[36m"
    end = "\033[0m" #orginal
class Generator():
    def key(self, method: str, length: int, depth: int):
        if method == "private":
            key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
            return key
        if method == "public":
            keylist = []
            for _ in range(length):
                keylist.append(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))
            key = ''.join(map(str, keylist))
            return key
    def keypair(self):
        privateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        publicKey = privateKey.public_key()
        return privateKey, publicKey
class Cryptor():
    class RSA():
        def encrypt(self, public, ptext):
            ctext = public.encrypt(
                ptext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return ctext
        def decrypt(self, private, ctext):
            ptext = private.decrypt(
                ctext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return ptext
class Screen():
    def clear(self, type):
        if type == "screen":
            if os.name == 'posix':
                os.system('clear')
            elif os.name == 'nt':
                os.system('cls')
        if type == "line":
            print("\033[2K")

config = {"debug": False}
c = Colors()
colorList = [c.red, c.green, c.yellow, c.blue, c.purple, c.cyan, c.end]
cy = Cryptor()
cy.rsa = cy.RSA()
g = Generator()
s = Screen()

#* Tests
if config["debug"] == True:
    private, public = g.keypair()
    pt = b"Plaintext"
    ct = cy.rsa.encrypt(public, pt)
    dt = cy.rsa.decrypt(private, ct)

    while True:
        s.clear("screen")
        print("Menu")
        print("[A] Encryption Tests")
        print("[B] Get/Save Tests")
        print("[C] Generator Tests")
        print("[D] CC Test")
        print("[E] End")
        userInput = input("Choice: ")
        if userInput.lower() == "a":
            s.clear("screen")
            print(f"{c.yellow}{pt}{c.end}\n{'*' * 50}")
            print(f"{c.cyan}{ct}{c.end}\n{'*' * 50}")
            print(f"{c.yellow}{dt}{c.end}\n{'*' * 50}")
            userInput = input("Press any key and Enter")
        elif userInput.lower() == "b":
            s.clear("screen")
            reqG, resG = get("test.json", "json", cc=True)
            reqS, resS = save("test.json", "json", resG["data"], cc=True)
            print(reqG, resG)
            print(reqS, resS)
            reqG2, resG2 = get("tet.json", "json", cc=True)
            reqS2, resS2 = save("tet.json", "json", resG2["data"], cc=True)
            print(reqG2, resG2)
            print(reqS2, resS2)
            userInput = input("Press Enter")
        elif userInput.lower() == "c":
            print(f"{c.purple}{g.key('private', 2048, 1)}{c.end}")
            userInput = input("Press any key and Enter")
        elif userInput.lower() == "d":
            s.clear("screen")
            printCC("Hello world! This is text.")
            printCC(f"{c.blue}Hello World!{c.end}", 0.75)
            userInput = input("Press any key and Enter")
        elif userInput.lower() == "e":
            s.clear("screen")
            break
 