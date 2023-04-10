#FROM ubuntu:20.04
FROM python:3.9
SHELL ["/bin/bash","-x","-e","-c"]
RUN apt-get -y update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install libssl-dev g++ graphviz-dev libtool make automake autoconf libsqlite3-dev libpython3-dev libyaml-dev libcurl4 dnsutils nano graphviz gcc jq libjq-dev git wget libpq-dev curl dnsutils nano docker dos2unix uuid-runtime zlib1g-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
RUN apt-get -y install rustc
RUN pip3 install virtualenv
RUN pip3 install setuptools-rust
RUN virtualenv -p $(which python3) /opt/venv
ADD ./ /opt/sprout
WORKDIR /opt/sprout
RUN source /opt/venv/bin/activate &&\
  pip3 install setuptools &&\
  pip3 install setuptools-rust &&\
  python3 -m pip install ./
