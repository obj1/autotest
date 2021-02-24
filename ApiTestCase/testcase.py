import requests,unittest
import yaml
from ddt import ddt,file_data,data
from until.excelRW import Excel
from until.readConfig import readConfig
from until.httpRequest import httpClient
from httptestrunnet.HTMLTestRunner import HTMLTestRunner
from until.tools import *

# excel = Excel(readConfig.Api_CaseInfo_Path_excel)
# casesInfo = excel.read()
casesInfo = apitestcase_runs()
@ddt
class Testcase(unittest.TestCase):
    def setup(self):
        pass
    @data(*casesInfo)
    def testcase1(self,casesInfo):
        '''发请求过程和断言的方法和代码封装到请求的类'''
        name, method, args, tiqu,pre = casesInfo['接口路径'],\
                             casesInfo['请求方法'],\
                             str_loads(casesInfo['入参']), \
                             str_loads(casesInfo['提取变量']), \
                                       casesInfo['接口的前缀']
        res = httpClient.send_request(pre=pre,name=name, method=method,args=args,tiqu=tiqu)
        duanyan = str_loads(casesInfo['断言'])
        '''断言：预期结果(duanyan)与实际结果(响应值)相等或者是否包含'''
        result = validate(duanyan, res.json())
        logger.info(res.json())
        logger.info(result[1])
        self.assertTrue(result[0])
from log.log import logger
if __name__ == '__main__':
    # unittest.main()
    suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover('.', pattern='test*.py')
    with open('../httptestrunnet/result.html','wb') as fp:
        runner = HTMLTestRunner(stream=fp,title='自动化测试报告',description='全量接口自动化用例',tester='一座森林')
        runner.run(discover)
