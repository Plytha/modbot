"""
Handler for messages received via irc websocket
"""

from irc_message import IRC_Message
import json


class IRC_Handler:

    def __init__(self, filename: str, channel_name: str):
        self.config_filename = filename
        self.channel_name = channel_name

        self.rules = []

        self.setup_rules()

    def setup_rules(self):
        with open(f"twitch/config/{self.config_filename}", "r") as f:
            data = json.load(f)

            print(data)
            raise RuntimeError("Not implemented yet")
        
    def process(self, message: str):
        """Remove the headers from message and return its content"""
        if "PRIVMSG" in message:
            all_fields = message.split(";")
            for field in all_fields:
                if "display-name" in field:
                    author = field.split("=")[1]
            content = message.split(f"#{self.channel_name}")[-1]
            content = content.split(":", 1)[1]

            res = self.check(content)

            return IRC_Message(author, content, res)
        return None

    def check(self, message: str) -> dict:
        """Apply the rules to a given message"""
        for rule in self.rules:
            if rule.check(message):
                return rule.to_dict()

        return {"name": "placeholder", "flagged": False}
