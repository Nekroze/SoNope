FROM python:3

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./sonope/cli.py /usr/local/bin/sonope
WORKDIR /
COPY ./blacklist.csv /blacklist.csv

ENTRYPOINT ["/usr/local/bin/sonope"]
CMD ["-b=blacklist.csv"]
