# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 23:05:38 2019

@author: iHJX_Alienware
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

import warnings
warnings.filterwarnings('ignore') 
    # 不发出警告

def get_urls(city,n):
    '''
    【分页网页url采集】函数
    city：城市对应的编码
    n：页数参数
    '''
    lst = []
    ui = 'https://travel.qunar.com/p-%s-jingdian-1-' % city
    for i in range(n):
        lst.append(ui + str(i+1))
    return lst


def get_data(ui,d_h,d_c,table):
    '''
    【数据采集及mongo入库】函数
    ui：数据信息网页
    d_h：user-agent信息
    d_c：cookies信息
    table：mongo集合对象
    '''  
    ri = requests.get(url = ui,headers=d_h,cookies=d_c)
        # 访问网页
    soupi = BeautifulSoup(ri.text, 'lxml')
        # 解析网页
    lis = soupi.find('ul',class_="list_item clrfix").find_all('li')
    n = 0
    for li in lis:
        dic = {}  # 创建空字典，用于存储数据
        dic['景点名称'] = li.find('span',class_="cn_tit").text
        dic['评分'] = li.find('span',class_="total_star").span['style'] 
        dic['排名'] = li.find('span',class_="ranking_sum").text
        dic['攻略提到数量'] = li.find('div',class_="strategy_sum").text
        dic['点评数量'] = li.find('div',class_="comment_sum").text
        dic['多少比例驴友来过'] = li.find('div',class_="txtbox clrfix").find('span',class_="comment_sum").text
        dic['经度'] = li['data-lng']
        dic['纬度'] = li['data-lat']
        table.insert_one(dic)  # 数据入库
        n += 1
    return n
    
    
if __name__ == "__main__":    
    urllst = get_urls('cs299878-shanghai',20)
    print(urllst)   
        # 获取分页网址
    
    h_dic = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        # 获取user-agent
    cookies = '_i=ueHd8Z2SQZf7O4fA4ZVQ9jSpYfyX; fid=75c34561-904f-4bda-baae-a2d89edfca70; QN99=514; QunarGlobal=10.86.213.150_21340582_169c41e489a_-4977|1553773999584; QN601=36afc3d6e9f172c761fa2b81ed34b6b6; QN48=9de25339-3799-4c18-b375-2275ccf4fcba; QN300=auto_4e0d874a; QN621=1490067914133%3DDEFAULT%26fr%3Dtravel_place; QN1=Cl8cFlzue3WY3p8zF1D3Ag; SC1=a232d2893abc0680b203c7d5c5397b2d; SC18=; _RF1=116.230.38.126; _RSG=.0KW4mp6Bk2MuI09beHsXA; _RDG=2844cbaee9f0442a1b380aa63e50e6e031; _RGUID=2b8b1b3c-0481-403e-a876-468949012e16; QN668=51%2C55%2C55%2C59%2C51%2C53%2C53%2C50%2C54%2C57%2C57%2C50%2C59; bathe=4e68cd1f8845dcbdb73a833dfd974427cc04bac279b3528be4db1358b3d8a2ab4b93f45d091746a19ed8dd7d00116224; QN269=F5C6AFD18B7E11E980F7FA163E76697D; QN205=auto_4e0d874a; QN277=auto_4e0d874a; QN243=4; csrfToken=DRaB4LKK5BrZVXvLS8591SBFScNz55FR; _vi=eP--4Rxln8ftKDV1kxKnyKp1A_A2crT5qM47PbTfAlQp0gXIcOHU6rK4JIeF3g1r75lcVcmVdAl1BAPpjRoxxB8uCEBFrj9aymh0oC7ge-6e1e0_82uvbU2_8vMZTDl9eqJUSNMOctrPhPRPoLpLU9Gxm8JiuW0e2rBWfgJhNYgn; QN163=0; QN6=auto_4e0d874a; Hm_lvt_c56a2b5278263aa647778d304009eafc=1561380866,1561466017,1561640137,1561832094; viewpoi=716890|7480238|710603|3159457|7935208|712404|7564992|3167369|3173556|3382917|702215|3231402|7639888|5248773|5127290|713871; viewdist=299878-85|299914-28|300195-2|300100-8|299937-10|299782-10|300079-4; uld=1-299878-102-1561832389|1-299914-35-1561832261|1-299782-18-1561466259|1-300079-4-1561380885|1-299937-10-1557924126|1-300100-10-1557058982|1-1062172-3-1555731251|1-300195-2-1554530701; QN267=917935724c1fdf6d; Hm_lpvt_c56a2b5278263aa647778d304009eafc=1561832388; QN271=349e14f6-43f5-4c00-afcf-3c5282dc9887'
    c_dic = {}
    for i in cookies.split('; '):
        c_dic[i.split('=')[0]] = i.split('=')[1]
        # 获取cookies
        
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['去哪儿网']
    datatabel = db['data01']
        # 设置数据库集合
    
    errorlst = []
    count = 0
    for u in urllst:
        try:
            count += get_data(u,h_dic,c_dic,datatabel)
            print('数据采集成功，总共采集%i条数据' % count)
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：',u)
