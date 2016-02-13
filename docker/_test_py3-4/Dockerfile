FROM python:3.4
MAINTAINER steven.e.cutting@linux.com

RUN pip install --upgrade pip
RUN pip install pytest toolz pytest-runner

VOLUME /app

WORKDIR /app

CMD ["/app/docker/test_py3-4/docker_pytest.sh"]
