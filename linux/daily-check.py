'''
Author       : magicwenli
Date         : 2021-01-07 20:35:58
LastEditTime : 2021-02-21 16:13:58
Description  : 多用户自动打卡脚本
                  使用 wxpusher 进行微信推送
                  Forked from JerryYang666/XJTU-DHA-auto-complete
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time,base64,random,signal
from wxpusher import WxPusher


######### XJTU OAuth
# username with BASE64 encoding
ua = ['a', 'b', 'c']
# password with BASE64 encoding
pd = ['d', 'e', 'f']
#########


######### Wxpusher
appToken = 'AT_1x'
pid = ['UID_a',
       'UID_b','UID_c']
themeIds = [123]
#########

# 登录页面，带参跳转
url = "http://wxpusher.zjiecode.com/api/send/message"
login = "http://jkrb.xjtu.edu.cn/EIP/user/index.htm"

temperature = '0'
tryNum = 1


def set_timeout(num):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                print('start alarm signal.')
                r = func(*args)
                print('close alarm signal.')
                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                return "超时啦"
        return to_do

    return wrap


# 西交SSO登录操作
@set_timeout(15)  # 限时修饰器，仅在windows下有用，linux需要使用SIGNAL系统调用
def user_login(account, password, url, driver):
    driver.get(url)
    driver.implicitly_wait(5)  # 等待浏览器渲染js文件
    driver.find_element_by_xpath(
        '//*[@id="form1"]/input[1]').send_keys(account)  # 输入用户名密码
    driver.find_element_by_xpath(
        '//*[@id="form1"]/input[2]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="account_login"]').click()  # 点击登录按钮
    driver.implicitly_wait(5)

# 健康报打卡操作
@set_timeout(30)
def daka(driver):
    global temperature
    driver.implicitly_wait(3)
    # driver.find_element_by_link_text(u'本科生每日健康状况填报').click()
    # driver.find_element_by_xpath('//*[@id="form"]/div[2]/div/ul[1]/li[2]/div/a').click()
    driver.switch_to.frame(driver.find_element_by_xpath(
        '//*[@id="mini-17$body$2"]/iframe'))  # 进入页面主框架
    driver.switch_to.frame(1)  # 进入二级框架
    driver.find_element_by_xpath(
        '//*[text()="本科生每日健康状况填报"]').click()  # 更新-尽量避免使用index确定按钮位置
    # driver.execute_script('document.getElementsByClassName("service-hall-box-top-hover")[1].click()') #执行JavaScript点击“本科生每日健康状况填报”按钮
    time.sleep(5)
    driver.switch_to.default_content()  # 回退到页面主框架外
    driver.switch_to.frame(driver.find_element_by_xpath(
        '//*[@id="mini-17$body$3"]/iframe'))  # 进入标签页框架
    # 调试使用“漏填健康日报补录”，调试结束后改为“每日健康填报”
    driver.find_element_by_xpath('//*[text()="每日健康填报"]').click()
    # driver.execute_script('document.getElementsByClassName("bl-item bl-link active")[0].click()') #js点击“每日健康填报”按钮（按钮位置index可能改变）
    time.sleep(6)
    if checkDakaStat(driver):
        temperature = '0'
    else:
        # 开始打卡-todo
        driver.switch_to.default_content()  # 回退到页面主框架外
        driver.switch_to.frame(driver.find_element_by_xpath(
            '//*[@id="mini-17$body$4"]/iframe'))  # 进入标签页框架
        driver.switch_to.frame(0)  # 进入表格二级框架
        # Step1 选择绿码选项
        driver.find_element_by_css_selector(
            '[value="绿色"]').click()  # 调试结束改为绿色！！
        # Step2 填入自动生成的体温数值
        temperature = fakeTemperature()
        driver.find_element_by_name('BRTW').send_keys(temperature)
        # Step3 点击提交
        driver.switch_to.parent_frame()  # 退出到表格二级框架外
        driver.execute_script(
            'document.getElementById("sendBtn").click()')  # js点击提交按钮
        driver.find_element_by_xpath('//*[text()="确定"]').click()  # 操控点击确定按钮
        # **在每个打卡时间段结束前1小时可以进行一个遍历检查，console.log返回“每天仅可填报一次，请勿重复！”即可判断自动填报成功


# 自动生成36.0-36.9度之间的一个体温数值
def fakeTemperature():
    decimal = random.randint(0, 9)
    srtDecimal = str(decimal)
    temp = "36." + srtDecimal
    return temp

# 检查打卡状态，console.log返回“每天仅可填报一次，请勿重复！”即可判断自动填报成功

@set_timeout(5)
def checkDakaStat(driver):
    consoleLog = driver.get_log('browser')
    for logs in consoleLog:
        if logs['level'] == 'INFO':
            if logs['message'].find('每天仅可填报一次，请勿重复！') != -1:
                return True
    return False


def push(i, mesNum):
    if mesNum == 0:
        if temperature != '0':
            text = "健康每日报已打卡，生成温度："+temperature+" 度"
        else:
            text = "今日已打卡，无需重复"
    elif mesNum == 1:
        text = '用户'+str(i+1)+'打卡错误，正在第'+str(tryNum)+'次重试...'
    elif mesNum == 2:
        text = '失败次数过多，跳过运行...'
    print(text)
    time.sleep(1)
    WxPusher.send_message(text,
                          uids=[pid[i]],
                          topic_ids=themeIds,
                          token=appToken)

option = webdriver.ChromeOptions()
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}  # 设置浏览器log读取等级
driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.CHROME,
    options=option
        )
# driver.maximize_window()  # 最大化浏览器窗口

if __name__ == '__main__':
    i = 0
    error = 0


    while i != len(ua):
        username = base64.b64decode(ua[i]).decode("utf-8")
        password = base64.b64decode(pd[i]).decode("utf-8")
        try:
            user_login(username, password, login, driver)  # 登陆
            time.sleep(2)
            error = 0
            daka(driver)
        except RuntimeError as e:
            error = 1
            print(e)
        except Exception as e:
            error = 1
            print(e)

        push(i, error)

        if error == 1:
            i -= 1
            tryNum += 1
        else:
            tryNum = 1

        driver.quit()
        print("driver has died")

        time.sleep(2)

        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
            options=option
            )
        i += 1

        if tryNum > 5:
            push(i, 2)
            i += 1
    driver.quit()
