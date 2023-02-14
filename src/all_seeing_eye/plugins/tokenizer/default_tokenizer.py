from dataclasses import dataclass
from all_seeing_eye.plugins.tokenizer.tokenizer import Tokenizer

@dataclass
class Default(Tokenizer):

    def tokenize(self, word):
        return word.split(".")
