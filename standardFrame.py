# selenium 4
"""
pyinstaller --onefile your_script.py
pyinstaller --onedir your_script.py
"""
import random
import time
import threading
import os
import json
import socket
import queue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions


# 定义一个配置文件，存放浏览器驱动路径等信息
with open('./conf.json', mode='r') as f:
    try:
        content = json.load(f)
        chromedriver_path = content['chromedriver_path']
    except Exception as e:
        print(f'请检查设置的文件路径是否正确：\n{e}')
        assert 1 == 0

lock = threading.Lock()


class Explorer:
    def __init__(self,
                 chromedriver_path: str = r"C:\Users\cerebrumWeaver\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe",
                 port: int = 7093):
        self.chromeService = ChromeService(chromedriver_path)  # 指定驱动路径
        self.chromeOptions = ChromeOptions()  # 初始化配置类
        self.chromeOptions.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 指定打开端口

        # # 以最高权限运行，可以解决DevToolsActivePort文件不存在的报错
        # self.chromeOptions.add_argument("--no-sandbox")
        # # 27. 禁止弹窗拦截器
        # self.chromeOptions.add_argument('--disable-popup-blocking')
        # # 11. 禁止弹出通知
        # self.chromeOptions.add_argument('--disable-notifications')
        # # 6. 使用无头模式（无界面模式）
        # # self.chromeOptions.add_argument('--headless')
        # # 最大化运行
        # self.chromeOptions.add_argument("--start-maximized")
        # # options.add_experimental_option('detach', True)  # 保持浏览器打开状态
        # # 屏蔽--ignore-certificate-errors提示信息
        # self.chromeOptions.add_argument("--ignore-certificate-errors")
        # # 不加载GPU，规避bug
        # self.chromeOptions.add_argument("--disable-gpu")
        # self.chromeOptions.add_argument("--disable-software-rasterizer")
        # # 禁用浏览器正在被自动化程序控制的提示
        # self.chromeOptions.add_argument('--disable-infobars')
        # # 添加需要的 ChromeOptions 选项
        # self.chromeOptions.add_argument('--disable-popup-blocking')
        # self.chromeOptions.add_argument('--disable-notifications')



        self.port = port
        self.driver = None
        pass

    def set_options(self):
        chrome_options = self.chromeOptions

        # 1. 设置浏览器启动时的窗口大小
        chrome_options.add_argument('--window-size=1200x800')

        # 2. 设置浏览器启动时的用户数据目录，用于保留登录状态等信息
        chrome_options.add_argument('--user-data-dir=/path/to/user/data/directory')

        # 3. 禁用图片加载
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')

        # 4. 设置浏览器语言
        chrome_options.add_argument('--lang=en-US')

        # 5. 隐藏自动化插件提示
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 6. 使用无头模式（无界面模式）
        chrome_options.add_argument('--headless')

        # 7. 配置代理
        chrome_options.add_argument('--proxy-server=http://your-proxy-server:port')

        # 8. 禁用 GPU（有时在虚拟机环境下可能需要）
        chrome_options.add_argument('--disable-gpu')

        # 9. 配置启动时的最大化
        chrome_options.add_argument('--start-maximized')

        # 10. 禁用扩展插件
        chrome_options.add_argument('--disable-extensions')

        # 11. 禁止弹出通知
        chrome_options.add_argument('--disable-notifications')

        # 12. 禁用 PDF 视图
        chrome_options.add_argument('--disable-internal-pdf')

        # 13. 禁用密码保存提示
        chrome_options.add_argument('--disable-infobars')

        # 14. 禁用自动填充表单
        chrome_options.add_argument('--disable-autofill')

        # 15. 指定用户代理
        chrome_options.add_argument('--user-agent=your-user-agent-string')

        # 16. 配置代理自动配置文件 URL
        chrome_options.add_argument('--proxy-pac-url=http://your-proxy-pac-url')

        # 17. 配置启动时的禁用扩展插件
        chrome_options.add_argument('--disable-extensions')

        # 18. 配置启动时的禁用 GPU 加速
        chrome_options.add_argument('--disable-gpu')

        # 19. 配置启动时的禁用缓存
        chrome_options.add_argument('--disable-application-cache')

        # 20. 配置启动时的禁用 GPU 缓冲区图象缓存
        chrome_options.add_argument('--disable-gpu-sandbox')

        # 21. 启动 Chrome 浏览器时最大化窗口
        chrome_options.add_argument('--start-maximized')

        # 22. 设置浏览器的缩放级别
        chrome_options.add_argument('--force-device-scale-factor=1')

        # 23. 指定浏览器界面的语言
        chrome_options.add_argument('--lang=zh-CN')

        # 24. 禁用域名自动填充
        chrome_options.add_argument('--disable-domain-reliability')

        # 25. 启动 Chrome 浏览器时不显示信息栏
        chrome_options.add_argument('--disable-infobars')

        # 26. 启动 Chrome 浏览器时忽略 GPU 内存限制
        chrome_options.add_argument('--ignore-gpu-blacklist')

        # 27. 禁止弹窗拦截器
        chrome_options.add_argument('--disable-popup-blocking')

        # 28. 设置代理服务器，格式为 "host:port"
        chrome_options.add_argument('--proxy-server=http://your-proxy-server:port')

        # 29. 设置下载文件的默认目录
        chrome_options.add_argument('--download.default_directory=/path/to/download/directory')

        # 30. 设置 ChromeDriver 日志级别
        chrome_options.add_argument('--log-level=3')  # 0: INFO, 1: WARNING, 2: LOG_ERROR, 3: LOG_FATAL

    # cmd命令启动浏览器
    @staticmethod
    def launch_chrome(port, explorer_type: str = 'google'):
        """
        一、谷歌浏览器url地址栏输入：chrome://version/，复制路径到环境变量
        二、chrome.exe --remote-debugging-port=7093 --user-data-dir="D:\\AutomationProfile7093 类似这样的命令在浏览器中打开，浏览器初始化步骤人工干预操作完
        三、开发工具要右键以管理员运行，否则没有权限执行cmd命令
        """
        if explorer_type == 'google':
            """
            chrome.exe --remote-debugging-port=7095 --user-data-dir="D:\\AutomationProfile7095
            """
            cmd = f'chrome.exe --remote-debugging-port={port} --user-data-dir="D:\AutomationProfile{port}"'
            os.system(cmd)
        pass

    # 获取浏览器driver对象
    def get_driver(self, explorer_type: str = 'google'):
        if explorer_type == 'google':
            lock.acquire()
            # 开启线程，通过cmd命令打开google浏览器
            threading.Thread(target=Explorer.launch_chrome, args=(self.port,), daemon=False,
                             name=f'{self.port}线程Chrome浏览器').start()
            # 判断端口是否开放
            while not Explorer.port_enabled(self.port):
                print(f'休眠一秒，等待浏览器端口{self.port}开放')
                time.sleep(1)
                pass
            try:
                self.driver = webdriver.Chrome(service=self.chromeService, options=self.chromeOptions)
            except Exception as e:
                print(f'浏览器驱动异常，请检查路径，或者更新驱动：\n{e}')
                assert 1 == 0
            lock.release()  # 在浏览器driver对象生产后在释放锁
        else:
            pass
        return self.driver

    # 校验端口是否开放
    @staticmethod
    def port_enabled(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(("localhost", port))
            print(f"Port {port} is open")
            return True
        except:
            print(f"Port {port} is closed")
            return False
        finally:
            sock.close()
            pass

    # 业务代码
    def task_processing(self):
        if self.driver is None:
            print(11111111111)
            driver = self.get_driver()
            # 最大化窗口
            # driver.maximize_window()
        else:
            print(22222222222)
            driver = self.driver
        driver.get('https://www.baidu.com')
        while True:
            question = q.get()
            print(f'当前session：{driver.session_id}')
            driver.find_element(by=By.XPATH, value='//*[@id="kw"]').clear()
            time.sleep(1)
            driver.find_element(by=By.XPATH, value='//*[@id="kw"]').send_keys(question)
            driver.find_element(by=By.XPATH, value='//*[@id="su"]').click()

            q.task_done()  # 表示前面排队的任务已经被完成。被队列的消费者线程使用。每个 get() 被用于获取一个任务， 后续调用 task_done() 告诉队列，该任务的处理已经完成。
            pass


q = queue.Queue(maxsize=10)


# 生产者
def producer():
    while True:
        questions = ['今年IT行业咋这么萧条', 'AI行业最近行情怎么样', '数据建模通用性流程']
        for question in random.choices(questions, k=3):
            q.put(question)


thread_list = []


# 消费者
def consumer():
    for p in range(7093, 7096, 1):
        thread = threading.Thread(target=Explorer(chromedriver_path=chromedriver_path, port=p).task_processing)
        thread_list.append(thread)
        thread.start()


threading.Thread(target=producer).start()
consumer()
q.join()  # 等待所有子线程结束
# for thread in thread_list:
#     thread.join()
print('主线程结束')
