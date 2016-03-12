"""
text2math Copyright (C) 2016  Steven Cutting
"""


from setuptools import setup, find_packages

with open("README.md") as fp:
    THE_LONG_DESCRIPTION = fp.read()

PACKAGES = ['text2math']


setup(
    name="text2math",
    version="0.1.0",
    license='GNU GPL v3+',
    description="Simple package for generating ngrams and bag of words representation from text.",
    long_description=THE_LONG_DESCRIPTION,
    classifiers=['Topic :: NLP',
                 'Topic :: Text processing',
                 'Topic :: text munging',
                 'Topic :: data munging',
                 'Topic :: feature engineering',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Data Scientists',
                 'Operating System :: GNU Linux',
                 'Operating System :: OSX :: MacOS :: MacOS X',
                 'Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'License :: GNU GPL v3+',
                 'Status :: ' + "pre-alpha",
                 ],
    keywords='nlp text ngram ngrams',
    author='Steven Cutting',
    author_email='steven.e.cutting@linux.com',
    packages=find_packages(exclude=('scripts', 'tests')),
    # scripts=['bin/word-counts', 'bin/text-2-bow'],
    install_requires=['toolz>=0.7.4',
                      'cchardet>=1.0.0',
                      'unidecode>=0.04.19',
                      ],
    setup_requires=['pytest-runner>=2.6.2'],
    tests_require=['pytest>=2.8.7'],
    )
