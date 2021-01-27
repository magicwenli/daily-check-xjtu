# Linux version
> 使用 Docker 搭建

### 克隆本仓库

```shell
git clone https://github.com/magicwenli/daily-check-xjtu.git
```

### 修改参数

```shell
cd daily-check-xjtu
vim linux/dailycheck/daily-check.py
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

### 拉取并运行

```shell
sudo docker run -d --name dcheck -p 4444:4444  -v /dev/shm:/dev/shm yangwesley/daily-check:v2
```
运行完成后等待1~2分钟。

接下来进入容器，运行启动脚本`entrypoint.sh`

```shell
sudo docker exec -it dcheck bash
sh /opt/dailycheck/entrypoint.sh
exit
```

### 后续修改
修改主机`/opt/dailycheck`中的配置，然后进入容器运行`entrypoint.sh`。
