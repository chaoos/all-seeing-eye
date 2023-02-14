from abc import ABC, abstractmethod
from importlib import import_module
from dataclasses import dataclass
from typing import List
from all_seeing_eye.plugins.plugins import Plugin
import re

@dataclass
class Tokenizer(Plugin):
    """
    Interface for a Token library
    """
    _instance = None
    _class = None
    _module_name = 'all_seeing_eye.plugins.tokenizer.tokenize'
    _type = 'Token'

    @abstractmethod
    def tokenize(self, word: str) -> List[str]:
        pass

