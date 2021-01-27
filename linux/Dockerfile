## 设置基础镜像
FROM selenium/standalone-chrome:3.141.59-zirconium

LABEL auther="magicwenli"
LABEL Descripttion = "This image is build for daily-check-xjtu" Vendor="GitHub" Version="latest"

## docker build -t yangwesley/daily-check:v2 .
## docker run -d --name dcheck -p 4444:4444 -v /dev/shm:/dev/shm yangwesley/daily-check:v2

WORKDIR /home/seluser
## 设置镜像制作过程中，需要执行的命令
RUN sudo apt-get update && \
    sudo apt-get install -y --no-install-recommends \
         vim python3 python3-pip git cron && \
    sudo apt-get clean
VOLUME /opt/dailycheck
ADD dailycheck/ /opt/dailycheck/
RUN pip3 install -r /opt/dailycheck/requirements.txt
ADD ./entrypoint.sh /opt/dailycheck/

# ENTRYPOINT ["sh","/opt/dailycheck/entrypoint.sh" ]
