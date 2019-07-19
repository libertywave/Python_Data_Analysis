# -*- coding: utf-8 -*-
"""
@author: iHJX_Alienware
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import re

import warnings
warnings.filterwarnings('ignore') 
    # 不发出警告

def get_urls(u,d_h,d_c):
    '''
    【视频页面url采集】函数
    u：起始网址
    d_h：user-agent信息
    d_c：cookies信息
    结果：得到一个视频页面的list
    '''
    lst = []
    ri = requests.get(url = u,headers = d_h, cookies = d_c)
    soupi = BeautifulSoup(ri.text, 'lxml')
    lis = soupi.find('ul',class_="video-contain clearfix").find_all('li')
    lst = []
    for i in lis:
        lst.append('https:' + i.a['href'])
    return lst


def get_data(ui,d_h,d_c,table):
    '''
    【视频页面数据采集 / cid信息 / 弹幕xml数据采集】函数
    ui：数据信息网页
    d_h：user-agent信息
    d_c：cookies信息
    table：mongo集合对象
    '''  
    r1 = requests.get(url = ui,headers=d_h,cookies=d_c)  
    soup1 = BeautifulSoup(r1.text, 'lxml')
        # 访问视频网页，并解析
    name = soup1.h1['title']
    date = re.search(r'(20.*\d)',soup1.find('div',class_ = 'video-data').text).group(1)
    cid = re.search(r'"cid":(\d*),',r1.text).group(1)
    u2 = 'https://comment.bilibili.com/%s.xml' % cid
        # 采集视频基本信息及cid
    r2= requests.get(url = u2)
    r2.encoding = r2.apparent_encoding
    dmlst = re.findall('<d p=.*?</d>',r2.text)
        # 获取弹幕列表
    n = 0
    for dm in dmlst:
        dic = {}
        dic['标题'] = name
        dic['发布时间'] = date
        dic['cid'] = cid
        dic['弹幕'] = re.search(r'>(.*)</d',dm).group(1)
        dic['其他信息'] = re.search(r'<d p="(.*)"',dm).group(1)
        table.insert_one(dic)  # 数据入库
        n += 1
        #print(dic)
    return n
   
    
if __name__ == "__main__":    
    h_dic = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        # 获取user-agent
    cookies = 'buvid3=305CC2CB-1703-4626-A640-BD3E7E70B8A0140269infoc; rpdid=kmilopiiqpdosiqompkiw; stardustvideo=1; fts=1536299103; CURRENT_FNVAL=16; _uuid=F512FD0B-B7CA-D2BD-BA0B-8F6CF509090895539infoc; CURRENT_QUALITY=32; UM_distinctid=1688637b7f253c-03826e932bec74-b781636-1fa400-1688637b7f371d; sid=7p19dnm9; LIVE_BUVID=317bf8e1d57f578eb645a258216460f4; LIVE_BUVID__ckMd5=577b641e83c4ef57; _jct=0f856580a02711e9bcb642b0599aacba; DedeUserID=440933759; DedeUserID__ckMd5=79a56d1b79ed415e; SESSDATA=fe06eee0%2C1565034591%2C0ed92271; bili_jct=d09a0721996e707fbe800c9250cd65b9'
    c_dic = {}
    for i in cookies.split('; '):
        c_dic[i.split('=')[0]] = i.split('=')[1]
        # 获取cookies
    
    u1 = 'https://search.bilibili.com/all?keyword=%E8%94%A1%E5%BE%90%E5%9D%A4'
    urllst = get_urls(u1,h_dic,c_dic)
    print(urllst)
        # 采集视频页面网址
        
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['blibli']
    datatable = db['弹幕信息'] 
        # 设置数据库集合 
        
    errorlst = []
    count = 0
    for u in urllst:
        try:
            count += get_data(u,h_dic,c_dic,datatable)
            print('数据采集成功，总共采集%i条数据' % count)
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：',u)