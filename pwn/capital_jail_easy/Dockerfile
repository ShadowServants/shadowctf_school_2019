FROM python:3.7-alpine

RUN apk add socat

RUN mkdir /app

ADD ./server.py /app/server.py
RUN chmod +x /app/server.py

RUN addgroup -S task
RUN adduser -S -G task task

ADD ./flag_3e0db8951b894a433bb147e9c250b6d5.txt /flag_3e0db8951b894a433bb147e9c250b6d5.txt
RUN chown root:task /flag_3e0db8951b894a433bb147e9c250b6d5.txt
RUN chmod 644 /flag_3e0db8951b894a433bb147e9c250b6d5.txt

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER task

CMD ["/entrypoint.sh"]