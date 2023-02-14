from dataclasses import dataclass
from plugins.tokenizer.tokenizer import Tokenizer

@dataclass
class Default(Tokenizer):

    def tokenize(self, word):
        return word.split(".")
