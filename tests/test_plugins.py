import pytest
from all_seeing_eye.plugins.matcher.matcher import Matcher
from all_seeing_eye.plugins.pdf.pdf import Pdf
from all_seeing_eye.plugins.segmentizer.segmentizer import Segmentizer
from all_seeing_eye.plugins.tokenizer.tokenizer import Tokenizer
from all_seeing_eye.plugins.ui.ui import Ui
from all_seeing_eye.ase import App, parser
import inspect

matcher_modules = [
    (None, Matcher),
    ('all_seeing_eye.plugins.matcher.fuzzywuzzy', Matcher),
    ('all_seeing_eye.plugins.matcher.default_matcher', Matcher),
]

pdf_modules = [
    (None, Pdf),
    ('all_seeing_eye.plugins.pdf.pdfplumber', Pdf),
    ('all_seeing_eye.plugins.pdf.fitz', Pdf),
    ('all_seeing_eye.plugins.pdf.pdfplumber', Pdf),
    ('all_seeing_eye.plugins.pdf.PyPDF2', Pdf),
]

segmentizer_modules = [
    (None, Segmentizer),
    ('all_seeing_eye.plugins.segmentizer.wordsegment', Segmentizer),
    ('all_seeing_eye.plugins.segmentizer.default_segmentizer', Segmentizer),
]

tokenizer_modules = [
    (None, Tokenizer),
    ('all_seeing_eye.plugins.tokenizer.tokenize', Tokenizer),
    ('all_seeing_eye.plugins.tokenizer.default_tokenizer', Tokenizer),
]

ui_modules = [
    (None, Ui),
    ('all_seeing_eye.plugins.ui.default_ui', Ui),
    ('all_seeing_eye.plugins.ui.rich', Ui),
]


@pytest.mark.parametrize("module,plugin", matcher_modules + pdf_modules + segmentizer_modules + tokenizer_modules)
def test_factory(module, plugin):
    assert isinstance(plugin.get_instance(module), plugin)


@pytest.mark.parametrize("module,plugin", ui_modules)
@pytest.mark.skip(reason="parse_args trows error")
def test_factory_ui(module, plugin):
    cls = plugin.get_class(module)
    app = App(parser().parse_args())
    assert isinstance(cls(app), plugin)


@pytest.mark.parametrize("module,plugin", matcher_modules + pdf_modules + segmentizer_modules + tokenizer_modules + ui_modules)
def test_factory_class(module, plugin):
    assert inspect.isclass(plugin.get_class(module))
