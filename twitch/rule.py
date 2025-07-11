"""
Class to instantiate rules from the json file
"""
import re

class Rule:

    def __init__(self,
                 name: str,
                 match_all: bool,
                 is_ordered: bool,
                 words_filters: list[str],
                 regex_filters = None):
        
        self.name = name
        self.match_all = match_all
        self.is_ordered = is_ordered
        self.words_filters = words_filters
        self.check_words = (len(self.words_filters) > 0)
        self.regex_filters = regex_filters # not implemented for now
        self.check_regex = (len(self.regex_filters) > 0)

        
        if self.is_ordered and not self.match_all:
            print(f"(WW) Rule {self.name} set to be ordered when any word triggers. Argument disregarded.")

    def check(self, message: str) -> bool:
        """Check if the rule is met"""
        print(f"(II) Applying rule {self.name} to message {message}")

        if self.match_all:
            words_match = self._check_all(message) if self.check_words else True
            regex_match = self._check_regex(message) if self.check_regex else True
            return words_match and regex_match

        words_match = self._check_any(message) if self.check_words else False
        regex_match = self._check_regex(message) if self.check_regex else False
        return words_match or regex_match

    def _check_all(self, message: str) -> bool:
        # breakpoint()
        if self.is_ordered:
            return self._check_all_ordered(message)
        return self._check_all_unordered(message)

    def _check_regex(self, message: str) -> bool:
        for regex in self.regex_filters: # just in case, will probably often be only one regex
            if regex.search(message) is None:
                return False

        return True

    def _check_all_unordered(self, message: str) -> bool:
        # breakpoint()
        message_words = [sanitize(x) for x in message.split(" ")]
        for word in self.words_filters:
            if not word in message_words:
                return False
        

        return True

    def _check_all_ordered(self, message:str) -> bool:
        # if first word is not in, fails
        
        if not self.words_filters[0] in message:
            return False

        # find all instances of first word
        occurences = message.count(self.words_filters[0])
        message_words = [sanitize(x) for x in message.split(" ")]
        matches = 0

        for i, word in enumerate(message_words):
            if word == self.words_filters[matches]:
                matches += 1
                
            elif word in self.words_filters:
                matches = 0

            if matches == len(self.words_filters):
                return True

            # we can no longer find all words in the message
            if len(message_words) - i < len(self.words_filters) and matches == 0:
                return False

        return False

    
    def _check_any(self, message: str) -> bool:
        message_words = [sanitize(x) for x in message.split(" ")]
        for word in self.words_filters:
            if word in message:
                return True

        return False

    def to_dict(self):
        return {
            "name": self.name,
            "flagged": True
        }



def sanitize(word):
    return word.lower()