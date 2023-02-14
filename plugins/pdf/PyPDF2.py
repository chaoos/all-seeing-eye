import PyPDF2
from dataclasses import dataclass
from plugins.pdf.pdf import Pdf

@dataclass
class PyPDF2(Pdf):

    def open(self, path):
        self.file_handle = open(path, 'rb')
        self.pdf = PyPDF2.PdfReader(self.file_handle)
        return self.pdf

    def close(self):
        self.file_handle.close()

    @property
    def num_pages(self):
        return len(self.pdf.pages)

    @property
    def pages(self):
        return (page for page in self.pdf.pages)

    def get_page_nr(self, page):
        return list(self.get_pages()).index(page)+1

    def get_page_text(self, page):
        return page.extract_text().replace('\n', ' ')
