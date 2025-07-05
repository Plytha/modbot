"""
Handler for messages received via irc websocket
"""

from irc_message import IRC_Message

class IRC_Handler:

    def __init__(self, filename: str, channel_name: str):
        self.config_filename = filename
        self.channel_name = channel_name

    def process(self, message: str):
        """Remove the headers from message and return its content"""
        if "PRIVMSG" in message:
            all_fields = message.split(";")
            for field in all_fields:
                if "display-name" in field:
                    author = field.split("=")[1]
            content = message.split(f"#{self.channel_name}")[-1]
            content = "".join([x for x in content.split(":")[1:]])

            return IRC_Message(author, content)
        return None

    def check(self, message: str):
        """Apply the rules to a given message"""