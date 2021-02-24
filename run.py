#用例的执行入口
import pytest
from until.send_email import send
#运行所有的用例

pytest.main()

#xx项目的用例
#pytest.main(['./shop2'])

#xx项目的接口自动化用例

import os
os.system('allure generate --clean ./report/xml/ -o ./results/html/')
# os.system('taskkill /im chromedriver.exe /f')
send()
