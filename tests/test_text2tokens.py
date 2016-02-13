__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/13/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"


from itertools import repeat
from functools import partial
import types

import pytest
import toolz as tlz
map_c = tlz.curry(tlz.map)
reduce_c = tlz.curry(tlz.reduce)

from text2math import text2tokens


is_generator = lambda obj: isinstance(obj, types.GeneratorType)

var_len_strings = lambda n: list(tlz.take(n, tlz.iterate(lambda string: string + "a", "")))


def test__stopwords():
    assert(text2tokens.STOPWORDS)


def test__stopwords__2():
    assert(tlz.pipe(text2tokens.STOPWORDS,
                    set,
                    lambda sw: sw.intersection({"the", "and", "or", "has"}),
                    len,
                    lambda length: bool(length == 4)))


@pytest.mark.parametrize("glue,strings,expected",
                         [("-", ["foo", "bar"], "foo-bar"),
                          ("baz", ["foo", "bar"], "foobazbar"),
                          ("*", ["foo", "bar", "baz"], "foo*bar*baz"),
                          ])
def test__join_strings(glue, strings, expected):
    assert(text2tokens.join_strings(glue, strings) == expected)


@pytest.mark.parametrize("string",
                         ["monkey",
                          "monkey--monkey",
                          ])
def test__split_on_reg__0(string):
    splitter = text2tokens.split_on_reg(r"[-]+")
    assert(is_generator(splitter(string)))


@pytest.mark.parametrize("string,pattern,length",
                         [("monkey", r"[-]+", 1),
                          ("monkey--monkey", r"[-]+", 2),
                          ("monkey--monkey---monkey", r"[-]+", 3),
                          ])
def test__split_on_reg__1(string, pattern, length):
    tokens = list(text2tokens.split_on_reg(pattern, string))
    assert(len(tokens) == length)
    assert(len(set(tokens)) == 1)


@pytest.mark.parametrize("string",
                         ["monkey",
                          "monkey--monkey",
                          ])
def test__splitter_of_words__0(string):
    assert(is_generator(text2tokens.splitter_of_words(string)))


@pytest.mark.parametrize("string,length,unique",
                         [("monkey", 1, 1),
                          ("monkey--monkey", 2, 1),
                          ("monkey--monkey---monkey", 3, 1),
                          ("monkey&&monkey", 2, 1),
                          ("foo foo", 2, 1),
                          ("bar  bar", 2, 1),
                          ("monkey-/#$%() \\*+=?.:;[]!&<>@monkey", 2, 1),
                          ("foo-/#$%() \\bar*+=?.:;[]!&<>@baz", 3, 3),
                          ("foo-/bar#$%()foo \\bar*+=?.:baz;[]!foo&<>@baz", 7, 3),
                          ("he's", 2, 2),
                          ])
def test__splitter_of_words__1(string, length, unique):
    tokens = list(text2tokens.splitter_of_words(string))
    assert(len(tokens) == length)
    assert(len(set(tokens)) == unique)


@pytest.mark.parametrize("string,expected",
                         [("MONKEY", "monkey"),
                          ("Foo Bar baz", "foo bar baz"),
                          ])
def test__lower(string, expected):
    assert(text2tokens.lower(string) == expected)


@pytest.mark.parametrize("tokenset,count",
                         [([" ", "", "\t", "\n", "\r"], 0),
                          ([" \t\n\r"], 0),
                          (["MONKEY", "monkey", "foo bar baz"], 3),
                          (["monkey\t", "foo\n", "bar\r"], 3),
                          ])
def test__filter_whitespace(tokenset, count):
    assert(len(list(text2tokens.filter_whitespace(tokenset))) == count)


@pytest.mark.parametrize("tokenset,mintokenlen,count",
                         [(var_len_strings(20), 0, 20),
                          (var_len_strings(20), 5, 15),
                          (var_len_strings(20), 20, 0),
                          ])
def test__filter_shorter_than(tokenset, mintokenlen, count):
    length = tlz.pipe(tokenset,
                      text2tokens.filter_shorter_than(mintokenlen),
                      list,
                      len)
    assert(length == count)


@pytest.mark.parametrize("tokenset,mintokenlen,count",
                         [(var_len_strings(20), 0, 0),
                          (var_len_strings(20), 5, 5),
                          (var_len_strings(20), 20, 20),
                          ])
def test__filter_longer_than(tokenset, mintokenlen, count):
    length = tlz.pipe(tokenset,
                      text2tokens.filter_longer_than(mintokenlen),
                      list,
                      len)
    assert(length == count)


@pytest.mark.parametrize("tokenset,count",
                         [(("the", "and", "or"), 0),
                          ])
def test__filter_stopwords(tokenset, count):
    assert(tlz.pipe(tokenset,
                    text2tokens.filter_stopwords,
                    list,
                    len,
                    lambda length: length == count,
                    ))


# -----------------------------------------------------------------------------


@pytest.mark.parametrize("n,string,expected",
                         [(1, "foo-bar", [("foo", ), ("bar", )]),
                          (1, "foobazbar", [("foobazbar", )]),
                          (1, "foo*bar*baz", [("foo", ), ("bar", ), ("baz", )]),
                          (2, "foo*bar*baz", [("foo", "bar"), ("bar", "baz")]),
                          (1, "foo-and-where-bar", [("foo", ), ("bar", )]),
                          (2, "foo-and-where-bar", [("foo", "bar")]),
                          ])
def test__ngram_tuples(n, string, expected):
    assert(list(text2tokens.ngram_tuples(n, string)) == expected)


@pytest.mark.parametrize("n,string,expected",
                         [(1, "foo-bar", ["foo", "bar"]),
                          (2, "foo-bar", ["foo_bar"]),
                          (3, "foo-bar", []),
                          (1, "foobazbar", ["foobazbar"]),
                          (2, "foobazbar", []),
                          (3, "foobazbar", []),
                          (1, "foo*bar*baz", ["foo", "bar", "baz"]),
                          (2, "foo*bar*baz", ["foo_bar", "bar_baz"]),
                          (3, "foo*bar*baz", ["foo_bar_baz"]),
                          ])
def test__ngram(n, string, expected):
    assert(list(text2tokens.ngram(n, string)) == expected)


@pytest.mark.parametrize("string,expected",
                         [("foo-bar", ["foo", "bar"]),
                          ("foobazbar", ["foobazbar"]),
                          ("foo*bar*baz", ["foo", "bar", "baz"]),
                          ])
def test__unigram(string, expected):
    assert(list(text2tokens.unigram(string)) == expected)


@pytest.mark.parametrize("string,expected",
                         [("foo-bar", ["foo_bar"]),
                          ("foobazbar", []),
                          ("foo*bar*baz", ["foo_bar", "bar_baz"]),
                          ])
def test__bigram(string, expected):
    assert(list(text2tokens.bigram(string)) == expected)


@pytest.mark.parametrize("string,expected",
                         [("foo-bar", []),
                          ("foobazbar", []),
                          ("foo*bar*baz", ["foo_bar_baz"]),
                          ])
def test__trigram(string, expected):
    assert(list(text2tokens.trigram(string)) == expected)
