from abc import abstractmethod
from all_seeing_eye.plugins.plugins import Plugin


class Matcher(Plugin):
    """
    Interface for a Match library
    """
    _module_name = 'all_seeing_eye.plugins.matcher.fuzzywuzzy'
    _type = 'Match'

    @abstractmethod
    def score(self, term: str, query: str) -> int:
        """
        Return the score of a query in a search term.

        :param      term:   The term
        :type       term:   str
        :param      query:  The query
        :type       query:  str

        :returns:   The score from 0 to 100.
        :rtype:     int
        """
        pass
