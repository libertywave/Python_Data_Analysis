# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:51:10 2019

@author: Vodka
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource
import warnings
warnings.filterwarnings('ignore')

#导入数据
import os
os.chdir(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究')

#(1)数据加载及合并
df1 = pd.read_csv('data01.csv',engine = 'python',encoding = 'utf-8')
df2 = pd.read_csv('data02.csv',engine = 'python',encoding = 'utf-8')
df_city = pd.read_excel('中国行政代码对照表.xlsx',sheetname = 0)
df_city['行政编码'] = df_city['行政编码'].astype('object')
df0 = pd.concat([df1,df2])
df = pd.merge(df0,df_city,left_on = '户籍地城市编号',right_on = '行政编码')
df['工作地'] = df['工作地'].str[:15]

del df['户籍地城市编号']
del df['行政编码']

#（2）提取工作地的省、市、区
# 提取省
df['工作地_省'] = df['工作地'].str.split('省').str[0]

#提取市
df['工作地_市'] = df['工作地'].str.split('省').str[1].str.split('市').str[0]
df['工作地_市'][df['工作地_省'].str.len() > 5] = df['工作地_省'].str.split('市').str[0]

#提取区县
df['工作地_区县'] = ' '
df['工作地_区县'][(df['工作地'].str.contains('区')) & (df['工作地_市'].str.len() < 5)] = df['工作地'].str.split('市').str[1].str.split('区').str[0] + '区'
df['工作地_区县'][(df['工作地'].str.contains('区')) & (df['工作地_市'].str.len() > 5)] = df['工作地'].str.split('区').str[0] + '区'
df['工作地_区县'][(df['工作地'].str.contains('县')) & (df['工作地_市'].str.len() < 5)] = df['工作地'].str.split('市').str[1].str.split('县').str[0] + '县'
df['工作地_区县'][(df['工作地'].str.contains('县')) & (df['工作地_市'].str.len() > 5)] = df['工作地'].str.split('县').str[0] + '县'

#数据整理，填充未识别单元格
df['工作地_省'][df['工作地_省'].str.len() > 5] = '未识别'
df['工作地_市'][(df['工作地_市'].str.len() > 5) | (df['工作地_市'].str.len() < 2)] = '未识别'
df['工作地_区县'][(df['工作地_区县'].str.len() > 5) | (df['工作地_区县'].str.len() < 2)] = '未识别'

#重命名列名
df.columns = ['姓','工作地','户籍所在地_省','户籍所在地_市','户籍所在地_区县','户籍所在地_lng',
              '户籍所在地_lat','工作地_省','工作地_市','工作地_区县']


#（3）数据统计，筛选姓氏Top20

name_count = df0['姓'].value_counts()[:20]
result_name = pd.DataFrame({'count':name_count,
                            'count_pre':name_count / name_count.sum()})

#bokeh制作联动柱状图

from bokeh.models import HoverTool
from bokeh.layouts import gridplot

name_lst = result_name.index.tolist()
source = ColumnDataSource(result_name)

output_file('中国姓氏排行Top20.html')
hover1 = HoverTool(tooltips = [('姓氏计数','@count')])
p1 = figure(x_range = name_lst,plot_width = 800,plot_height = 300,
            title = '中国姓氏Top20计数',
            tools = [hover1,'reset,crosshair,xwheel_zoom,pan'])
p1.vbar(x = 'index',top = 'count',source = source,
        width = 0.8,alpha = 0.8,color = 'red')
p1.xgrid.grid_line_dash = [6,4]
p1.ygrid.grid_line_dash = [6,4]

hover2 = HoverTool(tooltips = [('姓氏占比','@count_pre')])
p2 = figure(x_range = p1.x_range,plot_width = 800,plot_height = 300,
            title = '中国姓氏Top20占比',
            tools = [hover2,'reset,crosshair,xwheel_zoom,pan'])
p2.vbar(x = 'index',top = 'count_pre',source = source,
        width = 0.8,alpha = 0.8,color = 'green')

p2.xgrid.grid_line_dash = [6,4]
p2.ygrid.grid_line_dash = [6,4]

p3 = gridplot([[p1],[p2]])

show(p3)

#（4）查看‘王’姓氏分布

#导出王姓数据
data_wang1 = df[df['姓'] == '王']
writer1 = pd.ExcelWriter(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\wang1.xlsx')
data_wang1.to_excel(writer1,'sheet1',index = False)
writer1.save()

data_wang2 = data_wang1.groupby(['户籍所在地_lng','户籍所在地_lat','户籍所在地_市'])['姓'].count()
data_wang2 = data_wang2.reset_index()
data_wang2.columns = ['lng','lat','name','value']
writer2 = pd.ExcelWriter(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\wang2.xlsx')
data_wang2.to_excel(writer2,'sheet1',index = False)
writer2.save()

#导出姬姓数据

data_ji1 = df[df['姓'] == '姬']
writer1 = pd.ExcelWriter(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\ji1.xlsx')
data_ji1.to_excel(writer1,'sheet1',index = False)
writer1.save()

data_ji2 = data_ji1.groupby(['户籍所在地_lng','户籍所在地_lat','户籍所在地_市'])['姓'].count()
data_ji2 = data_ji2.reset_index()
data_ji2.columns = ['lng','lat','name','value']
writer2 = pd.ExcelWriter(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\ji2.xlsx')
data_ji2.to_excel(writer2,'sheet1',index = False)
writer2.save()

#(5) 查看汤姓奔波整数（出生地与工作地的距离）

data_tang = df[['姓','户籍所在地_lng','户籍所在地_lat','工作地_市','工作地_区县']][df['姓'] == '汤']
data_tang = data_tang[data_tang['工作地_市'] != '未识别']
data_tang = data_tang[data_tang['工作地_区县'] != '未识别']
data_tang.columns = ['familyname','birth_lng','birth_lat','work_lng','work_lat']
writer_tang = pd.ExcelWriter(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\tang.xlsx')
data_tang.to_excel(writer_tang,'sheet1',index = False)
writer_tang.save()

#(6) 查看叶姓奔波整数（出生地与工作地的距离）

data_ye = df[['姓','户籍所在地_lng','户籍所在地_lat','工作地_市','工作地_区县']][df['姓'] == '叶']
data_ye = data_ye[data_ye['工作地_市'] != '未识别']
data_ye = data_ye[data_ye['工作地_区县'] != '未识别']
data_ye.columns = ['familyname','birth_lng','birth_lat','work_lng','work_lat']
writer_ye = pd.ExcelWriter(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\ye.xlsx')
data_ye.to_excel(writer_ye,'sheet1',index = False)
writer_ye.save()
















print('finished') 