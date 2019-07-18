# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:43:58 2019

@author: Vodka
"""

import numpy as py
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import show,figure,output_file
from bokeh.models import ColumnDataSource
import os
import warnings
warnings.filterwarnings('ignore')

# 1.加载数据
os.chdir('C:\\Users\Vodka\\Desktop\\项目练习03：城市餐饮店铺选址分析')
df2 = pd.read_excel('result_point.xlsx',sheetname=0)
df2.fillna(0,inplace = True)
df2.columns = ['人口密度','道路长度','餐饮计数','素菜计数','lng','lat']

# 2.指标统计
#标准化数据
df2['rkmd_norm'] = (df2['人口密度'] - df2['人口密度'].min()) / (df2['人口密度'].max() - df2['人口密度'].min())
df2['cyrd_norm'] = (df2['餐饮计数'] - df2['餐饮计数'].min()) / (df2['餐饮计数'].max() - df2['餐饮计数'].min())
df2['tljp_norm'] = (df2['素菜计数'] - df2['素菜计数'].min()) / (df2['素菜计数'].max() - df2['素菜计数'].min())
df2['dlmd_norm'] = (df2['道路长度'] - df2['道路长度'].min()) / (df2['道路长度'].max() - df2['道路长度'].min())

# 最终得分
df2['final_score'] = df2['rkmd_norm']*0.4 + df2['cyrd_norm']*0.3 + df2['tljp_norm']*0.1 + df2['dlmd_norm']*0.2
data_final_q2 = df2.sort_values(by = 'final_score',ascending = False).reset_index()

# 3.制作空间散点图
data_final_q2['size'] = data_final_q2['final_score']*10
data_final_q2['color'] = 'green'
data_final_q2['color'].iloc[:10] = 'red'

source = ColumnDataSource(data_final_q2)


from bokeh.models import HoverTool


output_file('空间散点图.html')
hover = HoverTool(tooltips = [
        ('经度','@lng'),
        ('纬度','@lat'),
        ('最终得分','@final_score')
        ])


p = figure(plot_width = 800,plot_height = 800,x_axis_label = '经度',y_axis_label = '纬度',
           title = '空间散点图',
           tools = [hover,'box_select,reset,pan,wheel_zoom,crosshair'])

p.square(x = 'lng',y = 'lat',source = source,
         line_color = 'black',fill_alpha = 0.8,
         size = 'size',color = 'color')

show(p)

print('over')