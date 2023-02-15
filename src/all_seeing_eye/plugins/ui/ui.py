from abc import abstractmethod
from dataclasses import field
from typing import Iterator, Type, Any, Optional
from all_seeing_eye.plugins.plugins import Plugin


class Ui(Plugin):
    """
    Interface for a Token library
    """
    app: Optional[Type[Any]] = field(default=None, init=False)
    _module_name = 'all_seeing_eye.plugins.ui.default_ui'
    _type = 'UI'

    @abstractmethod
    def progress(self, iterator: Iterator[Any]) -> Iterator[Any]:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, type, value, traceback):
        pass

    @abstractmethod
    def show_results(self):
        pass

    @abstractmethod
    def new_match(self, match) -> None:
        pass
