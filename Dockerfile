FROM ubuntu:22.04

ENV TZ=Europe/Amsterdam

COPY ./entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /requirements.txt
RUN apt update && apt install -y \
        git \
        tar \
        wget \
        python3 \
        python3-pip \
        nano \
	&& rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install -r requirements.txt \
    && mkdir /site

ENV INPUT_HUGOVERSION extended_0.123.8

ENTRYPOINT [ "/entrypoint.sh" ]
