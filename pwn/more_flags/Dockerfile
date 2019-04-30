FROM debian:stretch
RUN useradd -ms /bin/bash admin
ADD .gotty /home/admin/
ADD gotty /bin/gotty
RUN chmod +x /bin/gotty
RUN mv /bin/rm /dev/null
ADD task /app
RUN chmod -R 555 /app
WORKDIR /app
USER admin
#ENTRYPOINT ["/usr/local/bin/gotty"]
#CMD ["--permit-write","--reconnect","/bin/sh"]
