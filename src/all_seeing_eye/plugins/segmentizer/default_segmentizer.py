from all_seeing_eye.plugins.segmentizer.segmentizer import Segmentizer


class Default(Segmentizer):

    def segment(self, sentence):
        return self.default_segment(sentence)
