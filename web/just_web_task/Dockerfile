FROM python:3.7-alpine
RUN apk update && apk add --no-cache gcc musl-dev zlib-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD app /app
