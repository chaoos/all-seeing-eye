from all_seeing_eye.plugins.tokenizer.tokenizer import Tokenizer


class Default(Tokenizer):

    def tokenize(self, word):
        return word.split(".")
