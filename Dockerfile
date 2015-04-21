FROM natemara/docker-utopic-python3

ADD . /app
WORKDIR /app
RUN python3 setup.py install

ENTRYPOINT python3 setup.py test
