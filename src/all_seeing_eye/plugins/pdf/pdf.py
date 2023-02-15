from abc import abstractmethod
from typing import List, Generator, Dict, Any
from all_seeing_eye.plugins.plugins import Plugin


class Pdf(Plugin):
    """
    Interface for a PDF library
    """
    _module_name = 'all_seeing_eye.plugins.pdf.pdfplumber'
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
    def pages(self) -> Generator[Any, Any, Any]:
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
