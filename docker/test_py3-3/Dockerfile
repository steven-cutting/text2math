FROM python:3.3
MAINTAINER steven.e.cutting@linux.com

RUN pip install --upgrade pip
RUN pip install pytest toolz pytest-runner
RUN pip install cchardet ftfy unidecode beautifulsoup4 cytoolz lxml

VOLUME /app

WORKDIR /app

CMD ["/app/docker/test_py3-3/docker_pytest.sh"]
