from tools import Generator, Colors, Cryptor, printCC, success, error

g = Generator()
color = Colors()
cy = Cryptor()

class API():
    def __init__(self):
        printCC(f"{color.blue}API Initialized{color.end}")
        self.PRIVATE_API_KEY = g.key("private", 2048, 1)
        printCC(f"{color.green}PRIVATE_API_KEY Created{color.end}")
        self.PUBLIC_API_KEY = g.key("public", 32, 1)
        printCC(f"{color.green}PUBLIC_API_KEY Created: {color.end}{color.blue}{self.PUBLIC_API_KEY}{color.end}")
        self.SELF_RSA_PRIVATE, self.SELF_RSA_PUBLIC = g.keypair()
        printCC(f"{color.green}SELF_RSA_PRIVATE && SELF_RSA_PUBLIC created{color.end}")
        self.auths = {}
        printCC(f"{color.green}Auths dict created{color.end}")
        # use two way RSA 
        # Client Key + Server Key
    def new(self, account):
        if not account.get("name"):
            request = {"type": "newc", "account": None}
            response = {"code": 404, "description": "No Account Entered", "data": {"public": None, "private": None}}
            printCC(error(request, response))
            return response
        key1, key2 = g.keypair()
        self.auths[account["name"]] = {"key": key2}
        request = {"type": "new", "account": account}
        response = {"code": 200, "description": "OK", "data": {"public": key2, "private": key1}}
        printCC(success(request, response))
        return key1

a = API()
account = {
    "name": "cool"
}

printCC("oh look somone joineded")
a.new(account)