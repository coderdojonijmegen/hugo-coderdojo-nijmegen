FROM ubuntu:22.04

ENV TZ=Europe/Amsterdam

COPY ./requirements.txt /requirements.txt
RUN apt update && apt install -y \
	git \
	tar \
	wget \
	python3 \
	python3-pip \
	nano \
	&& rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install -r requirements.txt

ENV INPUT_HUGOVERSION extended_0.111.3

COPY ./entrypoint.sh /entrypoint.sh
COPY src/ /src/

ENTRYPOINT [ "/entrypoint.sh" ]
