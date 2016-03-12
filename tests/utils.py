__title__ = 'text2math'
__author__ = 'Steven Cutting'
__author_email__ = 'steven.e.cutting@linux.com'
__created_on__ = '03/11/2016'
__copyright__ = "text2math Copyright (C) 2016  Steven Cutting"


import sys

import pytest


py3_xfail = pytest.mark.xfail(sys.version_info >= (3, 0),
                              reason="Doesn't work in python 3+.")
