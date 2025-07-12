"""
Handler for messages received via irc websocket
"""

from irc_message import IRC_Message
import os
import json
from rule import Rule
import re

class IRC_Handler:

    def __init__(self, filename: str, channel_name: str):
        self.config_filename = filename
        self.channel_name = channel_name

        self.rules = []

        self.setup_rules()

    def setup_rules(self):
        if not os.path.exists(os.path.join("twitch/config", self.config_filename)):
            raise RuntimeError(f"File {os.path.join('twitch/config', self.config_filename)} does not exist.")
        with open(os.path.join("twitch/config", self.config_filename), "r") as f:
            data = json.load(f)

            rules = data["rules"]
            for rule in rules:
                name = rule["name"]
                matches_all = (rule["matches"] == "all")

                if "ordered" in rule.keys():
                    ordered = rule["ordered"]
                else:
                    ordered = False

                word_filters = [x.lower() for x in rule["filters"]["words"]]
                regex_filters = [re.compile(x) for x in rule["filters"]["regex"]]

                rule_object = Rule(name, 
                                   matches_all, 
                                   ordered,
                                   word_filters,
                                   regex_filters)
                self.rules.append(rule_object)

        
    def process(self, message: str):
        """Remove the headers from message and return its content"""
        if "PRIVMSG" in message:
            all_fields = message.split(";")
            for field in all_fields:
                if "display-name" in field:
                    author = field.split("=")[1]
            content = message.split(f"#{self.channel_name}")[-1]
            content = content.split(":", 1)[1].replace("\n","")

            res = self.check(content)

            return IRC_Message(author, content, res)
        return None

    def check(self, message: str) -> dict:
        """Apply the rules to a given message"""
        for rule in self.rules:
            if rule.check(message):
                print("(II) Rule matched")
                return rule.to_dict()

        return {"name": "placeholder", "flagged": False}
