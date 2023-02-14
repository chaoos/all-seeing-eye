from abc import ABC, abstractmethod
from importlib import import_module
from dataclasses import dataclass
from plugins.plugins import Plugin

@dataclass
class Matcher(Plugin):
    """
    Interface for a Match library
    """
    _instance = None
    _class = None
    _module_name = 'plugins.matcher.fuzzywuzzy'
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
