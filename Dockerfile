FROM selenium/standalone-chrome
USER root
RUN apt update &&  apt -y install --no-install-recommends python3-pip nmap && \
    pip3 install selenium setuptools wheel python-nmap requests
USER seluser