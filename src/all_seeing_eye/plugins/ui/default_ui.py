from all_seeing_eye.plugins.ui.ui import Ui
from tqdm import tqdm
import os


class Default(Ui):

    def set_description(self, x):
        self.bar.set_description(f"File {os.path.basename(x)}")
        return x

    def progress(self, iterator):
        self.bar = tqdm(iterator)
        return (self.set_description(x) for x in self.bar)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def show_results(self):
        print(self.app.matches)

    def new_match(self, match):
        print(match)
