import fitz
from all_seeing_eye.plugins.pdf.pdf import Pdf


class Fitz(Pdf):

    def open(self, path):
        self.doc = fitz.open(path)
        return self.doc

    def close(self):
        if not self.doc.is_closed:
            self.doc.close()

    @property
    def num_pages(self):
        return len(self.doc)

    @property
    def pages(self):
        return (page for page in self.doc)

    def get_page_nr(self, page):
        return page.number+1

    def get_page_text(self, page):
        return page.get_text().replace('\n', ' ')
