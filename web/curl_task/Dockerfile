FROM python:3.7-alpine
# EXPOSE 5000:5000
RUN apk add curl
RUN apk add bash
RUN pip3 install flask
ADD . /code
WORKDIR /code
# RUN chmod 750 -R /
RUN chmod -R o=rt /code/
RUN chmod o=rxt /code/
RUN chmod o=rxt -R templates
RUN rm Dockerfile
RUN mv /bin/rm /dev/null
# RUN chmod 444 /bin/rm
RUN adduser -H -D user
USER user
CMD ["python3", "main.py"]

