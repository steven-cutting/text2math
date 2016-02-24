__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/13/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"

from itertools import repeat, count
import json
import os
import re
import sys

import toolz as tlz
filter_c = tlz.curry(tlz.filter)
map_c = tlz.curry(tlz.map)
sliding_window_c = tlz.curry(tlz.sliding_window)

if sys.version_info[0] < 3:
    from itertools import izip as zip


with open(os.path.join(os.path.dirname(__file__), 'stopwords.json')) as fp:
    STOPWORDS = frozenset(json.load(fp))


# ---------------------------


@tlz.curry
def join_strings(glue, strings):
    """
    Same as:
        In [0]: glue = "-"
        In [1]: strings = ["foo", "bar"]
        In [2]: glue.join(strings)
        Out[2]: "foo-bar"
    """
    return glue.join(strings)


# ---------------------------


def simple_split(string):
    """
    Same as str.split()

    Splits 'string' on whitespace. Empty strings are remove from the result.
    """
    return string.split()


@tlz.curry
def split_on_reg(regpattern, string):
    """
    Splits the string based on the regex pattern 'regpattern'.
    """
    return (bit for bit in re.split(regpattern, string))


def splitter_of_words(string):
    """
    Splits 'string' on non alphanumeric characters.
    """

    non_alpha_num = r"""[,-/\#\$\%\(\)\*\+\<\=\>\@\[\\\]\^\`\{\|\}\~ :?&;!'"\n\t\r_]+"""
    return split_on_reg(non_alpha_num, string)


# ---------------------------
# Treatments


def lower(string):
    """
    Makes string all lowercase.
    """
    return string.lower()


@tlz.curry
def replace(new, old, string):
    """
    Replace 'old' in 'string' with 'new'.
    """
    return string.replace(old, new)


@tlz.curry
def merge_on(old, string):
    """
    Merge on 'old'.
    """
    return replace(new='', old=old, string=string)


# ---------------------------


def filter_whitespace(tokenset):
    """
    Filters out tokens that are only whitespace.
    """
    return tlz.filter(tlz.compose(bool, lambda string: string.strip()), tokenset)


@tlz.curry
def filter_shorter_than(n, tokenset):
    """
    Filters out tokens that have less than 'n' characters.
    """
    return tlz.filter(lambda tkn: len(tkn) >= n, tokenset)


@tlz.curry
def filter_longer_than(n, tokenset):
    """
    Filters out tokens that have 'n' characters or more.
    """
    return tlz.filter(lambda tkn: len(tkn) < n, tokenset)


def filter_stopwords(tokenset):
    """
    Filters out stopwords.
    """
    return tlz.filter(lambda tkn: tkn not in STOPWORDS, tokenset)


# -----------------------------------------------------------------------------


@tlz.curry
def ngram_tuples(n, string, minlen=3, maxlen=25):
    """
    Creates ngram tuples of size 'n' from 'string'.

    Ex:
        In [2]: list(ngram_tuples(n=1, string='Just another example text.'))
        Out[2]: [('another',), ('example',), ('text',)]

        In [2]: list(ngram_tuples(n=2, string='Just another example text.'))
        Out[2]: [('another', 'example'), ('example', 'text')]

        In [11]: list(ngram_tuples(3, 'I needed a longer example text for this example.'))
        Out[11]:
            [('needed', 'longer', 'example'),
             ('longer', 'example', 'text'),
             ('example', 'text', 'example')]


    minlen - filter out words that have fewer characters than 'minlen'.
    maxlen - filter out words that have more characters than 'maxlen'.
    """
    return tlz.pipe(string,
                    lower,
                    simple_split,
                    filter_longer_than(maxlen),
                    tlz.compose(tlz.concat, map_c(splitter_of_words)),
                    filter_shorter_than(minlen),
                    filter_stopwords,
                    sliding_window_c(n))


@tlz.curry
def ngram(n, string, minlen=3, maxlen=25):
    """
    Creates ngram tuples of size 'n' from 'string'.

    Ex:
        In [2]: list(ngram(n=1, string='Just another example text.'))
        Out[2]: ['another', 'example', 'text']

        In [2]: list(ngram(n=2, string='Just another example text.'))
        Out[2]: ['another_example', 'example_text']

        In [10]: list(ngram(3, 'I needed a longer example text for this example.'))
        Out[10]: ['needed_longer_example', 'longer_example_text', 'example_text_example']

    minlen - filter out words that have fewer characters than 'minlen'.
    maxlen - filter out words that have more characters than 'maxlen'.
    """
    return tlz.pipe(string,
                    ngram_tuples(n, minlen=minlen, maxlen=maxlen),
                    map_c(join_strings("_")))


def unigram(string, **kwargs):
    return ngram(n=1, string=string, **kwargs)


def bigram(string, **kwargs):
    return ngram(n=2, string=string, **kwargs)


def trigram(string, **kwargs):
    return ngram(n=3, string=string, **kwargs)


def uni_and_bigram_tuples(string, minlen=3, maxlen=25):
    return tlz.pipe(string,
                    lower,
                    simple_split,
                    filter_longer_than(maxlen),
                    tlz.compose(tlz.concat, map_c(splitter_of_words)),
                    filter_shorter_than(minlen),
                    filter_stopwords,
                    tuple,
                    tlz.juxt(sliding_window_c(1), sliding_window_c(2)),
                    tlz.interleave,
                    map_c(join_strings("_")))
