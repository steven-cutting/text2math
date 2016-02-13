FROM pypy:2-4
MAINTAINER steven.e.cutting@linux.com

RUN pip install --upgrade pip
RUN pip install pytest toolz pytest-runner

VOLUME /app

WORKDIR /app

CMD ["/app/docker/test_pypy2/docker_pytest.sh"]
