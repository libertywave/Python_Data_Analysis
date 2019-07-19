# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 15:10:18 2019

@author: Vodka
"""

import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


#(1)读取数据
import os

os.chdir(r'C:\Users\Vodka\Desktop\项目练习06_房价影响因素挖掘')
df01 = pd.read_csv('house_rent.csv',engine = 'python')
df02 = pd.read_csv('house_sell.csv',engine = 'python')
df01.dropna(inplace=True)
df02.dropna(inplace=True)

#(2)计算指标并按照租金，售价汇总（每平米）

df01['rent_area'] = df01['price'] / df01['area']
data_rent = df01[['community','lng','lat','rent_area']].groupby('community').mean()
data_sell = df02[['property_name','lng','lat','average_price']].groupby('property_name').mean()
data_rent.reset_index(inplace = True)
data_sell.reset_index(inplace = True)
data = pd.merge(data_rent,data_sell,left_on = 'community',right_on = 'property_name')
data = data[['community','lng_x','lat_x','rent_area','average_price']]
data.rename(columns = {'lng_x':'lng','lat_x':'lat','average_price':'sell_area'},inplace = True)
    
#(3)计算房屋售租比

data['sell_rent'] = data['sell_area'] / data['rent_area']
print('上海房屋售租比中位数为%i个月'%data['sell_rent'].quantile(0.5))

# 绘制直方图
data['sell_rent'].plot.hist(bins = 100,color = 'red',figsize = (12,6))

# 绘制箱型图
data['sell_rent'].plot.box(vert = False,grid = True,figsize = (12,6))

#（4）导出数据

data.to_csv('上海市房价情况.csv',encoding = 'gbk')
#QGIS操作

#（5）加载导出的点数据

data_point = pd.read_excel('result_point.xlsx',sheetname = 0)
data_point.fillna(0,inplace = True)

# 指标标准化处理

def f1(data,col):
    return (data[col] - data[col].min()) / (data[col].max() - data[col].min())

data_point['人口密度指标'] = f1(data_point,'Z')
data_point['路网密度指标'] = f1(data_point,'长度')
data_point['餐饮价格指标'] = f1(data_point,'cy_count')
data_point['离市中心距离'] = ((data_point['lng'] - 353508.848122)**2 + (data_point['lat'] - 3456140.926976 )**2)**0.5

data_point_test = data_point[['人口密度指标','路网密度指标','餐饮价格指标','离市中心距离','sell_area_']]
data_point_test = data_point_test[data_point_test['sell_area_'] > 0].reset_index()
del data_point_test['index']

plt.figure(figsize = (15,6))
plt.scatter(data_point_test['人口密度指标'],data_point_test['sell_area_'],s = 2,)

plt.figure(figsize = (15,6))
plt.scatter(data_point_test['路网密度指标'],data_point_test['sell_area_'],s = 2,)

plt.figure(figsize = (15,6))
plt.scatter(data_point_test['餐饮价格指标'],data_point_test['sell_area_'],s = 2,)

plt.figure(figsize = (15,6))
plt.scatter(data_point_test['离市中心距离'],data_point_test['sell_area_'],s = 2,color = 'red')

data_point_test.corr().loc['sell_area_']


#(6) 按照距离市中心每10公里计算各指标相关性

dis = []
rkmd_pearson = []
lwmd_pearson = []
cyjg_pearson = []
zxjl_pearson = []

for distance in range(10000,70000,10000):
    data_n = data_point_test[data_point_test['离市中心距离'] <= distance]
    pearson = data_n.corr()['sell_area_']
    dis.append(distance)
    rkmd_pearson.append(pearson['人口密度指标'])
    lwmd_pearson.append(pearson['路网密度指标'])
    cyjg_pearson.append(pearson['餐饮价格指标'])
    zxjl_pearson.append(pearson['离市中心距离'])
    print('离市中心距离小于%i时，数据量有%i条'%(distance,len(data_n)))
    print('人口密度指标相关系数为%.3f'%pearson['人口密度指标'])
    print('路网密度指标相关系数为%.3f'%pearson['路网密度指标'])
    print('餐饮价格指标相关系数为%.3f'%pearson['餐饮价格指标'])
    print('离市中心距离相关系数为%.3f\n'%pearson['离市中心距离'])

#绘制Bokeh折线图

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource,HoverTool

data_df = pd.DataFrame({'rkmd_pearson':rkmd_pearson,
                        'lwmd_pearson':lwmd_pearson,
                        'cyjg_pearson':cyjg_pearson,
                        'zxjl_pearson':zxjl_pearson},
                        index = dis)

source = ColumnDataSource(data_df)
output_file('房价相关系数.html')
hover = HoverTool(tooltips = [('离市中心距离','@index'),
                              ('人口密度指标相关系数','@rkmd_pearson'),
                              ('路网密度指标相关系数','@lwmd_pearson'),
                              ('餐饮价格指标相关系数','@cyjg_pearson'),
                              ('中心距离指标相关系数','@zxjl_pearson')
                              ])
p = figure(plot_width = 900,plot_height = 500,
           title = '各指标与房价在不同距离相关系数变化情况',
           tools = [hover,'pan,crosshair,xwheel_zoom,box_select,reset'])

p.line(x = 'index',y = 'rkmd_pearson',source = source,
       line_alpha = 0.8,line_color = 'red',line_dash = 'dotted',
       legend = '人口密度指标相关系数')
p.circle(x = 'index',y = 'rkmd_pearson',source = source,
         color = 'red',size = 8,alpha = 0.8,legend = '人口密度指标相关系数')

p.line(x = 'index',y = 'lwmd_pearson',source = source,
       line_alpha = 0.8,line_color = 'green',line_dash = 'dotted',
       legend = '路网密度指标相关系数')
p.circle(x = 'index',y = 'lwmd_pearson',source = source,
         color = 'green',size = 8,alpha = 0.8,legend = '路网密度指标相关系数')

p.line(x = 'index',y = 'cyjg_pearson',source = source,
       line_alpha = 0.8,line_color = 'blue',line_dash = 'dotted',
       legend = '餐饮价格指标相关系数')
p.circle(x = 'index',y = 'cyjg_pearson',source = source,
         color = 'blue',size = 8,alpha = 0.8,legend = '餐饮价格指标相关系数')

p.line(x = 'index',y = 'zxjl_pearson',source = source,
       line_alpha = 0.8,line_color = 'black',line_dash = 'dotted',
       legend = '餐中心距离指标相关系数')
p.circle(x = 'index',y = 'zxjl_pearson',source = source,
         color = 'black',size = 8,alpha = 0.8,legend = '餐中心距离指标相关系数')

p.legend.location = 'center_right'
p.legend.click_policy = 'hide'

show(p)
















