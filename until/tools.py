# print('封装一些常用公共方法,比如:随机数，获取当前时间，身份证，银行卡,手机号')
''''''
from log.log import logger


def str_loads(data):
    '''excel表填写的字典读取的时候是字符串类型，可能包含了空格
      本是字典类型的，没有填写数据的，返回为None
    '''
    if data and isinstance(data,str):
        datas=eval(data)
        return datas
    else:
        return None

'''断言'''
def validate(yuqi, shiji,msg='断言结果:'):
    for key,value in  yuqi.items():
        '''直到预期结果不等于实际结果的时候，或者预期结果不在实际结果里面
        才返回布尔值
        '''
        if key not in shiji:
            msg+='{}的字段根本就不在实际结果里面'.format(key)
            return False,msg
        else:
    #             #预期的字典为字典
                if isinstance(value,dict) and isinstance(shiji[key],dict):
                    res=validate(value,shiji[key]) #返回布尔值和msg
                    if res[0] is False:
                        return res
                elif value!=shiji[key]:
                    msg+='{}的值预期是{},而实际是{}'.format(key,value,shiji[key])
                    return False,msg
    msg += '实际结果与预期结果相等'
    return True,msg

from until.readConfig import readConfig
from until.excelRW import Excel

def apitestcase_runs():
    '''接口用例：支持单个运行，支持多个按 顺序运行'''
    excel = Excel(readConfig.Api_CaseInfo_Path_excel)
    casesInfo = excel.read() #列表
    runApi,runApis=readConfig.runApi,readConfig.runApis
    if runApi:
        # casesInfo结合ddt使用,就算只取1个也要通过列表的形式
        casesInfo=casesInfo[runApi-1:runApi] # 第一种
        # casesInfo = [casesInfo[runApi-1]] #第二种
    elif runApis:
        cases=[]
        for i in runApis:
            cases.append(casesInfo[i-1])
        casesInfo=cases

    return casesInfo

