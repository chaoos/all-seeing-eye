from dataclasses import dataclass
from plugins.segmentizer.segmentizer import Segmentizer

@dataclass
class Default(Segmentizer):

    def segment(self, sentence):
        return self.default_segment(sentence)
