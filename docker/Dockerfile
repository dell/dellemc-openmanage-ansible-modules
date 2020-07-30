FROM python:3
LABEL maintainer="OpenManageAnsible@Dell.com"

ENV version 2.1-master
ENV path /dellemc
RUN mkdir $path
WORKDIR $path

RUN pip install ansible omsdk

RUN curl -sL https://github.com/dell/dellemc-openmanage-ansible-modules/archive/v$version.tar.gz | \
    tar xz && \
    cd dellemc-openmanage-ansible-modules-$version && \
    python install.py

VOLUME [$path]

ENTRYPOINT ["/usr/local/bin/ansible-playbook"]
