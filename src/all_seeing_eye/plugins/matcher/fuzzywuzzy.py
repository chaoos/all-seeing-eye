from fuzzywuzzy import fuzz
from all_seeing_eye.plugins.matcher.matcher import Matcher


class FuzzyWuzzy(Matcher):

    def score(self, term: str, query: str) -> int:
        if len(term) < len(query):
            return 0

        scores = [
            fuzz.ratio(term, query),
            fuzz.partial_ratio(term, query),
            fuzz.token_set_ratio(term, query),
            fuzz.token_sort_ratio(term, query),
        ]
        return int(scores[scores.index(max(scores))])
