from abc import abstractmethod
from typing import List
from all_seeing_eye.plugins.plugins import Plugin


class Tokenizer(Plugin):
    """
    Interface for a Token library
    """
    _module_name = 'all_seeing_eye.plugins.tokenizer.tokenize'
    _type = 'Token'

    @abstractmethod
    def tokenize(self, word: str) -> List[str]:
        pass
