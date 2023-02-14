from nltk import tokenize
from dataclasses import dataclass
from plugins.tokenizer.tokenizer import Tokenizer

@dataclass
class Tokenize(Tokenizer):

    def tokenize(self, word):
        return tokenize.sent_tokenize(word)
