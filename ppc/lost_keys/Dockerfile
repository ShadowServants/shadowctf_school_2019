FROM python:3.7-alpine

RUN apk add gcc musl-dev gmp-dev mpfr-dev mpc1-dev socat

ADD ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD ./ /app
RUN chmod +x /app/server.py

CMD ["/entrypoint.sh"]