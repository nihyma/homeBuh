FROM python:3.8-slim
ARG BUILD_REPO=nihyma/homeBuh
ARG BUILD_BRANCH=master

LABEL build_repo=$BUILD_REPO build_branch=$BUILD_BRANCH
LABEL Author="nihyma"

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
VOLUME /config
CMD ["python", "app.py"]

