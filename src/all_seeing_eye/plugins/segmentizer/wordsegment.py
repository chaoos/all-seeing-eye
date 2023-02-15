import wordsegment
from dataclasses import dataclass, field
from all_seeing_eye.plugins.segmentizer.segmentizer import Segmentizer
import sys


@dataclass
class Wordsegment(Segmentizer):

    regex: str = field(default=r'|'.join([r"\/", r"\_", r"\-", r"\.", r"\:", r"\,", r"\;"]), repr=False)

    def __post_init__(self):
        # wordsegment.segment needs this depth
        sys.setrecursionlimit(2000)
        wordsegment.load()

    def segment(self, sentence):
        try:
            return " ".join(wordsegment.segment(sentence))
        except RecursionError:
            return self.default_segment(sentence)
