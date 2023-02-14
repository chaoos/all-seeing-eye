from dataclasses import dataclass
from plugins.ui.ui import Ui
from ase import App
from tqdm import tqdm
import os

@dataclass
class Default(Ui):
    app: App

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

    def new_match(match):
        print(match)
