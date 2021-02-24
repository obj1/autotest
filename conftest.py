'''web自动化下的conftest'''
import time

import pytest
from until.InitBrowser import supportBrowser,Browser
@pytest.fixture()
def openbrowser():
    # driver = supportBrowser()
    # yield driver
    browser = Browser()
    yield browser
    time.sleep(20)
    # driver.quit() fixture指定为session或者module时使用

