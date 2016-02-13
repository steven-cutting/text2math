__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/13/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"


from text2math import tokens2numbers as tkn2num

import pytest
import toolz as tlz
reduce_c = tlz.curry(tlz.reduce)


sum_tally_tuples = lambda tpls: reduce_c(lambda x, y: x+y[1], tpls, 0)
EXTEXT = tlz.reduce(lambda x, y: x+y, ["aaa " * 20,
                                       "bbb " * 10,
                                       "ccc " * 3,
                                       "ddd " * 1])


@pytest.mark.parametrize("tokenset,length,total",
                         [(tlz.concatv(["a"] * 20,
                                       ["b"] * 10,
                                       ["c"] * 3,
                                       ["d"] * 1,
                                       ), 4, 34),

                          ])
def test__freq(tokenset, length, total):
    bow = tkn2num.freq(tokenset)
    assert(len(bow) == length)
    assert(sum_tally_tuples(bow) == total)


# -----------------------------------------------------------------------------


@pytest.mark.parametrize("string,length,total,parser",
                         [(EXTEXT, 4, 34, tkn2num.uni_gram),

                          ])
def test___gram_counts(string, length, total, parser):
    bow = tkn2num.gram_counts(parser, string)
    assert(len(bow) == length)
    assert(sum_tally_tuples(bow) == total)


@pytest.mark.parametrize("string,length,total",
                         [(EXTEXT, 4, 34),

                          ])
def test__uni_gram_counts(string, length, total):
    bow = tkn2num.uni_gram_counts(string)
    assert(len(bow) == length)
    assert(sum_tally_tuples(bow) == total)


@pytest.mark.parametrize("string,length,total",
                         [(EXTEXT, 6, 33),

                          ])
def test__bi_gram_counts(string, length, total):
    bow = tkn2num.bi_gram_counts(string)
    assert(len(bow) == length)
    assert(sum_tally_tuples(bow) == total)


@pytest.mark.parametrize("string,length,total",
                         [(EXTEXT, 8, 32),

                          ])
def test__tri_gram_counts(string, length, total):
    bow = tkn2num.tri_gram_counts(string)
    assert(len(bow) == length)
    assert(sum_tally_tuples(bow) == total)


@pytest.mark.parametrize("wordcounts,exbow,exdict",
                         [([("aaa", 20),
                            ("bbb", 10),
                            ("ccc", 3),
                            ("ddd", 1)],
                           [(0, 20),
                            (1, 10),
                            (2, 3),
                            (3, 1)],
                           {0: "aaa", 1: "bbb",
                            2: "ccc", 3: "ddd"}),
                          ])
def test__bag_of_words(wordcounts, exbow, exdict):
    bow, dict_ = tkn2num.bag_of_words(wordcounts)
    assert(bow == exbow)
    assert(dict_ == exdict)


@pytest.mark.parametrize("string,excounts,parser",
                         [(EXTEXT,
                           [("aaa", 20),
                            ("bbb", 10),
                            ("ccc", 3),
                            ("ddd", 1)],
                           tkn2num.uni_gram),
                          (EXTEXT,
                           [("aaa_aaa", 19),
                            ("aaa_bbb", 1),
                            ("bbb_bbb", 9),
                            ("bbb_ccc", 1),
                            ("ccc_ccc", 2),
                            ("ccc_ddd", 1)],
                           tkn2num.bi_gram),
                          ])
def test__text_to_bow(string, excounts, parser):
    t2bow = tkn2num.text_to_bow(parser)  # testing ability to curry
    bow, dict_ = t2bow(string)
    gram2count = sorted([(dict_[i], c) for i, c in bow], key=tlz.first)
    assert(gram2count == excounts)


@pytest.mark.parametrize("string,excounts",
                         [(EXTEXT,
                           [("aaa", 20),
                            ("bbb", 10),
                            ("ccc", 3),
                            ("ddd", 1)]),
                          ])
def test__text_to_uni_bow(string, excounts):
    bow, dict_ = tkn2num.text_to_uni_bow(string)
    gram2count = sorted([(dict_[i], c) for i, c in bow], key=tlz.first)
    assert(gram2count == excounts)


@pytest.mark.parametrize("string,excounts",
                         [(EXTEXT,
                           [("aaa_aaa", 19),
                            ("aaa_bbb", 1),
                            ("bbb_bbb", 9),
                            ("bbb_ccc", 1),
                            ("ccc_ccc", 2),
                            ("ccc_ddd", 1)]),
                          ])
def test__text_to_bi_bow(string, excounts):
    bow, dict_ = tkn2num.text_to_bi_bow(string)
    gram2count = sorted([(dict_[i], c) for i, c in bow], key=tlz.first)
    assert(gram2count == excounts)
