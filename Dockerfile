FROM python:3

RUN mkdir /workdir
ADD . /workdir/
WORKDIR /workdir
RUN python setup.py build
RUN python setup.py install
