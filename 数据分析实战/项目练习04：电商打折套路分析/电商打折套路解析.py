# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 14:17:40 2019

@author: Vodka
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource

# 1.读取数据
import os
os.chdir(r'C:\Users\Vodka\\Desktop\项目练习04：电商打折套路分析')

df = pd.read_excel('双十一淘宝美妆数据.xlsx',sheet_name = 0)
df.fillna(0,inplace = True)
#加载日期，提取销售日期
df.index = df['update_time']
df['date'] = df.index.day

# 2.双十一当天销售占比情况

data1 = df[['id','title','店名','date']]
#统计不同商品的销售开始和截止日期
d1 = data1[['id','date']].groupby(by = 'id').agg(['min','max'])['date']

#统计双十一当天售卖的商品id
id_11 = data1[data1['date'] == 11]['id']

d2 = pd.DataFrame({'id':id_11,
                   '双十一当天是否售卖':True})
#合并数据
id_data = pd.merge(d1,d2,left_index=True,right_on='id',how = 'left')
id_data.fillna(False,inplace=True)

n = len(d1)
n_11 = len(d2)
n_pre = n_11 / n
print('双十一当天参与活动的商品有%i个，占比为%.2f%%'%(n_11,n_pre*100))

#3.商品销售节奏分类
id_data['type'] = '待分类'
id_data['type'][(id_data['min']<11) & (id_data['max']>11)] = 'A'
id_data['type'][(id_data['min']<11) & (id_data['max']==11)] = 'B'
id_data['type'][(id_data['min']==11) & (id_data['max']>11)] = 'C'
id_data['type'][(id_data['min']==11) & (id_data['max']==11)] = 'D'
id_data['type'][id_data['双十一当天是否售卖'] == False] = 'F'
id_data['type'][id_data['max']<11] = 'E'
id_data['type'][id_data['min']>11] = 'G'

# 计算不同类别的商品数量
result1 = id_data['type'].value_counts()
#result1 = result1.loc[['A','B','C','D','E','F','G']]


from bokeh.palettes import brewer

colori = brewer['Greens'][7]
plt.axis('equal')
plt.pie(result1,labels = result1.index,
        autopct = '%.2f%%',colors = colori,
        startangle=90,radius=2,counterclock=False)

#4.未参与双十一当天活动商品去向如何
id_not11 = id_data[id_data['双十一当天是否售卖'] == False]
# 找到双十一当天未参与活动的商品的对应的原始数据
df_not11 = id_not11[['id','type']]
data_not11 = pd.merge(df_not11,df,on = 'id',how = 'left')

#筛选出暂时下架的商品
id_con1 = id_data['id'][id_data['type'] == 'F'].values

#筛选出重新上架商品
data_con2 = data_not11[['id','title','date']].groupby(by=['id','title']).count()
title_count = data_con2.reset_index()['id'].value_counts()
id_con2 = title_count[title_count > 1].index

#筛选出预售商品
data_con3 = data_not11[data_not11['title'].str.contains('预售')]
id_con3= data_con3['id'].value_counts().index

print('未参与双十一当天活动的商品中，有%i个为暂时下架商品，有%i个为重新上架商品，有%i个为预售商品'
      %(len(id_con1),len(id_con2),len(id_con3)))

#5.真正参与双十一当天活动的商品及品牌情况
#真正参与双十一当天活动的商品 = 双十一当天在售商品 + 预售商品 （可以尝试接过去重）

id_11sale_final = np.hstack((id_11,id_con3))
result2_i = pd.DataFrame({'id':id_11sale_final})

#不同品牌参与双十一当天活动的数量
x1 = pd.DataFrame({'id':id_11})
x1_df = pd.merge(x1,df,on = 'id',how = 'left')
brand_11sale = x1_df.groupby('店名')['id'].count()

#不同品牌预售的数量
x2 = pd.DataFrame({'id':id_con3})
x2_df = pd.merge(x2,df,on='id',how = 'left')
brand_ys = x2_df.groupby('店名')['id'].count()

#最终结果
result2_data = pd.DataFrame({'当天参与活动商品数量':brand_11sale,
                             '预售商品数量':brand_ys})
result2_data['总量'] = result2_data['当天参与活动商品数量'] + result2_data['预售商品数量']
result2_data.sort_values('总量',inplace = True,ascending = False)

#6.绘制堆叠图

from bokeh.models import HoverTool
from bokeh.core.properties import value

lst_brand =result2_data.index.tolist()
lst_type = result2_data.columns.tolist()[:2]
colors = ['red','green']

result2_data.index.name = 'brand'
result2_data.columns = ['sale_on11','presell','sum']
source = ColumnDataSource(result2_data)

hover = HoverTool(tooltips = [('品牌','@brand'),
                              ('双十一当天参与活动商品数量','@sale_on11'),
                              ('预售商品数量','@presell'),
                              ('真正参与双十一商品总数','@sum')
                              ])

output_file('参与双十一活动品牌数量.html')

p = figure(plot_width = 800,plot_height = 300,
           title = '各商品参与双十一说动情况',
           #tools = [hover,'reset,xwheel_zoom,pan,crosshair']
           )

p.vbar_stack(lst_type,x = 'presell',source = source,
             width = 0.8,color = colors,alpha = 0.7,
             legend = [value(x) for x in lst_type],
             muted_color = 'black',muted_alpha = 0.2
             )

show(p)

print('finished!')