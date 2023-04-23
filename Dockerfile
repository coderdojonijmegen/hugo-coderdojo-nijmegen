FROM ubuntu:22.04

ENV TZ=Europe/Amsterdam

RUN apt update && apt install -y \
	git \
	tar \
	wget \
	python3 \
	python3-pip \
	nano \
	&& rm -rf /var/lib/apt/lists/*

ENV INPUT_HUGOVERSION extended_0.111.3

COPY ./entrypoint.sh /entrypoint.sh
COPY deploy.py /deploy.py
COPY utils/ /utils/
COPY ./requirements.txt /requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]
