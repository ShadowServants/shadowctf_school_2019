FROM python:3.6
RUN apt-get update && apt-get install -y socat python3-pip
RUN pip3 install pycrypto
RUN useradd -s /bin/bash crypter
ADD task /app
RUN chmod +x /app/server.py
WORKDIR /app
USER crypter
ENTRYPOINT ["socat", "TCP4-LISTEN:7777,reuseaddr,fork", "EXEC:./server.py"]