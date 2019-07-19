# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:40:39 2019

@author: Vodka
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

#(1).读取数据
import os
os.chdir(r'C:\Users\Vodka\Desktop\项目练习07：中国城市资本流动问题探索')

df = pd.read_excel('data.xlsx')
df = df.groupby(['投资方所在城市','融资方所在城市','年份']).sum().reset_index()
# 同城投资数量
data_tc = df[df['投资方所在城市'] == df['融资方所在城市']]
data_tc = data_tc.sort_values('投资企业对数',ascending = False).reset_index()
del data_tc['index']
#跨城投资数量
data_kc = df[df['投资方所在城市'] != df['融资方所在城市']]
data_kc = data_kc.sort_values('投资企业对数',ascending = False).reset_index()
del data_kc['index']

#(2)比较同城投资和跨城投资Top20分布情况
#汇总同城投资总数
tc_sum = data_tc.groupby(['投资方所在城市','融资方所在城市']).sum().sort_values('投资企业对数',ascending = False)
del tc_sum['年份']
#汇总跨城投资总数
kc_sum = data_kc.groupby(['投资方所在城市','融资方所在城市']).sum().sort_values('投资企业对数',ascending = False)
del kc_sum['年份']

tc_sum.iloc[:20].plot(kind='bar',color = 'green',alpha = 0.7,figsize = (12,6))
kc_sum.iloc[:20].plot(kind='bar',color = 'blue',alpha = 0.7,figsize = (12,6))

#(3)分年份比较2013-2016年同城、跨城投资数据
#创建函数
def f1(year):
    tc_year = data_tc[data_tc['年份'] == year].sort_values('投资企业对数',ascending = False)
    kc_year = data_kc[data_kc['年份'] == year].sort_values('投资企业对数',ascending = False)
    tc_year.index = tc_year['投资方所在城市']
    kc_year.index = kc_year['投资方所在城市'] + '-' + kc_year['融资方所在城市']
    return(tc_year.iloc[:20],kc_year.iloc[:20])

#绘制每一年柱状图    
fig,axes = plt.subplots(4,2,figsize = (12,15))
plt.subplots_adjust(wspace = 0.1,hspace = 0.5)

f1(2013)[0]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,40000],
                                color = 'blue',ax = axes[0,0],title = '同城投资--2013年')
f1(2013)[1]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,3000],
                                color = 'green',ax = axes[0,1],title = '跨城投资--2013年')
f1(2014)[0]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,40000],
                                color = 'blue',ax = axes[1,0],title = '同城投资--2014年')
f1(2014)[1]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,3000],
                                color = 'green',ax = axes[1,1],title = '跨城投资--2014年')
f1(2015)[0]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,40000],
                                color = 'blue',ax = axes[2,0],title = '同城投资--2015年')
f1(2015)[1]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,3000],
                                color = 'green',ax = axes[2,1],title = '跨城投资--2015年')
f1(2016)[0]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,40000],
                                color = 'blue',ax = axes[3,0],title = '同城投资--2016年')
f1(2016)[1]['投资企业对数'].plot(kind = 'bar',grid = True,alpha = 0.7,ylim = [0,3000],
                                color = 'green',ax = axes[3,1],title = '跨城投资--2016年')

#（4）导入城市经纬度信息
city = pd.read_excel('中国城市代码对照表.xlsx')
kc_sum.reset_index(inplace = True)
kc_data = pd.merge(kc_sum,city[['城市名称','经度','纬度']],left_on = '投资方所在城市',right_on = '城市名称')
kc_data = pd.merge(kc_data,city[['城市名称','经度','纬度']],left_on = '融资方所在城市',right_on = '城市名称')
kc_data = kc_data[['投资方所在城市','融资方所在城市','投资企业对数','经度_x','纬度_x','经度_y','纬度_y']]
kc_data.columns = ['投资方所在城市','融资方所在城市','投资企业对数','lng_tz','lat_tz','lng_rz','lat_rz']

