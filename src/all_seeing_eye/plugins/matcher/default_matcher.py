from all_seeing_eye.plugins.matcher.matcher import Matcher


class Default(Matcher):

    def score(self, term: str, query: str) -> int:
        return 100 if query in term else 0
