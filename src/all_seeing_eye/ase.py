#!/usr/bin/env python3

import argparse
import os
import pickle
import hashlib
from dataclasses import dataclass, field
from typing import List, Iterator
from itertools import chain
from abc import ABC, abstractmethod
from all_seeing_eye.lib.app import App, SearchConfig, Item, Match


@dataclass
class FileIterator:
    path: str
    config: SearchConfig = field(default_factory=SearchConfig)

    def segment(self, word, segmentize):
        if segmentize:
            word = self.config.segmentizer.segment(word)
        return {'display': word, 'search': word}


@dataclass
class FileInfo(FileIterator):
    """
    This class describes the iterator for regular file metadata
    """
    def __iter__(self):
        return iter([
            Item(self.path, "Dirname", self.segment(os.path.dirname(self.path), False)),
            Item(self.path, "Filename", {
                'display': os.path.basename(self.path),
                'search': os.path.basename(self.path)
            }),
        ])


@dataclass
class PdfMeta(FileIterator):
    """
    This class describes the iterator for PDF metadata
    """
    def __iter__(self):
        self.config.pdf.open(self.path)
        return iter(Item(self.path, "Metadata", self.segment(v, self.config.segmentize))
                    for (k, v) in self.config.pdf.metadata)

    def __del__(self):
        self.config.pdf.close()


@dataclass
class PdfIterator(ABC, FileIterator):
    path: str = field(default=None)
    config: SearchConfig = field(default_factory=SearchConfig)
    iter_items: List[Item] = field(default_factory=list)
    from_memory: bool = field(default=False)

    def __post_init__(self):
        hash_args = [
            __class__.__name__,
            self.path,
            self.config.segmentize,
            self.config.tokenize,
            self.config.contents
        ]
        hash = hashlib.md5(str(hash_args).encode()).hexdigest()
        self.cache_fname = f'{self.config.cache_dir}/{self.__class__.__name__}/{hash}.cache'

        self.config.pdf.open(self.path)
        if not self.config.reindex:
            self.load()

    def __del__(self):
        self.config.pdf.close()
        self.store()

    def __iter__(self) -> Iterator[Item]:
        if self.from_memory:
            return iter(self.iter_items)
        else:
            return filter(lambda x: x is not None,
                          (self.factory(Item,
                                        path=self.path,
                                        where=self.get_metainfo(page),
                                        term=self.segment(item, self.config.segmentize))
                           for page in self.config.pdf.pages for item in self.get_items_on_page(page)))

    def factory(self, object, *args, **kwargs):
        try:
            o = object(*args, **kwargs)
            self.iter_items.append(o)
            return o
        except UnicodeDecodeError:
            return None

    def load(self):
        if self.config.cache_dir is not None:
            os.makedirs(os.path.dirname(self.cache_fname), exist_ok=True)
            if os.path.exists(self.cache_fname):
                with open(self.cache_fname, 'rb') as handle:
                    self.iter_items = pickle.load(handle)
                    self.from_memory = True

    def store(self):
        if self.config.cache_dir is not None and not self.from_memory:
            os.makedirs(os.path.dirname(self.cache_fname), exist_ok=True)
            with open(self.cache_fname, 'wb') as handle:
                pickle.dump(self.iter_items, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @abstractmethod
    def get_items_on_page(self, page) -> List[str]:
        pass

    @abstractmethod
    def get_metainfo(self, page) -> str:
        pass


class PdfCont(PdfIterator):
    """
    This class describes the iterator for contents of PDF files
    """
    def get_items_on_page(self, page):
        return self.config.tokenizer.tokenize(self.config.pdf.get_page_text(page))

    def get_metainfo(self, page):
        return f"Contents of page {self.config.pdf.get_page_nr(page)}/{self.config.pdf.num_pages}"


# todo: segmentize=False only here
class PdfAnnots(PdfIterator):
    """
    This class describes the iterator for annotations of PDF files
    """
    def get_items_on_page(self, page):
        return self.config.pdf.get_page_annots(page)

    def get_metainfo(self, page):
        return f"Annotations of page {self.config.pdf.get_page_nr(page)}/{self.config.pdf.num_pages}"


@dataclass
class PdfSegments(FileIterator):
    """
    This class describes the iterator that splits a PDF document into its
    sentences, annotations, metadata, ...
    """
    def __iter__(self):
        return chain(
            FileInfo(self.path, self.config),
            PdfMeta(self.path, self.config, ),
            PdfCont(self.path, self.config) if self.config.contents else iter([]),
            PdfAnnots(self.path, self.config) if self.config.contents else iter([]),
        )


def parser():
    parser = argparse.ArgumentParser(description='All-seeing Eye: Search PDF metadata and contents')
    parser.add_argument('query', help='Query for substring in metadata')
    parser.add_argument('-d', '--directories', type=os.path.expanduser,
                        nargs='+', help='Directories to search', default=[])
    parser.add_argument('-c', '--contents', help='Seach contents as well (slower)',
                        action='store_true')
    parser.add_argument('--break', dest='brk', help='Stop after first match for each file',
                        action='store_true')
    parser.add_argument('--th', '--threshold', dest='threshold',
                        help='Search score threshold', type=int, default=70)
    parser.add_argument('-s', dest='segmentize', help='Segmentize words (very slow)',
                        action='store_true')
    parser.add_argument('-t', dest='tokenize',
                        help='Tokenize the pages using sent_tokenize() (slower)', action='store_true')
    parser.add_argument('-f', '--force', help='overwrite setting from config.json file',
                        action='store_true')
    parser.add_argument('-r', '--reindex', help='rewrite the index', action='store_true')
    parser.add_argument('--config', type=os.path.expanduser,
                        help='path to the config file',
                        default='~/.config/ase/config.json')
    return parser


def main():

    app = App(parser().parse_args())
    print(f"{app.config = }")

    with app.config.ui as ui:
        for path in ui.progress(app.config.files):
            for item in PdfSegments(path, app.config):
                if (score := app.config.matcher.score(item.term.get('search'), app.args.query)) >= app.args.threshold:
                    app.matches.append(Match(score, item))

        ui.show_results()


if __name__ == '__main__':
    main()
