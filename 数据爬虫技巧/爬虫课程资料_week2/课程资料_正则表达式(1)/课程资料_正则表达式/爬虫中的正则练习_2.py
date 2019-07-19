# -*- coding: utf-8 -*-
"""
@author: iHJX_Alienware
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urllst = ['https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=0&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=20&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=40&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=60&type=T',
 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=80&type=T']    
     # 添加网址

def get_data(ui):
    ri = requests.get(url=ui)
    soupi = BeautifulSoup(ri.text, 'lxml')
    lis = soupi.find('ul',class_="subject-list").find_all('li')
    lst = []
    for li in lis:
        dic = {}
        dic['书名'] = re.sub(r'\s+','',li.h2.text)
            # 添加简单字段
        infors = re.sub(r'\s+','',li.find('div',class_="pub").text)
        dj = re.search(r'.*/([.\d]*)\D*',infors) 
        if dj:
            dic['定价'] = dj.group(1)
            # 匹配定价信息，如果匹配成功则添加进字典
        nf = re.search(r'.*/([-\d]*)/',infors) 
        if nf:
            dic['年份'] = nf.group(1)
            # 匹配定价信息，如果匹配成功则添加进字典
        lst.append(dic)
    return lst
    
get_data(urllst[0])
    # 测试
    
datalst = []
for u in urllst:
    try:
        datalst.extend(get_data(u))
        print('数据采集成功，总共采集%i条数据' % len(datalst))
    except:
        errorlst.append(u)
        print('数据采集失败，数据网址为：',u)
        
print(datalst) 
df = pd.DataFrame(datalst)       
    # 采集数据，生成dataframe