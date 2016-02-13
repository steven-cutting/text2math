__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '02/13/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"


import toolz as tlz


def freq(tokenset):
    """
    Find number of occurrences of each value 'tokenset'.
    """
    return tlz.pipe(tokenset,
                    tlz.frequencies,
                    dict.items)


def corpus_freq(tokensets):
    return tlz.map(freq, tokensets)
