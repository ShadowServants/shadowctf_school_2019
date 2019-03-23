FROM alpine:3.8

RUN apk update && apk add --no-cache socat g++
COPY main.cpp main.cpp
RUN g++ main.cpp -o app
