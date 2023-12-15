from tools import printCC, Colors, success, error

c = Colors()
request = {
    "path": "./sdj",
    "type": "get"
}
response = {
"data": "W",
"code": 200,
"description": "Returned data."
}

printCC(c.blue + "Hello World!" + c.end)
printCC(f"{c.blue}Hello World!{c.end}")
printCC("Hello World!")

print(success(request, response))
printCC(success(request, response))

print(error(request, response))
printCC(error(request, response))