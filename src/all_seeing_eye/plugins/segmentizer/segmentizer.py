from abc import ABC, abstractmethod
from importlib import import_module
from dataclasses import dataclass, field
from typing import Dict
from all_seeing_eye.plugins.plugins import Plugin
import re

@dataclass
class Segmentizer(Plugin):
    """
    Interface for a Segmentation library
    """
    _instance = None
    _class = None
    _module_name = 'all_seeing_eye.plugins.segmentizer.wordsegment'
    _type = 'Segment'

    def default_segment(self, word: str) -> str:
        regex = r'|'.join(["\/", "\_", "\-", "\.", "\:", "\,", "\;"])
        return " ".join(re.split(regex, word))

    @abstractmethod
    def segment(self, sentence: str) -> str:
        """
        Segmentize a sentence.
        
        :param      sentence:  The sentence
        :type       sentence:  str
        
        :returns:   The segmentized sentence
        :rtype:     str
        """
        pass