#(5)导出Gephi文件分析
#导出边数据
gephi_edges = kc_data[['投资方所在城市','融资方所在城市','投资企业对数']]
gephi_edges.columns = ['source','target','weight']
gephi_edges['weight'] = (gephi_edges['weight'] - gephi_edges['weight'].min()) / (gephi_edges['weight'].max() - gephi_edges['weight'].min())
gephi_edges.to_csv('gephi_edges.csv',index = False,encoding = 'gbk')
#导出点数据，label字段只要前20
cities = list(set(gephi_edges['source'].tolist() + gephi_edges['target'].tolist()))
gephi_nodes = pd.DataFrame({'Id':cities})
top_20 = gephi_edges.sort_values('weight',ascending = False)['source'].drop_duplicates().iloc[:20]
top_20_df = pd.DataFrame({'Id':top_20,'Label':top_20})
gephi_nodes = pd.merge(gephi_nodes,top_20_df,on = 'Id',how = 'left')
gephi_nodes.to_csv('gephi_nodes.csv',index = False,encoding = 'gbk')

#（6）导出Qgis数据,用于生成轨迹图
kc_data.to_csv('跨城投资Qgis数据.csv',index = False,encoding = 'gbk')

#（7）挖掘资本流向情况

result1 = kc_sum[['投资方所在城市','投资企业对数']].groupby('投资方所在城市').sum().sort_values('投资企业对数',ascending = False)
result2 = kc_sum[['融资方所在城市','投资企业对数']].groupby('融资方所在城市').sum().sort_values('投资企业对数',ascending = False)

result1.iloc[:10].plot(kind = 'bar',grid = True,color = 'red',alpha = 0.7,figsize = (12,6))
result2.iloc[:10].plot(kind = 'bar',grid = True,color = 'blue',alpha = 0.7,figsize = (12,6))

#2013-2016年，两大阵营资本流动

def f2(year):
    kc_datai = data_kc[data_kc['年份'] == year]
    x  = kc_datai[['融资方所在城市','投资企业对数']].groupby('融资方所在城市').max().reset_index()
    city_tz_max = pd.merge(kc_datai,x,on =['融资方所在城市','投资企业对数'],how = 'right')
    #得到融资城市最大投资对数的投资方城市
    city_tz_max['阵营'] = 0
    city_tz_max['阵营'][(city_tz_max['投资方所在城市'] == '北京') | 
                        (city_tz_max['投资方所在城市'] == '上海') |
                        (city_tz_max['投资方所在城市'] == '深圳')] = 1
    # 划分两大阵营
    city_tz_max = pd.merge(city_tz_max,city[['城市名称','经度','纬度']],left_on = '融资方所在城市',right_on = '城市名称',how = 'left')
    city_tz_max = city_tz_max[['投资方所在城市','融资方所在城市','阵营','投资企业对数','经度','纬度']]
    #添加经纬度
    dici = {}
    dici['北上深阵营城市数据量'] = city_tz_max['阵营'].value_counts()[1]
    dici['本地化阵营城市数据量'] = city_tz_max['阵营'].value_counts()[0]
    #print(city_tz_max['阵营'].value_counts())
    return city_tz_max,dici

#北上深阵营城市投资变化趋势

zy_year = pd.DataFrame([f2(2013)[1],f2(2014)[1],f2(2015)[1],f2(2015)[1]],
                        index = ['2013年','2014年','2015年','2016年'])


zy_year['北上深阵营占比'] = zy_year['北上深阵营城市数据量'] / (zy_year['北上深阵营城市数据量'] + zy_year['本地化阵营城市数据量'])

zy_year[['本地化阵营城市数据量','北上深阵营城市数据量']].plot(kind = 'bar',stacked = True,
                                                           color = ['red','blue'],grid = True,
                                                           rot = 0,alpha = 0.7,figsize = (12,6))
#导出Qgis数据

f2(2013)[0].to_csv('year2013.csv',index = False,encoding = 'gbk')
f2(2014)[0].to_csv('year2014.csv',index = False,encoding = 'gbk')
f2(2015)[0].to_csv('year2015.csv',index = False,encoding = 'gbk')
f2(2016)[0].to_csv('year2016.csv',index = False,encoding = 'gbk')










