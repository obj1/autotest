'''模块2的用例：不需要登录'''
from WebTestcase.POM.homepage import HomePage
from log.log import logger
class Testcase2(HomePage):
    def testcase(self,openbrowser):
        self.search_and_click(openbrowser,'手机')
        times = openbrowser.assert_ele(self.gods)
        logger.info('{}在页面上出现了{}次'.format(self.gods,times))
        assert times==6
    def testcase2(self,openbrowser):
        assert 6==6
