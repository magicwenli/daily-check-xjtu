FROM selenium/standalone-chrome:latest

LABEL auther="magicwenli"
LABEL Descripttion = "This image is build for daily-check-xjtu" Vendor="GitHub" Version="latest"

RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends \
         vim python3 python3-pip git cron && \
    sudo apt-get clean

RUN pip3 install selenium wxpusher
