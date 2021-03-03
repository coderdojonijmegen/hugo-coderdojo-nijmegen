FROM ubuntu:20.04

RUN apt update && apt install -y \
	git \
	tar \
	wget \
	python3 \
	python3-pip \
	nano \
	&& rm -rf /var/lib/apt/lists/*

ENV INPUT_HUGOVERSION extended_0.74.0

COPY ./entrypoint.sh /entrypoint.sh
COPY ./deploy.py /deploy.py
COPY ./dojo.py /dojo.py
COPY ./requirements.txt /requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]
