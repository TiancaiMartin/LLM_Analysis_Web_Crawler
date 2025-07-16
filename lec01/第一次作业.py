import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
import random
import csv
import re
#爬取网页信息，获取公告列表
#基础参数设定
pageno = 1
stockid = "000825"

#url = "https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletin.php?stockid=:{}&Page=:{}".format(
#    stockid,pageno)
#上面这个是一开始的另一种写法，发现有点问题，爬取不到公告内容，遂弃用

url = f"https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletin.php?stockid={stockid}&Page={pageno}"

#设定爬取html文本的函数，在后面小实验对比的时候会用到
def get_html_text(url:str)-> str:
    agents = [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
        "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
        "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
        "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
        "Mozilla/2.02E (Win95; U)",
        "Mozilla/3.01Gold (Win95; I)",
        "Mozilla/4.8 [en] (Windows NT 5.1; U)",
        "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
        "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
        "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1"
    ]
    heads = {
        # ip代理池获取时用的url的headers
        'User-Agent': random.choice(agents),
        'ue': 'utf-8'  # 设置翻译支持中文
    }
    # 将如下修改为你的代码
    r=requests.get(url,headers=heads)
    text = requests.get(url,headers=heads).text
    if (r.status_code==200):
        return text
    else:
        print("爬取数据失败，请检查输入stockid以及pageno是否合法!")

data=pd.DataFrame(columns=['title','date','url'])
#定义清除列表重复项的函数，方便后面直接调用
def Distinct(data_list):
    res_list=[]
    for one in data_list:
        if not one in res_list:
            res_list.append(one)
    return res_list

notices_url_list=[]
#创建一个存放url的列表
pageno=1
while len(Distinct(notices_url_list)) < 100:
    #清除重复项
    url = f"https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletin.php?stockid={stockid}&Page={pageno}"
    # 解析列表页（使用BeautifulSoup）
    try:
        text = BeautifulSoup(requests.get(url).text,"html.parser")
        notices = text.find('div', attrs={"class": "datelist"})
    except:
        print("failed url_crawler")
        continue
    # 摘取网页源程序中<div \div>之间的内容，即公司公告，并将爬取的公司公告url转换成列表形式
    for notice in notices.find_all('a'):
        notices_url_list += [notice['href']]
        notices_url_list=Distinct(notices_url_list)
    pageno += 1
notices_url_list=notices_url_list[:100]
#保留前100个公告url（不重复）,理论上来说，
# 由于后面日期标题的爬取都是依赖于url的，因此只要url无重复项，后面的数据也不会有重复项哦
notices_title_list=[]
i=0
while len(notices_title_list)<100:
    for i in range(len(notices_url_list)):
        notice_url = f"https://vip.stock.finance.sina.com.cn{notices_url_list[i]}"
    #notice_url_text=requests.get(notice_url).text
        try:
            notice_page = BeautifulSoup(requests.get(notice_url).text,"html.parser")
            #对每一条公告对进行具体爬取
            notice_title = notice_page.find('th', attrs={"style":"text-align:center"}).text
            notices_title_list += [notice_title]
            # 抓取标题行
            i += 1
        except:
            print("failed title_crawler")
            continue
notices_title_list = list(map(str, notices_title_list))
notices_title_list=[item.replace('\t','').replace('\r','').replace('\n','') for item in notices_title_list]

i=0
#需要重新赋值，从第一个url开始遍历
notices_date_list=[]
while len(notices_date_list)<100:
    for i in range(len(notices_url_list)):
        try:
            notice_url = f"https://vip.stock.finance.sina.com.cn{notices_url_list[i]}"
            time.sleep(0.5)
            notice_page = BeautifulSoup(requests.get(notice_url).text,"html.parser")
            #对每一条公告对进行具体爬取
            notice_date = notice_page.find('td', attrs={'class': 'graybgH2', 'style': 'text-align:center;height:12px;'}).text#抓取日期
            notices_date_list += [notice_date]
            i += 1
        except:
            print("failed")
            continue
notices_date_list=[''.join(re.findall('[0-9-]', item)) for item in notices_date_list]
#仅保留日期，本来的会有'公告日期：'几个字
data['title']=notices_title_list
data['date']=notices_date_list
data['url']=notices_url_list
print(data)
#输出检查看看是否正常

