from abc import abstractmethod
from all_seeing_eye.plugins.plugins import Plugin
import re


class Segmentizer(Plugin):
    """
    Interface for a Segmentation library
    """
    _module_name = 'all_seeing_eye.plugins.segmentizer.wordsegment'
    _type = 'Segment'

    def default_segment(self, word: str) -> str:
        regex = r'|'.join([r"\/", r"\_", r"\-", r"\.", r"\:", r"\,", r"\;"])
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
