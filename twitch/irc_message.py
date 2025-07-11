"""
Wrapper for irc messages
"""

import datetime

class IRC_Message:

    def __init__(self, author: str, content: str, analysis: dict):
        self.author = author
        self.content = content
        self.analysis = analysis

    @property
    def flagged(self):
        return self.analysis["flagged"]
        

    def __str__(self):
        return f"[{datetime.datetime.now()} | {self.author}]: {self.content} (broke rule {self.analysis['name']})"
