# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 23:05:38 2019

@author: iHJX_Alienware
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

import warnings
warnings.filterwarnings('ignore') 
    # 不发出警告

def get_urls(n):
    '''
    【分页网页url采集】函数
    n：页数参数
    '''
    lst = []
    for i in range(n):
        lst.append('https://movie.douban.com/subject/20438962/photos?type=S&start=%i&sortby=like&size=a&subtype=a'%(i*30))
        # 这里注意，复制网页后，‘%E7%94%B5%E5%BD%B1’需要改成‘%%E7%%94%%B5%%E5%%BD%%B1’
    return lst


def get_pic(ui,d_h,d_c):
    '''
    【数据采集】函数
    ui：数据信息网页
    d_h：user-agent信息
    d_c：cookies信息
    得到图片的dict，包括图片id和图片src
    '''  
    ri = requests.get(url = ui,headers=d_h,cookies=d_c)
        # 访问网页
    soupi = BeautifulSoup(ri.text, 'lxml')
        # 解析网页
    lis = soupi.find('ul',class_="poster-col3 clearfix").find_all('li')
    piclst = []
    for li in lis:
        dic = {}
        dic['picname'] = li['data-id']
        dic['picsrc'] = li.find('img')['src']
        piclst.append(dic)
    return piclst


def save_pic(picdic):
    '''
    【数据采集】函数
    picdic：图片存储的字典，包括图片id和图片src
    '''  
    img = requests.get(url = picdic['picsrc'])
        # 访问网页
    with open('p' + picdic['picname'] + '.jpg', 'ab') as f:
        f.write(img.content)
        f.close()    
        # 写入文件

    
if __name__ == "__main__":  
    import os
    os.chdir('C:/Users/iHJX_Alienware/Desktop/pics/')
        #设 置图片存储路径
        
    urllst = get_urls(10)
    print(urllst)   
        # 获取分页网址
    
    h_dic = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        # 获取user-agent
    cookies = 'bid=-Vb0mooHgwU; ll="108296"; _vwo_uuid_v2=D97DB4EC3A6DE4D04879B636254944105|03c959f87008dd845074a7dc37ce072f; douban-fav-remind=1; gr_user_id=3ecc0d09-a431-4b8c-9b2f-3a11c9c8534f; __yadk_uid=Pb1dulESnqmihil5iES7HQu618r13jBg; __gads=ID=c086f25de6162974:T=1547364458:S=ALNI_MaBRbdZtgiTQGzZGFTCRn3e11onbQ; _ga=GA1.2.1605809557.1531756417; __utmv=30149280.14670; viewed="25815707_33416858_1152126_1035848_27667378_33419041_30482656_5257905_2064814_25862578"; push_noty_num=0; push_doumail_num=0; __utma=30149280.1605809557.1531756417.1561789945.1561820352.110; __utmc=30149280; __utmz=30149280.1561820352.110.81.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1561820367%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=81379588.2028513491.1535457105.1561789945.1561820367.43; __utmc=81379588; __utmz=81379588.1561820367.43.21.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=fb752381-b64e-43f8-9fe8-bfee8f24bf99; gr_cs1_fb752381-b64e-43f8-9fe8-bfee8f24bf99=user_id%3A0; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_fb752381-b64e-43f8-9fe8-bfee8f24bf99=true; Hm_lvt_6e5dcf7c287704f738c7febc2283cf0c=1561820374; Hm_lpvt_6e5dcf7c287704f738c7febc2283cf0c=1561820374; _pk_id.100001.3ac3=dabd77c1e491d680.1535457105.43.1561821031.1561790041.; __utmt_douban=1; __utmb=30149280.8.10.1561820352; __utmt=1; __utmb=81379588.7.10.1561820367'
    c_dic = {}
    for i in cookies.split('; '):
        c_dic[i.split('=')[0]] = i.split('=')[1]
        # 获取cookies

    srclst = []
    for u in urllst:
        try:
            imgs = get_pic(u,h_dic,c_dic)
            srclst.extend(imgs)  
            print('图片src获取成功，总共获取%i条' % len(srclst))
        except:
            continue
        # 获取图片src
        
    n = 1
    for src in srclst: 
        try:   
            save_pic(src)
            print('图片采集成功，已采集%i张图片' % n)
            n += 1
        except:
            continue
        # 批量图片采集

    