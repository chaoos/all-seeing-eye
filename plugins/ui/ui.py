from abc import ABC, abstractmethod
from importlib import import_module
from dataclasses import dataclass
from typing import Iterator
from plugins.plugins import Plugin
import re

@dataclass
class Ui(Plugin):
    """
    Interface for a Token library
    """
    _instance = None
    _class = None
    _module_name = 'plugins.ui.default'
    _type = 'UI'

    @abstractmethod
    def progress(self, iterator: Iterator) -> Iterator:
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

    @classmethod
    def new_match(match):
        pass
