"""
Wrapper for irc messages
"""

import datetime

class IRC_Message:

    def __init__(self, author: str, content: str):
        self.author = author
        self.content = content


    def __str__(self):
        return f"[{datetime.datetime.now()} | {self.author}]: {self.content}"