import requests
from until.readConfig import readConfig, YamlRead

from log.log import logger
class HttpClient():
    def __init__(self):
        self.session=requests.session() #统一请求会话管理
        self.pre=readConfig.api['testurl']
        self.headers={
            "Content-Type": "application/json",
        }#默认的请求参数类型
        self.session.headers.update(self.headers)
        # 所有的接口权限认证
        self.session.auth = ('admin', 'hhh123456')
    def zhuanhua(self,data): # 用来提取关联环境变量的
        # {
        #     "username": "admin",
        #     "password": "{{password}}"
        # }
        if data:
            for key,value in data.items():
                if isinstance(value,str) and value.startswith("{{") and value.endswith("}}"):
                    # value=value.split("{{")[1].split("}}")[0]
                    value=value[2:-2]
                    '''读取提取变量文件里面的值'''
                    value=YamlRead(readConfig.Tiqu_Path).getData[value]
                    data[key]=value # "password": "123456"
        return data
    def send_request(self,pre,method,name,args=None,tiqu=None):
        # name=self.pre+name # self.pre就是https://127.0.0.1:5000/
        name=pre+name
        '''转化入参和headers里面的参数，包含了{{}}，就去tiqu.yaml去读取'''
        args=self.zhuanhua(args)
        # print(args)
        res=self.session.request(method=method,url=name,params=args,json=args)
        # print(res.request.headers)
        # logger.info(res.json())
        respones = res.json()
        if tiqu and isinstance(tiqu,dict):
            #{"token_tiqu":"token","msg_tiqu":"msg"}
            for key,value in tiqu.items():
                # token_tiqu  token
                # msg_tiqu    msg
                if value  in respones: # ==>token是否在响应数据中
                    # 提取的变量是token，而且是放在headers，单独处理，不需要写入，只需要update headers
                    if value=='token': # 把token
                        h={"token":respones[value]} # 把token对应的值拿出来,添加到请求头
                        # print(h) # {'token': 'hhhtest'}
                        self.session.headers.update(h)
                    else:
                        tidata = YamlRead(readConfig.Tiqu_Path).getData
                        tiqu_data = {value: respones[value]}
                        if tidata == None or value not in tidata:
                            YamlRead(readConfig.Tiqu_Path).write(tiqu_data)
                else:
                    raise ('提取的字段{}在响应值不存在'.format(value))
        return res

    def duanyan(self):
        pass
httpClient = HttpClient()

# if __name__ == '__main__':
#     args = {
#         "username": "admin",
#         "password": "123456"
#     }
#     tiqu = {"token_tiqu": "token", "msg_tiqu": "msg"}
# #
#     httpClient.send_request('post','api/hhh/login',args=args,tiqu=tiqu)
# #     print(res.json())
#     res = httpClient.send_request('post','api/hhh/auth')
#     print(res.json())
