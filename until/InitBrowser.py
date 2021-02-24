import allure
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from until.readConfig import readConfig
from log.log import logger

#读取yaml的代码
browser=readConfig.browser
webUrl=readConfig.webUrl

'''浏览器基础设置方法'''
def supportBrowser():
    '''设置浏览器类型，运行环境，访问的url'''
    if browser['env']=='docker':
        chrome_capabilities = {
            "browserName": "chrome",
        }
        driver = webdriver.Remote("http://47.94.172.18:5555",
                                  desired_capabilities=chrome_capabilities)
    else:
        option=webdriver.ChromeOptions() #添加谷歌的可选项
        if browser['env']=='headless':
            '''谷歌添加无头模式的参数'''
            option.add_argument('headless')

        if browser['name']=='chrome':
            driver=webdriver.Chrome(options=option,
                                    executable_path=readConfig.ChromeDriver_Path)

        elif browser['name']=='firefox':
            driver=webdriver.Firefox()

        elif browser['name'] == 'ie':
            driver = webdriver.Ie()
        else:
            raise ('没有支持的浏览器')
    driver.get(webUrl['testurl'])
    driver.maximize_window()
    # driver.implicitly_wait(3)
    # print(driver.current_url)
    return  driver

'''浏览器公共方法封装'''
class Browser():
    def __init__(self):
        self.driver=supportBrowser()

    def wait_until_element_visible(self,webelement):
        '''元素显试等待时间，默认时间6秒'''
        # ele=WebDriverWait(self.driver,6).until(EC.visibility_of_element_located(webelement))
        # return ele
        try:
            ele=WebDriverWait(self.driver,6).until(EC.visibility_of_element_located(webelement))
            return ele
        except Exception as e:
            self.add_fail_picture()

    def wait_until_element_not_visible(self,webelement):
        # 元素不存在返回true,元素存在报错
        return WebDriverWait(self.driver, 6).until_not(EC.visibility_of_element_located(webelement))

    def send_keys_my(self,webelement,value):
        '''输入方法：每次输入之前自动加等待时间，自动打印日志'''
        self.wait_until_element_visible(webelement).send_keys(value)
        logger.info('在{0}元素输入了{1}'.format(webelement[1],value))

    def click_my(self, webelement):
        '''输入方法：每次输入之前自动加等待时间，自动打印日志'''
        self.wait_until_element_visible(webelement).click()
        logger.info('点击了{0}元素'.format(webelement[1]))

    def quit(self):
        self.driver.quit()

    def add_fail_picture(self):
        '''截图，添加到allure的报告里面去'''
        file_name = readConfig.Picture_Path + r'\test.jpg'
        self.driver.save_screenshot(file_name)  # 截图函数
        '''allure添加截图附件'''
        with open(file_name, mode='rb') as file:
            f = file.read()  # 读取文件，将读取的结果作为参数传给allure
        allure.attach(f, 'error', allure.attachment_type.JPG)
    def assert_ele(self,webelement):
        '''
        断言：一个元素在页面出现的次数
            0，1，
        '''
        try:
            elements = WebDriverWait(self.driver, 10).until(lambda x: x.find_elements(*webelement))
            return len(elements)
        except  Exception as e:
            print(e)
