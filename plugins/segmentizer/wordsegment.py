import wordsegment
from dataclasses import dataclass, field
from plugins.segmentizer.segmentizer import Segmentizer
import sys

@dataclass
class Wordsegment(Segmentizer):

    regex: str = field(default=r'|'.join(["\/", "\_", "\-", "\.", "\:", "\,", "\;"]), repr=False)

    def __post_init__(self):
        # wordsegment.segment needs this depth
        sys.setrecursionlimit(2000)
        wordsegment.load()

    def segment(self, sentence):
        try:
            return " ".join(wordsegment.segment(sentence))
        except RecursionError:
            return self.default_segment(sentence)