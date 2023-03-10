from nltk import tokenize
from all_seeing_eye.plugins.tokenizer.tokenizer import Tokenizer


class Tokenize(Tokenizer):

    def tokenize(self, word):
        return tokenize.sent_tokenize(word)
