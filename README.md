# daily-check-xjtu


## 功能

* 使用python3编写的一个小程序，可以帮你每天自动打卡  
* 多用户
* 微信推送（基于wxpusher）
* 支持定时任务

## 使用须知
* 使用者应结合当地防控情况审慎使用本工具
* 使用者应当每日自觉确认身体情况，并在出现不可控因素时及时向当地有关部门及学校通报。

---------------

* **使用前需手动打卡过**，确保除体温及健康码颜色之外的其他信息能自动加载  
* 在 Windows 10 ltsc 下测试通过
* 在 ubuntu18.04 下测试通过


## 部署方法

### linux

see [Linux version](linux/README.md)

### windows
1. 安装Chrome
2. 前往 https://chromedriver.storage.googleapis.com/index.html 下载最新Chrome自动控制驱动，解压后放到系统环境变量目录下（如C:\windows\system32\）

3. 运行addSchTask.bat添加每日两次的计划任务（也可以自行添加计划任务）
4. 注册wxpusher开发者，创建应用和主题，取得appToken，用户pid和主题号
5. 编辑check.py填写相关信息
