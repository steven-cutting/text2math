# -*- coding: utf-8 -*-
__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/13/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"

from operator import eq

import pytest
import cytoolz as tlz
c_eq = tlz.curry(eq)

from text2math import raw2text

from utils import osx_xfail


@pytest.mark.parametrize("string,expected",
                         [("<p>foo<\p><li>bar<\li>", "foobar"),
                          ])
def test__remove_html_bits(string, expected):
    assert(tlz.pipe(string,
                    raw2text.remove_html_bits,
                    c_eq(expected)))


def test__verify_unicode_fail():
    with pytest.raises(AssertionError):
        raw2text.verify_unicode(b"not unicode")


def test__verify_unicode_pass():
    raw2text.verify_unicode(u"unicode")


@pytest.mark.parametrize("wrong_arg",
                         [(u"not bytestring"),
                          (2344352),
                          ([b"sfsddf", b"sfsdf"]),
                          ([b"sfsddf"]),
                          ])
def test__verify_bytestring_fail(wrong_arg):
    with pytest.raises(AssertionError):
        raw2text.verify_bytestring(wrong_arg)


def test__verify_bytestring_pass():
    raw2text.verify_bytestring(b"bytestring")


# Examples from https://github.com/LuminosoInsight/python-ftfy
@pytest.mark.parametrize("string,expected",
                         [(u'This text should be in â€œquotesâ€\x9d.',
                           u'This text should be in "quotes".'),
                          # expected to fail on OSX
                          (u'30 \U0001d5c4\U0001d5c6/\U0001d5c1', u'30 km/h'),
                          (u'uÌˆnicode', u'ünicode'),
                          (u'HTML entities &lt;3',
                           u'HTML entities <3'),
                          (u'<em>HTML entities in HTML &lt;3</em>',
                           u'<em>HTML entities in HTML &lt;3</em>'),
                          (u"Broken text&hellip; it&#x2019;s ﬂubberiﬁc!",
                           u"Broken text... it's flubberific!"),
                          (u"™", u"TM"),
                          (u"H₂O", u"H2O"),
                          ])
def test__clean_unicode(string, expected):
    assert(tlz.pipe(string,
                    raw2text.clean_unicode,
                    c_eq(expected)))


# Examples from https://pypi.python.org/pypi/Unidecode/
@pytest.mark.parametrize("string,expected",
                         [(u'ko\u017eu\u0161\u010dek', u'kozuscek'),
                          # expected to fail on OSX
                          (u'30 \U0001d5c4\U0001d5c6/\U0001d5c1', u'30 km/h'),
                          (u"\u5317\u4EB0", 'Bei Jing '),
                          ])
def test__normize_text(string, expected):
    assert(tlz.pipe(string,
                    raw2text.normize_text,
                    c_eq(expected)))


@pytest.mark.parametrize("string,encoding,expected",
                         [(u"foo".encode("utf-8"), "utf-8", "foo"),
                          (u"foo".encode("ascii"), "ascii", "foo"),
                          (u"foo".encode("utf-32"), "utf-32", "foo"),
                          (u'ünicode'.encode("iso-8859-2"), "iso-8859-2", u'ünicode'),
                          (u'ünicode'.encode("utf-8"), "utf-8", u'ünicode'),
                          ])
def test__std_decode(string, encoding, expected):
    assert(tlz.pipe(string,
                    lambda txt: raw2text.std_decode(txt, encoding=encoding),
                    c_eq(expected)))


@pytest.mark.parametrize("string,acceptable",
                         [(u"foo".encode("utf-8"), ("utf-8", "ascii")),
                          (u"foo".encode("ascii"), ("ascii", )),
                          (u'ünicode'.encode("utf-8"), ("utf-8", 'iso-8859-2')),
                          ])
def test__guess_encoding(string, acceptable):
    guessed = tlz.pipe(string,
                       raw2text.guess_encoding,
                       lambda txt: txt.lower())
    assert(guessed in acceptable)


@pytest.mark.parametrize("string,encoding,expected",
                         [(u"foo".encode("utf-8"), "utf-8", u"foo"),
                          (u"foo".encode("ascii"), "ascii", u"foo"),
                          (u"foo".encode("utf-32"), "utf-32", u"foo"),
                          (u'ünicode'.encode("utf-8"), "utf-8", u'ünicode'),
                          (u'ünicode'.encode("utf-32"), "utf-32", u'ünicode'),
                          (u"foo".encode("ascii"), "utf-8", u"foo"),
                          (u'ünicode'.encode("utf-8"), "utf-8", u'ünicode'),
                          (u'ünicode'.encode("iso-8859-2"), "utf-8", u'ünicode'),
                          ])
def test__adv_decode(string, encoding, expected):
    decoded = raw2text.adv_decode(string, encoding=encoding)
    assert(decoded == expected)


@pytest.mark.parametrize("string,expected",
                         [(u'ko\u017eu\u0161\u010dek'.encode("utf-8"),
                           u'kozuscek'),
                          osx_xfail((u'30 \U0001d5c4\U0001d5c6/\U0001d5c1'.encode("utf-8"),
                                     u'30 km/h')),  # Find out why it fails on OSX.
                          (u"\u5317\u4EB0".encode("utf-8"), 'Bei Jing '),
                          (u"Broken text&hellip; it&#x2019;s ﬂubberiﬁc!".encode("utf-8"),
                           u"Broken text... it's flubberific!"),
                          (u"™".encode("utf-8"), u"TM"),
                          (u"H₂O".encode("utf-8"), u"H2O"),
                          (u"Broken text&hellip; it&#x2019;s ﬂubberiﬁc!".encode("utf-16"),
                           u"Broken text... it's flubberific!"),
                          (u"™".encode("utf-16"), u"TM"),
                          (u"H₂O".encode("utf-16"), u"H2O"),
                          (u"foo".encode("iso-8859-2"), u"foo"),
                          (u"foo".encode("windows-1250"), u"foo"),
                          (u"foo".encode("IBM850"), u"foo"),
                          ])
def test__decode_and_fix(string, expected):
    decoded = raw2text.decode_and_fix(string)
    assert(decoded == expected)
