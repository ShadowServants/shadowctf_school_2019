FROM ubuntu
RUN apt-get update && apt-get install -y socat
RUN useradd -s /bin/bash pwner
ADD task /app
RUN chmod +x /app/anime
WORKDIR /app
USER pwner
ENTRYPOINT ["socat", "TCP4-LISTEN:7777,reuseaddr,fork", "EXEC:./anime"]