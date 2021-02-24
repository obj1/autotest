'''
excel读取的封装:
excel表格每一行代表一个用例的数据，组装成一个字典
将表格的每一行数据组装到一个列表
将多个表格的数据组装到一个列表
'''

import xlrd,openpyxl
class Excel():
    def __init__(self,filepath):
        self.filepath=filepath
        self.excel=xlrd.open_workbook(self.filepath)

    def read(self):
        datas = [] #所有的表格的数据
        sheets=len(self.excel.sheet_names()) #获取有多少个表格，返回是一个列表
        for s in range(sheets):
            sheet=self.excel.sheet_by_index(s) #第一个表格
            rows,cols=sheet.nrows,sheet.ncols #获取多少行多少列
            header =sheet.row_values(0)  #获取第一行的数据
            for i in range(1,rows): #循环一次组装一个字典,有多少条数据
                info={}
                for j in range(0,cols): #字典有多少组"key":value
                    #key，value用excel的变量去代替
                        info[header[j]]=sheet.row_values(i)[j]
                datas.append(info)
        return  datas

    def write(self):
        pass

# if __name__ == '__main__':
#     from until.readConfig import readConfig
#     excel = Excel(readConfig.Api_CaseInfo_Path_excel)
#     print(excel.read())
