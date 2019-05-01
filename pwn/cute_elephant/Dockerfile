FROM ubuntu:16.04

RUN apt-get update && apt-get install -y postgresql postgresql-contrib socat

ADD ./flag.txt /flag.txt
RUN groupadd task

RUN chown root:task /flag.txt
RUN chmod 740 /flag.txt

RUN usermod -aG task postgres

ADD ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
