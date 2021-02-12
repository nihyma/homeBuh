FROM python:3.9-slim
ARG BUILD_REPO=nihyma/homeBuh
ARG BUILD_BRANCH=main

LABEL build_repo=$BUILD_REPO build_branch=$BUILD_BRANCH
LABEL Author="nihyma"

RUN apt-get update && apt-get install -y wget
RUN wget -O - --no-check-certificate https://github.com/nihyma/homeBuh/archive/main.tar.gz | tar -xz
RUN mv homeBuh-main homeBuh
WORKDIR /homeBuh
RUN pip install -r requirements.txt
WORKDIR /homeBuh/app
VOLUME /config
CMD ["python", "app.py -c /config/config.yml"]