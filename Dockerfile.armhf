FROM arm32v7/alpine:latest
ARG BUILD_REPO=nihyma/homeBuh
ARG BUILD_BRANCH=main

LABEL build_repo=$BUILD_REPO build_branch=$BUILD_BRANCH
LABEL Author="nihyma"


RUN wget -O - --no-check-certificate https://github.com/nihyma/homeBuh/archive/main.tar.gz | tar -xz
RUN mv homeBuh-main homeBuh

WORKDIR /homeBuh
ADD requirements.txt /homeBuh

RUN apk --no-cache update \
&& apk --no-cache upgrade \
&& apk add --no-cache py-pip \
&& apk add --no-cache zlib-dev \
&& apk add --no-cache libjpeg-turbo-dev \
&& apk add --no-cache build-base \
&& apk add --no-cache python3-dev \
&& pip3 install --no-cache-dir -r requirements.txt \
&& apk del --no-cache python3-dev \
&& apk del --no-cache build-base \
&& apk del --no-cache zlib-dev \
&& pip3 uninstall --no-cache-dir -y setuptools \
&& rm -f /usr/lib/libsqlite* \
&& rm -f /lib/libcrypto* \
&& rm -f /lib/libssl* \
&& rm -rf /var/lib/apt/lists/*

VOLUME /config
WORKDIR /homeBuh/app
CMD python3 main.py -c /config/config.yml
