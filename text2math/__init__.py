__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/06/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"

try:
    import cytoolz as tlz
except ImportError:
    import toolz as tlz

from text2math.raw2text import(remove_html_bits, decode_and_fix, adv_decode)
from text2math.text2tokens import(ngram, unigram, bigram, trigram,
                                  uni_and_bigram_tuples)
from text2math.tokens2numbers import freq


tknize_uni_n_bi = tlz.compose(tuple,
                              uni_and_bigram_tuples,
                              decode_and_fix,
                              remove_html_bits)

total_counts = tlz.compose(freq, tlz.concat)
