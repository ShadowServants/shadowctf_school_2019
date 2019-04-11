FROM python:3.7-alpine
# EXPOSE 5000:5000
RUN apk add curl
RUN apk add bash
RUN pip3 install flask
RUN apk add gcc musl-dev zlib-dev
RUN pip3 install gunicorn gevent
ADD . /code
WORKDIR /code
# RUN chmod 750 -R /
RUN chmod -R o=rt /code/
RUN chmod o=rxt /code/
RUN chmod o=rxt -R templates
RUN rm Dockerfile
RUN apk add gcc musl-dev zlib-dev
RUN pip3 install gunicorn gevent
RUN mv /bin/rm /dev/null
# RUN chmod 444 /bin/rm
RUN adduser -H -D user
USER user
# CMD ["python3", "main.py"]
CMD ["gunicorn", "--worker-class",  "gevent", "--worker-connections", "768", "--bind", "0.0.0.0:5000", "main:app"]
