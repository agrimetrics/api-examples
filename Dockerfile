FROM debian:latest AS examples-test-base

RUN apt update
RUN apt install -y python3 python3-pip git
RUN adduser testuser
RUN chown testuser: /opt
RUN pip3 install jupyterlab

FROM examples-test-base AS examples-test-run

WORKDIR /opt
USER testuser
COPY . api-examples
WORKDIR /opt/api-examples

RUN pip3 install -r field-explorer-examples/requirements.txt
RUN pip3 install -r graphql-examples/requirements.txt
RUN pip3 install -r verde-examples/requirements.txt

USER testuser
CMD jupyter notebook --ip 0.0.0.0
