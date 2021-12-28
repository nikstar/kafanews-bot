FROM python:3.8.10-alpine

RUN pip install feedparser

WORKDIR /workdir
COPY ./main.py .

CMD python main.py