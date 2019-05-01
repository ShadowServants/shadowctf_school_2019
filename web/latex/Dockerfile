FROM python:3.6-jessie

RUN apt-get update && apt-get install -y \
    sqlite \
    texlive-latex-base

COPY latex app
RUN pip install --no-cache-dir -r app/requirements.txt
WORKDIR /app
COPY flag.txt /flag.txt