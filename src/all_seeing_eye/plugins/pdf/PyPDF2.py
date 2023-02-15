import PyPDF2 as PyPDF2lib
from all_seeing_eye.plugins.pdf.pdf import Pdf


class PyPDF2(Pdf):

    def open(self, path):
        self.file_handle = open(path, 'rb')
        self.pdf = PyPDF2lib.PdfReader(self.file_handle)
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
        return list(self.pages).index(page)+1

    def get_page_text(self, page):
        return page.extract_text().replace('\n', ' ')
