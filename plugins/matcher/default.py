from fuzzywuzzy import fuzz
from dataclasses import dataclass
from plugins.matcher.matcher import Matcher

@dataclass
class Default(Matcher):

    def score(self, term: str, query: str) -> int:
        return 100 if query in term else 0
