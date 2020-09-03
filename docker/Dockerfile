FROM python:3-slim

LABEL author="Saishiva K (@saishivarcr)" \
    version="1.0"

ENV path /dellemc
RUN mkdir $path
WORKDIR $path

RUN pip install "ansible<2.10" omsdk

ADD https://github.com/dell/dellemc-openmanage-ansible-modules/archive/devel.tar.gz .

RUN tar -xvf devel.tar.gz && \
    cd dellemc-openmanage-ansible-modules-devel && \
    python install.py

VOLUME [$path]

ENTRYPOINT ["/usr/local/bin/ansible-playbook"]
