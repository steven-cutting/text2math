# -*- coding: utf-8 -*-
__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/13/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"


import sys
import warnings

try:
    import cytoolz as tlz
except ImportError:
    import toolz as tlz

c_map = tlz.curry(tlz.map)


# --
# Specific imports

# Parsing
from xml.dom import minidom

try:
    from bs4 import BeautifulSoup
except ImportError:
    warnings.warn("To use remove_html_bits you should install bs4 and lxml.")


# Encoding issues
try:
    import cchardet as chardet
except:
    import chardet
from unidecode import unidecode
import ftfy


if sys.version_info[0] < 3:
    _STRINGTYPES = (basestring,)
else:
    # temp fix, so that 2.7 support wont break
    unicode = str  # adjusting to python3
    _STRINGTYPES = (str, bytes)


# -----------------------------------------------------------------------------
# Read and parse


def get_text_from_xml_file(filename):
    """
    This is setup for extracting text from the Stackoverflow posts data dump
    that is stored in a xml file.

    Returns a stream of Post bodies (just the text).
    """

    @tlz.curry
    def _get_xml_attr(key, xml_element):
        return xml_element.attributes[key].value

    @tlz.curry
    def _try_to_get_xml_attr(key, xml_element, default=''):
        try:
            return _get_xml_attr(key, xml_element)
        except(KeyError):
            return default

    return tlz.pipe(filename,
                    minidom.parse,  # Not pure
                    lambda layer0: layer0.getElementsByTagName("posts")[0],
                    lambda layer1: layer1.getElementsByTagName("row"),
                    c_map(tlz.juxt(_try_to_get_xml_attr("Title"),
                                   _get_xml_attr("Body"))),
                    c_map(lambda titleAndBody: '\n\n\n'.join(titleAndBody)))


def remove_html_bits(text):
    """
    Removes html tags form text.
    """
    return BeautifulSoup(text, "lxml").text


# -----------------------------------------------------------------------------
# Encoding Issues


def verify_unicode(text):
    """
    Asserts text is unicode.

    Returns text after checking.
    """
    assert(isinstance(text, unicode))
    return text


def verify_bytestring(text):
    """
    Asserts text is byte string (not unicode).

    Returns text after checking.
    """
    # If text is a string and it is not unicode then it must be a byte string.
    assert(isinstance(text, _STRINGTYPES))
    assert(not isinstance(text, unicode))
    return text


def clean_unicode(text):
    """
    Cleans it, fixes past decode/encode mistakes, standardizes
    the Unicode scheme.
    """
    return ftfy.fix_text(text, normalization='NFKC')


def normize_text(text):
    """
    Normalizes characters and converts all to
    best matching ASCII representation.

    Expects text to be Unicode.
    (returned text is still Unicode)
    """
    return tlz.pipe(text,
                    verify_unicode,
                    unidecode,
                    unicode)


def std_decode(text, encoding='utf-8', errors='strict'):
    """
    Standardized interface to standard python string decode method.

    Only accepts byte string.
    """
    return tlz.pipe(text,
                    verify_bytestring,
                    lambda txt: txt.decode(encoding=encoding, errors=errors))


def guess_encoding(text):
    """
    Uses chardet to try and make a best guess as to the strings encoding.
    """
    return chardet.detect(text).get('encoding')


@tlz.curry
def adv_decode(text, encoding='utf-8', errors='strict'):
    """
    Byte String to Unicode, if already Unicode it just returns 'text' as is.
    If it fails to decode using the provided encoding it tries to guess what
    the correct encoding is and it attempts to decode 'text' again but
    with more liberal error handling. (replace instead of strict)
    """
    if isinstance(text, unicode):
        return text
    else:
        try:
            return std_decode(text, encoding=encoding, errors=errors)
        except(UnicodeDecodeError, LookupError):
            guessed_encoding = guess_encoding(text)
            if (errors == 'replace') and (encoding == guess_encoding):
                # Nothing left to try, re-raise error.
                raise
            return adv_decode(text, encoding=guessed_encoding, errors='replace')


def decode_and_fix(text, encoding='utf-8'):
    """
    First applies a liberal decode method to the text in which it
    """
    return tlz.pipe(text,
                    adv_decode(encoding=encoding),
                    clean_unicode,
                    normize_text)
