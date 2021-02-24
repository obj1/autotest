'''web自动化下的conftest'''
import pytest
from WebTestcase.POM.loginpage import LoginPage
from WebTestcase.POM.homepage import HomePage

@pytest.fixture()
def login(openbrowser):
    '''
    return:已经登录的浏览器对象
    '''
    #登录部分用例才会用到
    #点击登录按钮
    openbrowser.click_my(HomePage.login_button)
    #1.输入用户名
    openbrowser.send_keys_my(LoginPage.username,'hhhh')
    #2.输入密码
    openbrowser.send_keys_my(LoginPage.password,'123456')
    #3.点击登录按钮
    openbrowser.click_my(LoginPage.loginbutton)
    yield openbrowser

