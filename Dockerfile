FROM python:3.9.0
MAINTAINER "Naveen Dharmathunga <dnd.pro@outlook.com>"
ARG BUILD_DATE
ARG VCS_REF

ENV DOCKER_BUILD_DATE=$BUILD_DATE
ENV DOCKER_VCS_REF=$VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/DukeX9/David-TelegramBot-Docker" \
      org.label-schema.vcs-ref=$VCS_REF

RUN apt-get update; apt-get install -y openssl

COPY requirements.txt /projects/py/telebot/

RUN cd /projects/py/telebot && pip install --no-cache-dir -r requirements.txt
COPY . /projects/py/telebot

WORKDIR /projects/py/telebot

VOLUME /projects/py/telebot/certs
VOLUME /projects/py/telebot/res

CMD [ "scripts/start.sh" ]