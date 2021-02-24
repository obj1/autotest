import os

from selenium.webdriver.common.by import  By
from until.InitBrowser import Browser
class HomePage():
    # 搜索框
    search_input=(By.XPATH,'//*[@id="search-input"]')
    # 搜索按钮
    search_button=(By.XPATH,'//*[@id="ai-topsearch"]')
    # 进入登录页面的按钮
    login_button=(By.XPATH,"/html/body/div[2]/div/ul[1]/div/div/a[1]")
    # 商品数量
    gods=(By.XPATH,"/html/body/div[4]/div/ul/li")

    def search_and_click(self,openbrowser,value):
        '''首页输入框操作方法
        想在PO里面封装元素的操作方法'''
        openbrowser.send_keys_my(self.search_input,value)
        openbrowser.click_my(self.search_button)

