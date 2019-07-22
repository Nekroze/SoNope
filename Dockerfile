FROM python:3

RUN pip install soco docopt

COPY ./sonope.py /usr/local/bin/sonope
WORKDIR /
COPY ./blacklist.csv /blacklist.csv

ENTRYPOINT ["/usr/local/bin/sonope"]
CMD ["-b=blacklist.csv"]
