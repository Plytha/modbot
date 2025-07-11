import os, sys
import requests
import json
from websocket_handler import Websocket_Handler
from token_wrapper import Token
from constants import API_ENDPOINTS
import time
import asyncio
from websockets.asyncio.client import connect
from websockets.asyncio.server import serve
from irc_msg_handler import IRC_Handler

class Bot:

    def __init__(self, id_, secret):
        self.id_ = id_
        self.secret = secret
        self.sender_id = os.getenv("TWITCH_SELF_ID")
#         self.code = os.getenv("CODE")
        self.irc_token = Token(os.getenv("TWITCH_IRC_TOKEN"))
        self.websocket = None
        self.discord_websocket = None

        self.msg_handler = IRC_Handler("rules.json", "deplytha")
        

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


        
    def validate_token(self):
        """Validate the Token when required"""

        # Validate the token if it requires
        if self.irc_token.is_valid:
            return # no need to validate token
        
        #if self.token is None:
        #    raise Exception("The bot has no token.")
        

        # Request for a token validation
        print("(II) Requesting validation")
        endpoint = "VALIDATE"
        request_header = {"Authorization": f"OAuth {self.irc_token.token}"}
        request_body = ""
        self.handle_request(request_body, request_header, endpoint, post=False)

        self.irc_token.validate()

    async def forward_to_discord(self, message):
        """Discord websocket is write-only"""
        if self.discord_websocket is None:
            print("(II) No websocket for discord. Opening...")
            self.discord_websocket = await connect("ws://localhost:8765")
        print("(II) forwarded message to discord")
        await self.discord_websocket.send(message)

    async def cleanup(self):
        if self.discord_websocket is not None:
            await self.discord_websocket.close()
        await self.websocket.close()
        asyncio.get_event_loop().stop()
    
    async def irc_print_msg(self):
        while True:
            message = await self.websocket.recv()
            print(f"(II) GOT MESSAGE {message}")
            if message == "PING :tmi.twitch.tv":
                print("Received ping, sending pong")
                await self.websocket.send("PONG :tmi.twitch.tv")
            else:
                message_content = self.msg_handler.process(message)
                if message_content is not None:
                    print(f"Content: {message_content.content}")
                    if message_content.author == "deplytha" and \
                       message_content.content == "stop":
                        await self.cleanup()
                        return

                    if message_content.flagged:
                        await self.forward_to_discord(str(message_content))

                    
                    print(f"Received message {message}")

    async def irc_connect_to_chat_read(self):
        self.websocket = await connect("wss://irc-ws.chat.twitch.tv:443")
        self.validate_token()
        await self.websocket.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
            

        reply = await self.websocket.recv()
        print(reply)
        #            self.validate_oauth()
        # print(f"Attempt to connect with token {self.irc_token} and nickname plyplybot")
        await self.websocket.send(f"PASS oauth:{self.irc_token.token}")
            
        await self.websocket.send("NICK plyplybot")

        message = await self.websocket.recv()
        if not "Welcome, GLHF!" in message:
            raise RuntimeError(f"Could not connect to twitch.tv. Replied with {message}")

        asyncio.get_event_loop().create_task(self.irc_print_msg())
            
        # Connect to the channel
        await self.websocket.send("JOIN #deplytha")