##不同解析方法时间效率比较小实验##
# 这里调用了最开始设计的函数
url=f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/{stockid}.phtml"
html_text=get_html_text(url)
stockid = "000825"
category_dict={}#需要从页面上解析获取数据，以填充该字典！

# 请修改和完成如下函数，完成两种不同的解析方式
def parse_method1(text,category_dict):#使用BeautifulSoup提取文本
    """
    你的方法一
    """
    time.sleep(0.5)
    type_page = BeautifulSoup(text,"html.parser")
    type_select=type_page.find_all('option')
    category_dict=category_dict
    for ftype in type_select:
        category_dict[ftype['value']]=ftype.string#对列表数据进行划分提取
    return category_dict

def parse_method2(text,category_dict):#使用re正则表达式提取
    """
    你的方法二
    """
    time.sleep(0.5)
    text = text.replace('\t','').replace('\r','').replace('\n','').replace(" ","")
    type_select=re.findall(r'<option\s*value=["\']([a-z0-9]+)["\']>(.*?)</option>',text,re.S)
    category_dict=category_dict
    for ftype in type_select:
        category_dict[ftype[0]]=ftype[1]#对爬取元组数据进行划分提取
    return category_dict

#import time，之前已经引入了


def compare():
    """
    比较时间效率。该函数仅供参考。可以自行编写。
    """
    iteration=100

    m1_begin=time.time()
    for i in range(iteration):
        text=html_text
        parse_method1(text,category_dict)
    m1_end=time.time()

    m2_begin=time.time()
    for i in range(iteration):
        text=html_text
        parse_method2(text,category_dict)
    m2_end=time.time()

    print("m1 time cost:",m1_end-m1_begin)
    print("m2 time cost:",m2_end-m2_begin)
compare()
#运行comepare()
#输出结果如下：
'''
m1 time cost: 55.00569796562195
m2 time cost: 50.45888590812683
可知，方法二用时较短，即用re解析效率更高。
'''

#设置爬取公告文本的函数，方便后期调用
def parse_content(url:str) -> str:
    reg = re.compile('<[^>]>')
    #用于之后的仅保留正文
    # 完成下面部分的代码
    notice_url = f"https://vip.stock.finance.sina.com.cn{url}"
    time.sleep(0.5)
    #加一点反应时间比较像真人，不容易被网站ban掉
    notice_page = BeautifulSoup(requests.get(notice_url).text,"html.parser")
    #对每一条公告对进行具体爬取
    notice_content = notice_page.find('div',attrs={'id':'content'}).text
    #抓取正文
    content=reg.sub('',notice_content)
    return content
try:
    data['content']=data['url'].apply(parse_content)#遍历抓取各个公告的正文
except:
    print("failed content_crawler")

##抓取公告类别##
def parse_type(url:str) ->str:#定义爬取每个公告url对应类别的函数
    notices_ftype = '全部'#设置初始值，如果没有匹配类别，则默认归属全部
    i=1#防止ftype=‘0’
    for i in range(len(list(category_dict.keys()))):
        ftype = list(category_dict.keys())[i]
        type_notices_url_list=[]
        type_url=f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/000825.phtml?ftype={ftype}"
        type_notice_page = BeautifulSoup(requests.get(type_url).text,"html.parser")
        notices = type_notice_page.find('div', attrs={"class": "datelist"})
        if notices:#判断该类别下是否存在公告
            for notice in notices.find_all('a'):
                type_notices_url_list += [notice['href']]
                if url in type_notices_url_list:
                    notices_ftype = category_dict[ftype]
                else:
                    i+=1
        else:
            i+=1
    return notices_ftype

try:
    data['type']=data['url'].apply(parse_type)#抓取每个公告的类别
except:
    print("failed type_crawler")

your_name="钟东彤"
your_student_no="2020200883"
data.to_csv(f'/Users/tiancaixiaohuoban/Desktop/高礼/互联网与文本分析/homework1_'f'{your_name}_{your_student_no}_stockid{stockid}_{len(data)}条.csv',encoding='gbk')
