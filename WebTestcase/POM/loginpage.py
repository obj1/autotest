from selenium.webdriver.common.by import  By
class LoginPage:
    username=(By.NAME,'accounts')
    password=(By.NAME,'pwd')
    loginbutton=(By.XPATH,"//*[@type='submit' and text()='登录']")
