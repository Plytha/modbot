import os, sys
import requests
import json
from websocket_handler import Websocket_Handler
from jwt_token import Token
from constants import API_ENDPOINTS
import time
import asyncio
from websockets.asyncio.client import connect
from websockets.asyncio.server import serve

class Bot:

    def __init__(self, id_, secret):
        self.id_ = id_
        self.secret = secret
        self.sender_id = os.getenv("TWITCH_SELF_ID")
#         self.code = os.getenv("CODE")
        self.token = None

        self.websocket = Websocket_Handler()
        self.chat_websocket = Websocket_Handler()

        self.last_token_update = None

    def start_reading_chat(self):
        loop = asyncio.get_event_loop()

        loop.create_task(self.connect_to_chat_read())

        loop.run_forever()
        

    def handle_request(self, request_body, request_header, endpoint, post = True):
        """Send a request to given endpoint and return data as json"""

        request_URL = API_ENDPOINTS[endpoint]
        print(f"(II) Request url is {request_URL}")
        if post:
            rq = requests.post(request_URL, data=request_body, headers=request_header)
        else:
            rq = requests.get(request_URL, data=request_body, headers=request_header)
        
        if rq.ok:
            print("(II) OK Request")
            try:
                data_rx = json.loads(rq.content.decode('utf-8'))
                return data_rx
            except Exception as e:
                raise Exception(f"Request failed for reason: {e}")
                return
        else:
             raise Exception(f"Request returned with status code {rq.status_code} and content {rq.content}")  


    def get_new_token(self):
        print("(II) Getting new token")

        request_body = f"client_id={self.id_}&client_secret={self.secret}&grant_type=client_credentials"
        request_header = {"Content-Type": "application/x-www-form-urlencoded"}
        endpoint="GET_TOKEN"
        data = self.handle_request(request_body, request_header, endpoint)
    
        
        if not "access_token" in data.keys():
            print("Could not read a token in response")
            self.token = None
            return

        print("(II) Extracting token")
        self.token = data["access_token"]
        
        self.validate_token()
        
    def validate_token(self):
        """Validate the Token when required"""

        # Validate the token if it requires
        if (self.last_token_update is not None) \
        and (time.time() - self.last_token_update < 3600):
            return # no need to validate token
        
        if self.token is None:
            raise Exception("The bot has no token.")

        

        # Request for a token validation
        print("(II) Requesting validation")
        endpoint = "VALIDATE"
        request_header = {"Authorization": f"OAuth {self.token}"}
        request_body = ""
        self.handle_request(request_body, request_header, endpoint, post=False)
        
        # Update the validation time
        print("(II) Validation time updates")
        self.last_token_update = time.time()

    def validate_oauth(self):
        """Validate the Oauth when required"""

    
        # Request for a token validation
        print("(II) Requesting validation for Oauth")
        endpoint = "VALIDATE"
        request_header = {"Authorization": f"OAuth {os.getenv('TWITCH_IRC_TOKEN')}"}
        request_body = ""
        self.handle_request(request_body, request_header, endpoint, post=False)
        
                
    def debug_dump_token(self):
        if self.token is None:
            print("No token received SMH")
            return

        print(f"Received token {self.token}")

    async def print_msg(self):
        while True:
            message = await self.websocket.recv()
            if message == "PING :tmi.twitch.tv":
                print("Received ping, sending pong")
                await self.websocket.send("PONG :tmi.twitch.tv")
            else:
                print(f"Received message {message}")

    async def connect_to_chat_read(self):
        self.websocket = await connect("wss://irc-ws.chat.twitch.tv:443")
        await self.websocket.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
            

        reply = await self.websocket.recv()
        print(reply)
        #            self.validate_oauth()
        print(f"Attempt to connect with token {self.token} and nickname plyplybot")
        await self.websocket.send(f"PASS oauth:{os.getenv('TWITCH_IRC_TOKEN')}")
            
        await self.websocket.send("NICK plyplybot")

        asyncio.get_event_loop().create_task(self.print_msg())
            
        # Connect to the channel
        await self.websocket.send("JOIN #deplytha")
        """while True:
                message = await websocket.recv()
                if message == "PING :tmi.twitch.tv":
                    print("Received ping, sending pong")
                    await websocket.send("PONG :tmi.twitch.tv")
                else:
                    print(f"Received message {message}")"""

    def send_msg(self, msg, recipient_id=None):
        if recipient_id is None: # default test value
            recipient_id = os.getenv("TWITCH_CHANNEL_ID")
            
        print(f"(II) Sending message to channel with id {recipient_id}")
        # ensure token is valid
        self.validate_token()

        request_body = json.dumps({
            "broadcaster_id": f"{recipient_id}",
            "sender_id": f"{self.sender_id}",
            "message": f"{msg}"
        })
        request_header = {
            "Authorization": f"Bearer {self.token}",
            "Client-id": f"{self.id_}",
            "Content-Type": "application/json"
        }

        endpoint = "SEND_MESSAGE"

        print("(II) Request sent")
        self.handle_request(request_body, request_header, endpoint)
