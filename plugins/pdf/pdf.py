from abc import ABC, abstractmethod
from importlib import import_module
from dataclasses import dataclass
from typing import List, Generator, Dict
from plugins.plugins import Plugin

@dataclass
class Pdf(Plugin):
    """
    Interface for a PDF library
    """
    _instance = None
    _class = None
    _module_name = 'plugins.pdf.pdfplumber'
    _type = 'PDF'

    @abstractmethod
    def open(self, path: str):
        pass

    @abstractmethod
    def close(self):
        pass

    @property
    @abstractmethod
    def num_pages(self) -> int:
        pass

    @property
    @abstractmethod
    def pages(self) -> Generator:
        pass

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_page_nr(self, page) -> int:
        pass

    @abstractmethod
    def get_page_text(self, page) -> str:
        pass

    @abstractmethod
    def get_page_annots(self, page) -> List[str]:
        pass
