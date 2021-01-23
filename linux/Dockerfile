## 设置基础镜像
FROM selenium/standalone-chrome

LABEL auther="magicwenli"
LABEL Descripttion = "This image is build for daily-check-xjtu" Vendor="GitHub" Version="latest"

## 设置镜像制作过程中，需要执行的命令
RUN cd ~
RUN sudo apt-get update
RUN sudo apt-get -y install vim python3 python3-pip git
RUN pip3 install -r requirements.txt
RUN cat cron.txt > /etc/crontab
COPY ./* .
RUN chmod 777 daily-check-xjtu.py

