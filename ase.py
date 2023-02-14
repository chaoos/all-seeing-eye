#!/usr/bin/env python3

import argparse
import json
import os
from termcolor import colored
import textwrap
import pickle
import hashlib
from dataclasses import dataclass, field
from typing import Dict, Union, List, Iterator
from itertools import chain
from dacite import from_dict, Config
from abc import ABC, abstractmethod
from plugins.pdf.pdf import Pdf
from plugins.segmentizer.segmentizer import Segmentizer
from plugins.tokenizer.tokenizer import Tokenizer
from plugins.matcher.matcher import Matcher
from plugins.ui.ui import Ui
from typing import Generator, List, Callable, Optional
from functools import partial, reduce

# The function is usable such as combine(f,g)(x) with is equivalent to g(f(x)).
combine = lambda *xs: partial (reduce, lambda v,x: x(v), xs)

@dataclass
class Item:
    """
    This class describes a search item.
    """
    path: str = None
    where: str = None
    term: Dict[str, str] = field(default_factory=dict)

@dataclass(order=True)
class Match:
    """
    This class describes a match.
    """
    score: int = field(default=0, compare=True)
    item: Item = field(default_factory=Item, compare=False)

    def __str__(self):
        score = colored(f"(score = {self.score})", "green" if self.score > 95 else "light_green")
        where = colored(f"{self.item.where}", attrs=["bold"])
        if self.item.path is not None:
            basename = os.path.basename(self.item.path)
            dirname = os.path.dirname(self.item.path)
        else:
            basename = None
            dirname = None
        file_len = os.get_terminal_size().columns - len(" • {file}: {score}".format(score=score, file=""))
        file = colored(textwrap.shorten(f"{basename}", width=file_len), None, attrs=["underline"])
        match = "\n".join(
            textwrap.wrap(
                colored(f"\"{self.item.term.get('display')}\"", None, attrs=["dark"]),
                width=os.get_terminal_size().columns-10,
                initial_indent="\t",
                subsequent_indent="\t"
            )
        )

        return (
            f" • {file}: {score}\n"
          + f"\tFound in {where}, directory: {dirname}:\n"
          + f"{match}"
        )

@dataclass
class SearchConfig:
    """
    This class describes a search setup.
    """
    cache_dir: Optional[str] = field(default=None, hash=False)
    segmentize: bool = field(default=False, hash=True)
    tokenize: bool = field(default=False, hash=True)
    contents: bool = field(default=False, hash=True)
    directories: List[str] = field(default_factory=list, hash=False)
    segmentizer: Segmentizer = field(default_factory=Segmentizer.get_instance, hash=False)
    tokenizer: Tokenizer = field(default_factory=Tokenizer.get_instance, hash=False)
    matcher: Matcher = field(default_factory=Matcher.get_instance, hash=False)
    pdf: Pdf = field(default_factory=Pdf.get_instance, hash=False)
    ui: Ui = field(default_factory=Ui.get_class, hash=False)
    reindex: bool = field(default=False, hash=False)
    __files: List = field(default=None, init=False, repr=False)


    @property
    def files(self) -> List:
        """
        Property holding a list of files to search, should be a list, because we
        want to know how many files there are in order to show a progress bar.
        
        :returns:   The list of files
        :rtype:     List
        """
        
        if self.__files is None:
            is_pdf = lambda y: y.endswith("pdf")
            pdfs = filter(is_pdf, filter(os.path.isfile, self.directories))
            dirs = filter(os.path.isdir, self.directories)
            dir_walk = chain.from_iterable(map(os.walk, dirs))
            join = lambda x: map(partial(os.path.join, x[0]), filter(is_pdf, x[2]))
            self.__files = list(chain(pdfs, chain.from_iterable(map(join,dir_walk))))
        return self.__files

def config_factory(app, args: argparse.Namespace) -> SearchConfig:
    """
    Instantiate the SearchConfig object.
    
    :param      args:  The arguments
    :type       args:  Return value of parser.parse_args()
    
    :returns:   The configuration.
    :rtype:     SearchConfig
    """
    file = {}
    if os.path.exists(args.config):
        with open(args.config) as f:
            try:
                file = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f"file {args.config} contains invalid json")
                exit(1)

    data = {**file, **args.__dict__} if args.force else {**args.__dict__, **file}
    if not args.force:
        data['directories'] += args.directories

    cfg = Config(type_hooks={
        Segmentizer: lambda p: Segmentizer.get_instance(p.get("module_name")),
        Tokenizer: lambda p: Tokenizer.get_instance(p.get("module_name")),
        Matcher: lambda p: Matcher.get_instance(p.get("module_name")),
        Pdf: lambda p: Pdf.get_instance(p.get("module_name")),
        Ui: lambda p: Ui.get_class(p.get("module_name")),
        str: combine(os.path.expanduser, os.path.abspath), # also applies for List[str]
    })

    return from_dict(data_class=SearchConfig, data=data, config=cfg)

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
            for (k,v) in self.config.pdf.metadata)

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
                (
                    self.factory(Item,
                        path=self.path,
                        where=self.get_metainfo(page),
                        term=self.segment(item, self.config.segmentize)
                    ) for page in self.config.pdf.pages for item in self.get_items_on_page(page)
                )
            )

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

class MatchList(list):
    on_append: Callable = field(default=lambda x: None)

    def append(self, match):
        self.on_append(match)
        return super().append(match)

    def __str__(self):
        self.sort()
        hr = "─"*os.get_terminal_size().columns + "\n"
        return f"{hr}" + "\n".join(map(str, self)) + f"\n{hr}{len(self)} results found."

@dataclass
class App():
    args: argparse.Namespace
    matches: MatchList = field(default_factory=MatchList)
    config: SearchConfig = field(default_factory=SearchConfig)

    def __post_init__(self):
        self.config = config_factory(self, self.args)
        self.matches.on_append = self.config.ui.new_match # todo: why class method?

def main():
    parser = argparse.ArgumentParser(description='All-seeing Eye: Search PDF metadata and contents')
    parser.add_argument('query', help='Query for substring in metadata')
    parser.add_argument('-d','--directories', type=os.path.expanduser,
        nargs='+', help='Directories to search', default=[])
    parser.add_argument('-c','--contents', help='Seach contents as well (slower)',
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
    parser.add_argument('-r', '--reindex', help='rewrite the index',action='store_true')
    parser.add_argument('--config', type=os.path.expanduser,
        help='path to the config file',
        default='~/.config/ase/config.json')

    app = App(parser.parse_args())
    print(f"{app.config = }")

    with app.config.ui(app) as ui:
        for path in ui.progress(app.config.files):
            for item in PdfSegments(path, app.config):
                if (score := app.config.matcher.score(item.term.get('search'), app.args.query)) >= app.args.threshold:
                    app.matches.append(Match(score, item))

        ui.show_results()

if __name__ == '__main__':
    main()
