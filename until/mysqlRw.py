import pymysql

from until.readConfig import readConfig
database = readConfig.database

class Sql_handler():
    def __init__(self,host,user,pwd,db,port,charset='utf8',autocommit=True):
        self.host=host
        self.user=user
        self.pwd=pwd
        self.db=db
        self.port=port
        self.charset=charset
        self.autocommit=autocommit
    def excute_sql(self,sql,size=None,display=True):
        self.conn=pymysql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,
                                  port=self.port,charset=self.charset,autocommit=self.autocommit)
        self.cur=self.conn.cursor() # 创建游标
        try: # 上面代码.无需放进try. 上方代码如果失败的话,try不try已经毫无意义,try是为了防止连接成功后,执行语句时出错无法关闭连接的.
            # SQL支持大小写所以统一转小写,并判断语句第一个空格前与以下是否恒等
            # 比如:INSERT into ... 大写也是正确的
            # 比如:INSERTH into ... 语句关键字都写错了就不要它进入了吧,所以不但要转小写还要截取判断
            sql_spli_li=sql.lower().split() # 把语句转为小写,以空格隔开放进列表 如:['insert', 'into', 'dept', 'value(0,"it","china");']
            if sql_spli_li[0]=='insert' and sql_spli_li[1]=='into': # 插入就是insert into...嘛
                print('执行插入语句:',sql)
                self.cur.execute(sql) # 执行sql
                print('数据已插入')
            # 由于sql语句中"表"可以取别名,其实更新根本不需要取别名,但是防止傻瓜式操作就不通过下标拿set了.
            elif sql_spli_li[0]=='update' and ('set' in sql_spli_li):
                print('执行更新语句:',sql)
                self.cur.execute(sql) # 执行sql
                print('数据已更新')
            elif sql_spli_li[0]=='delete' and ('from' in sql_spli_li): # w3c是这两种: delete from ... / delete * from table_name
                print('执行删除语句: ',sql)
                self.cur.execute(sql) # 执行sql
                print('对应数据已删除') # 我看到数据已删除心情不好,就加个对应吧
            elif sql_spli_li[0]=='select' and ('from' in sql_spli_li):# 同理 select ... from...
                self.cur.execute(sql) # 执行sql
                self.count = self.cur.rowcount # 查询结果总量
                if display: # display就是判断一下外部是不是只想要返回值,如果只是要返回值的话这些没用的打印就别执行了
                    print('查询数据: {} \n数据总量: {}'.format(sql, self.count))
                if size:
                    self.res = self.cur.fetchmany(size) # 获取指定条数查询结果
                else:
                    self.res = self.cur.fetchall() # 获取所有查询结果
                if self.count and display: #如果表中没有数据或者只是想要返回值,就不要去遍历展示字段、游标和每一项了
                    print('查询结果如下:\n字段:',end='')
                    for field in self.cur.description: # 拿字段
                        print('\t', field[0], end='\t')
                    print()
                    for i in range(len(self.res)): # 拿游标及数据
                        print('游标',i,'\t',self.res[i])
                return self.count,self.res #外部想要使用就接收不想使用就拉倒
            else: # 不是sql对应关键字直接抛出异常
                raise Exception('传入的sql不是增、删、改、查语句,请检查关键字是否正确')
        finally: # 不是sql语句? sql语句执行完毕? sql语句报错? 已经return? 不论什么情况下,只要连接了,就要关闭,关闭就要finally.
            self.cur.close()# 关闭游标
            self.conn.close() # 关闭连接
    def __str__(self): # 打印实例,展示描述,可以查看如何使用
        return '''
        先实例 m=Sql_handler('主机','用户','密码','库名',端口号[,字符集,是否自动提交])
        如下调用的两种情况
            m.excute_sql(mysql语句[,查询展示结果数量])
            m.excute_sql(查询语句[,查询展示结果数量,是否内部进行结果展示])'''

# m = Sql_handler(*database.values()) # 不能直接这样用哦,因为yaml文件数据顺序和封装顺序不一致需要稍作修改
# def excute_sql(sql,size=None,display=True):
#     m.excute_sql(sql,size,display)
# if __name__ == '__main__':
    # database = readConfig.database
    # {'username': 'root', 'password': 'root', 'dbname': 'test', 'serve': 'localhost', 'port': 3307}
    # print(*database.values())
    # m = Sql_handler('localhost', 'root', 'root', 'test', 3306)
    # print('使用说明:',m)
    # 错误的  # 抛出异常 Exception: 传入的sql不是增、删、改、查语句,请检查关键字是否正确
    # m.excute_sql('INSERT456 into emp values(0,"IT","China")')

    # 增加   # 大小写都试一下
    # m.excute_sql('INSERT into dept value(0,"IT","China");')
    # m.excute_sql('insert into dept values(1,"IT2","China");')

    # 删除
    # m.excute_sql('delete from dept where dname="IT";')

    # 更新        试一下中文是否好用吧(报错的话记得修改字符集)
    # m.excute_sql('Update dept hh set dname="挨踢" where dname="IT2";')

    # 查询   直接调用就行内部已经print了
    # m.excute_sql('select * from dept')
    # m.excute_sql('select * from dept',2) #传size

    # 只要返回值
    # 如果外部想要使用数据总量或数据结果,也可以拿返回值,内部也返回了,
    # 只需要传参时display参数指定为false,内部就不会打印,只会返数据,
    # count,res=m.excute_sql('select * from dept',display=False)
    # print('总量:{}\n数据:{}'.format(count,res))
