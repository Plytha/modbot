"""
Class to instantiate rules from the json file
"""


class Rule:

    def __init__(self,
                 name: str,
                 match_all: bool,
                 words_filters: list[str],
                 regex_filters = None):
        
        self.name = name
        self.match_all = match_all
        self.words_filters = words_filters
        self.regex_filters = regex_filters # not implemented for now

        if self.regex_filters is not None \
           and len(self.regex_filters) > 0:
            raise RuntimeError("Regex based filters are not implemented yet")
            

    def check(self, message: str) -> bool:
        """Check if the rule is met"""

        if match_all:
            return _check_all(message)
        return _check_any(message)

    def _check_all(self, message: str) -> bool:
        for word in self.words_filters:
            if not word in message:
                return False

        return True
    
    def _check_any(self, message: str) -> bool:
        for word in self.words_filters:
            if word in message:
                return True

        return False

    def to_dict(self)
        return {
            "name": self.name,
            "flagged": True
        }
