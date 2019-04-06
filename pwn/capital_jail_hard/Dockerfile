FROM python:3.7-alpine

RUN apk add socat

RUN mkdir /app

ADD ./server.py /app/server.py
RUN chmod +x /app/server.py

RUN addgroup -S task
RUN adduser -S -G task task

ADD flag_003f1c8109461ad4b338b1a2ea1f6c32.txt /flag_003f1c8109461ad4b338b1a2ea1f6c32.txt
RUN chown root:task /flag_003f1c8109461ad4b338b1a2ea1f6c32.txt
RUN chmod 644 /flag_003f1c8109461ad4b338b1a2ea1f6c32.txt

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER task

CMD ["/entrypoint.sh"]