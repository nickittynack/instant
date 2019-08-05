import warnings
from pprint import pprint

from tracer import Tracer, format_history_as_table, trace_code, trace_code_file


HIST = [
    {1: {}, 8: {"a": "f"}},
    {1: {"n": 4}, 2: {"j": 10}, 3: {"i": 0}, 4: {"j": 11}},
    {3: {"i": 1}, 4: {"j": 12}},
    {3: {"i": 2}, 4: {"j": 13}},
    {3: {"i": 3}, 4: {"j": 14}},
    {3: {}, 5: {}, 10: {"the_result": 14}},
]


def test_basic_tracer():
    hist = trace_code_file("tests/fixtures/spam.py")
    assert hist == HIST
    t = format_history_as_table(hist)


def test_hist_format():
    t = format_history_as_table(HIST)
    assert t[9]["5"] == "the_result = 14"


CODE = """
a = 'http://example.com/whatever'

scheme, remainder = a.split(':')

"""


def test_multivar_trace():
    t = trace_code(CODE)


def test_req_cache():
    hist = trace_code_file("tests/fixtures/req.py")
    t = format_history_as_table(hist)
    assert t.keys() == ["0"]


def test_errortrace():
    hist = trace_code_file("tests/fixtures/exception.py")
    t = format_history_as_table(hist)


def test_mutate():
    hist = trace_code_file("tests/fixtures/mutate.py")
    t = format_history_as_table(hist)
    print(t)
    assert t[0][0] == "base = ['C', 'A', 'T']"
    assert t[1][0] == "base = ['B', 'A', 'T']"
    assert t[3][0] == "d = {'a': 'hello'}"
    assert t[4][0] == "d = {'a': 'world'}"
