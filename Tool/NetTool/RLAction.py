import json
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

G_server = ""
G_token = ""

class RLAction:
    def __init__(self):
        self.actionURL = ""
        self.port = 443
        self.timeout = 60
        self.headers =  {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
    def post(self,data=None):
        pass
    def get(self,data=None):
        pass

