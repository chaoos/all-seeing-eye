import pdfplumber
from dataclasses import dataclass
from all_seeing_eye.plugins.pdf.pdf import Pdf

@dataclass
class PdfPlumber(Pdf):

    def open(self, path):
        self.handle = pdfplumber.open(path)
        return self.handle

    def close(self):
        self.handle.close()

    @property
    def num_pages(self):
        return len(self.handle.pages)

    @property
    def pages(self):
        return (page for page in self.handle.pages)

    @property
    def metadata(self):
        return (item for item in self.handle.metadata.items())

    def get_page_nr(self, page):
        return page.page_number

    def get_page_text(self, page):
        return page.extract_text().replace('\n', ' ')

    def get_page_annots(self, page):
        return filter(lambda x: x is not None,
            map(lambda a: a.get('contents'), page.annots))
