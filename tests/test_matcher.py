import pytest
from all_seeing_eye.plugins.matcher.matcher import Matcher

matcher_modules = [
    ('all_seeing_eye.plugins.matcher.fuzzywuzzy', Matcher),
    # ('all_seeing_eye.plugins.matcher.default_matcher', Matcher),
]

lorem = ("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam "
         " nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam "
         "erat, sed diam voluptua.")


@pytest.mark.parametrize("module,plugin", matcher_modules)
@pytest.mark.parametrize("term,query,score_op", [
    (lorem, "ipsum", lambda s: s == 100),
    (lorem, "iPsuM", lambda s: s == 100),
    (lorem, "IPSUM", lambda s: s == 100),
    (lorem, "ipsum consetetur", lambda s: s == 100),
    (lorem, "ipsum conseteur", lambda s: s < 100 and 50 < s),
    (lorem, "ipsum-conseteur", lambda s: s < 100 and 50 < s),
    (lorem, "ipum", lambda s: s < 100 and 50 < s),
    (lorem, "ipum labore", lambda s: s < 100 and 50 < s),
])
def test_scorer(module, plugin, term, query, score_op):
    instance = plugin.get_class(module)()
    assert score_op(instance.score(term, query))
