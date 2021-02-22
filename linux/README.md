# Linux version
> 使用 Docker 搭建

需求：
- python3
  - selenium, wxpusher
- docker

## 克隆本仓库

```shell
git clone https://github.com/magicwenli/daily-check-xjtu.git 
```

## 建立文件夹并修改参数

```shell
mv daily-check-xjtu/linux /opt/daily-check-xjtu
chmod -R 777 /opt/daily-check-xjtu

cd /opt/daily-check-xjtu
vim daily-check.py
```
**XJTU OAuth 部分**

账号和密码都需要预先使用BASE64编码再填入，支持多账号，例如

```python
ua = ['YmFzZTY0PXhqdHU=', 'eGp0dT1iYXNlNjQ=']
pd = ['6K+36L6T5YWl6KaB', '57yW56CB5oiW6Kej']
```
**Wxpusher 部分**

按照[官方网站](https://wxpusher.zjiecode.com/)的说明进行注册。

需要的部分是用户UID、主题TopicId和appToken。

**定时任务部分**

修改cron.txt为想要定时任务的时间。

## 拉取并运行

```shell
sudo docker run -d --name dcheck -p 4444:4444 -v /opt/dailycheck:/dailycheck -v /dev/shm:/dev/shm yangwesley/daily-check:latest
```

安装`selenium`和`wxpusher`
```shell
pip3 install selenium wxpusher
```

接下来启动脚本`entrypoint.sh`

```shell
sudo bash /daily-check-xjtu/entrypoint.sh
```

## 后续修改
修改`/opt/daily-check-xjtu`中的配置，然后运行`entrypoint.sh`。
