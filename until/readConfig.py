'''1.读取配置文件
   2.项目下所有文件的相对路径
'''
import yaml,os

# 1.读取配置文件
class YamlRead:
    def __init__(self,yamlPath):
        '''如果是第一次调用，读取yaml文件，否则直接返回之前保存的数据'''
        if os.path.exists(yamlPath):
            self.yamlPath=yamlPath
        else:
            raise  FileNotFoundError('yaml文件不存在')
        self._data=None #保存yaml的数据

    @property  #把一个方法变成属性来调用,
    def getData(self):
        if not self._data:
            with open(self.yamlPath,mode='rb') as f:
                self._data=yaml.safe_load(f)
        return self._data

    def write(self,data):
        '''写入yaml，存放提取的数据'''
        with open(self.yamlPath,mode='a',encoding='utf-8') as file:
            yaml.dump(data,file,allow_unicode=True)
# 2.项目下所有文件的相对路径
class Config:
     # 项目下所有文件的相对路径
     Base_Path=os.path.abspath(__file__+'\..'+'\..')
     Base_Data=Base_Path+'\config\data.yaml'
     Base_LOG= Base_Path+'\log'
     ChromeDriver_Path=Base_Path+'\lib\chromedriver.exe'
     FirefoxDriver_Path=Base_Path+'\lib\geckodriver.exe'
     Picture_Path = Base_Path + '\picture'
     Api_CaseInfo_Path_Yaml = Base_Path + '\config\\apitestcases.yaml'
     Api_CaseInfo_Path_excel = Base_Path + r'\config\apitestcase.xlsx'
     Tiqu_Path = Base_Path + r'\config\tiqu.yaml'
     # 获取基础数据daya.yaml的数据
     def __init__(self):
         '''获取daya.yaml所有的数据'''
         self.config=YamlRead(Config.Base_Data).getData
     @property
     def webUrl(self):
         return  self.config['webUrl']
     @property
     def browser(self):
         return  self.config['Browser']
     @property
     def api(self):
         return self.config['Api']

     @property
     def database(self):
         return self.config['database']

     @property
     def runApi(self):
         return self.config['RunApi']

     @property
     def runApis(self):
         return self.config['RunApis']
readConfig=Config()

# print(readConfig.config)

