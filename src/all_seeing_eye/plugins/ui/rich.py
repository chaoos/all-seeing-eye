from dataclasses import field
from all_seeing_eye.plugins.ui.ui import Ui
from rich.progress import Progress


class Rich(Ui):
    prog: Progress = field(default_factory=Progress)

    def __post_init__(self):
        self.prog.__enter__()
        self.task = self.prog.add_task("[red]Searching ...")

    def advance(self, x):
        self.prog.advance(self.task)
        return x

    def progress(self, iterator):
        self.prog.update(self.task, total=len(iterator)-1)
        return (self.advance(x) for x in iterator)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def show_results(self):
        print(self.app.matches)

    def new_match(self, match):
        print(match)
