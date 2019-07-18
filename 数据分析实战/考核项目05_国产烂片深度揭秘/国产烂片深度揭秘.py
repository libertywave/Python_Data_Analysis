# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 08:41:41 2019

@author: Vodka
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource,HoverTool

#1、读取数据，以“豆瓣评分”为标准，看看电影评分分布，及烂片情况

import os
os.chdir(r'C:\Users\Vodka\Desktop\考核项目05_国产烂片深度揭秘')
df = pd.read_excel('moviedata.xlsx')
df = df[df['豆瓣评分'] > 0]

#查找下四分位数，绘制直方图和箱形图

q1 = df['豆瓣评分'].quantile(q=0.25)
print('豆瓣评分下四分位数为',q1)

df['豆瓣评分'].plot.hist(bins = 20,color = 'gray',grid = True,alpha = 0.8,figsize = (12,5))
df['豆瓣评分'].plot.box(vert = False,grid = True,figsize = (12,5))

# KS检验是否服从正态分布

from scipy import stats

u = df['豆瓣评分'].mean()
std = df['豆瓣评分'].std()
pvalue = stats.kstest(df['豆瓣评分'],'norm',(u,std))[1]
print('由于pvalue为%s,远小于0.05，故不服从正态分布'%pvalue)

#筛选烂片Top20

data_lp = df[df['豆瓣评分'] < q1].reset_index()
data_lp_top20 = data_lp[['电影名称','豆瓣评分','主演','导演']].sort_values('豆瓣评分').iloc[:20].reset_index()
del data_lp_top20['index']
print('烂片前20数据为',data_lp_top20)

#2.什么题材的电影烂片最多？

#筛选所有题材去重

typelist = []
for i in df[df['类型'].notnull()]['类型'].str.split('/'):
    for j in i:
        typelist.append(j.strip())

#集合可以去重，之后转换为列表
typelist = list(set(typelist))

df_type = df[df['类型'].notnull()]

#定义函数，返回值为字典，获取不同类型烂片的名字和比例

def f1(data,typei):
    dic_type_lp = {}
    datai = data[data['类型'].str.contains(typei)]
    lp_pre_i = len(datai[datai['豆瓣评分'] < 4.3]) / len(datai)
    dic_type_lp['typename'] = typei
    dic_type_lp['typecount'] = len(datai)
    dic_type_lp['type_lp_pre'] = lp_pre_i 
    return dic_type_lp

lst_type_lp = []
for i in typelist:
    dici = f1(df_type,i)
    lst_type_lp.append(dici)
    
df_type_lp = pd.DataFrame(lst_type_lp)
type_lp_top20 = df_type_lp.sort_values('type_lp_pre',ascending = False).iloc[:20]


#绘制bokeh图

type_lp_top20['size'] = type_lp_top20['typecount'] ** 0.5 * 2
source = ColumnDataSource(type_lp_top20)
lst_type = type_lp_top20['typename'].tolist()
hover = HoverTool(tooltips = [('类型','@typename'),
                              ('数据量','@typecount'),
                              ('烂片率','@type_lp_pre')])
output_file('不同类型烂片比例.html')
p = figure(x_range = lst_type,plot_width = 800,plot_height = 300,
           title = '不同类型烂片比例',
           tools = [hover,'pan,reset,xwheel_zoom,crosshair,box_select'])

p.circle(x = 'typename',y = 'type_lp_pre',source = source,size = 'size',
         line_color = 'black',line_dash = 'dotted',
         alpha = 0.8,fill_color = 'red',fill_alpha = 0.5)

show(p)

#3.和什么国家合拍更可能产生烂片？

#提取含中国大陆字段
df_loc = df[['电影名称','制片国家/地区','豆瓣评分']][df['制片国家/地区'].notnull()]
df_loc = df_loc[df_loc['制片国家/地区'].str.contains('中国大陆')]

#筛选所有合拍国家
loclst = []
for i in df_loc['制片国家/地区'].str.replace(' ','').str.split('/'):
    loclst.extend(i)
    
loclst = list(set(loclst))

#去除表示中国的字段值，留下所有的外国名

loclst.remove('中国大陆')
loclst.remove('香港')
loclst.remove('台湾')
loclst.remove('中国')

#定义函数，获得合拍国家的国名，数量以及所拍电影中烂片比例

def f2(data,loci):
    dic_loc_lp = {}
    datai = data[data['制片国家/地区'].str.contains(loci)]
    lp_pre_i = len(datai[datai['豆瓣评分'] < 4.3]) / len(datai)
    dic_loc_lp['loc'] = loci
    dic_loc_lp['loccount'] = len(datai)
    dic_loc_lp['loc_lp_pre'] = lp_pre_i 
    return dic_loc_lp

lst_loc_lp = []
for i in loclst:
    dici = f2(df_loc,i)
    lst_loc_lp.append(dici)

df_loc_lp = pd.DataFrame(lst_loc_lp)
df_loc_lp = df_loc_lp[df_loc_lp['loccount'] >= 3]
loc_lp_top = df_loc_lp.sort_values('loc_lp_pre',ascending = False)

#3.卡司数量是否和烂片有关？

#按照主演人数统计烂片数量

df['主演人数'] = df['主演'].str.split('/').str.len()

#获取所有电影的主演人数和烂片电影中的主演人数

df_role_all = df[['主演人数','电影名称']].groupby('主演人数').count()
df_role_lp = df[['主演人数','电影名称']][df['豆瓣评分'] < 4.3].groupby('主演人数').count()

#合并数据

df_role = pd.merge(df_role_all,df_role_lp,left_index = True,right_index = True)
df_role.columns = ['电影数量','烂片数量']

df_role = df_role.reset_index()

#根据主演人数分为五组，cut(),左开右闭区间

df_role['主演人数分类'] = pd.cut(x = df_role['主演人数'],
                                bins = [0,2,4,6,9,100],
                                labels = ['1-2人','3-4人','5-6人','7-9人','10人及以上'])
#根据主演人数的分类进行分组

df_role = df_role[['主演人数分类','电影数量','烂片数量']].groupby('主演人数分类').sum()
df_role['烂片比例'] = df_role['烂片数量'] / df_role['电影数量']

#不用主演的烂片比例

df_role1 = df[df['主演'].notnull()]
df_role2 = df[(df['主演'].notnull()) & (df['豆瓣评分'] < 4.3)]

#获得烂片电影中主演的名字并去重

leadrolelst = []
for i in df_role2['主演'].str.replace(' ','').str.split('/'):
    leadrolelst.extend(i)

leadrolelst = list(set(leadrolelst))

#定义函数，得到不同主演的电影数量及烂片比例

def f3(data,role):
    dic_role_lp = {}
    datai = data[data['主演'].str.contains(role)]
    if len(datai) > 10:
        lp_pre_i = len(datai[datai['豆瓣评分'] < 4.3]) / len(datai)
        dic_role_lp['role'] = role
        dic_role_lp['rolecount'] = len(datai)
        dic_role_lp['role_lp_pre'] = lp_pre_i 
    return dic_role_lp

lst_role_lp = []
for i in leadrolelst:
    dici = f3(df_role1,i)
    lst_role_lp.append(dici)

df_role_pre = pd.DataFrame(lst_role_lp)
df_role_pre.dropna(inplace = True)

#根据烂片比例由高到低提取前20的数据

role_lp_top20 = df_role_pre.sort_values('role_lp_pre',ascending = False)[:20]

#绘制bokeh图

role_lp_top20.reset_index(inplace = True)
del role_lp_top20['index']
role_range = role_lp_top20['role'].tolist()

source_role = ColumnDataSource(role_lp_top20)

hover_role = HoverTool(tooltips = [('主演','@role'),
                                   ('电影数量','@rolecount'),
                                   ('烂片比例','@role_lp_pre')])
output_file('不同主演的烂片比例.html')
p_role = figure(x_range = role_range,plot_width = 900,plot_height = 300,
                title = '不同主演的烂片比例',
                tools = [hover_role,'pan,box_select,crosshair,xwheel_zoom,reset'])

p_role.circle(x = 'role',y = 'role_lp_pre',size = 'rolecount',source = source_role,
              line_color = 'black',fill_color = 'blue',fill_alpha = 0.5)

show(p_role)


#5。不同导演每年电影产量情况是如何的？

#数据清洗，提取年份为2007-2017年

df_year = df[['电影名称','导演','豆瓣评分','上映日期']].dropna()
df_year['上映日期'] = df_year['上映日期'].str.replace(' ','')

df_year['year'] = df_year['上映日期'].str[:4]
df_year = df_year[df_year['year'].str[0] == '2']
df_year['year'] = df_year['year'].astype(np.int)
df_year = df_year[(df_year['year'] >= 2007) & (df_year['year'] <= 2017)]

#筛选导演

directorlst = []
for i in df_year['导演'].str.replace(' ','').str.split('/'):
    directorlst.extend(i)
directorlst = list(set(directorlst))

#根据循环得到所有导演烂片比例及拍电影总数量

lst_dir_lp = []
for i in directorlst:
    datai = df_year[df_year['导演'].str.contains(i)]
    if len(datai) > 10:
        dic_dir_lp = {}
        lp_pre_i = len(datai[datai['豆瓣评分'] < 4.3]) / len(datai)
        dic_dir_lp['dirname'] = i
        dic_dir_lp['dircount'] = len(datai)
        dic_dir_lp['dir_lp_pre'] = lp_pre_i
        lst_dir_lp.append(dic_dir_lp)
        
df_dir_lp = pd.DataFrame(lst_dir_lp)        
    
# 不同导演的电影产量及豆瓣均分
dir_lp_name = df_dir_lp['dirname'][df_dir_lp['dir_lp_pre'] > 0].tolist()

#定义函数

def f4(data,diri):
    datai = data[data['导演'].str.contains(diri)]
    data_movie_count = datai[['year','电影名称']].groupby('year').count()
    data_movie_score = datai[['year','豆瓣评分']].groupby('year').mean()
    data_i = pd.merge(data_movie_count,data_movie_score,left_index = True,right_index = True)
    data_i.columns = ['count','score']
    data_i['name'] = diri
    data_i['size'] = data_i['count'] * 5
    return data_i
        
datadir1 = f4(df_year,dir_lp_name[0])
datadir2 = f4(df_year,dir_lp_name[1])
datadir3 = f4(df_year,dir_lp_name[2])
datadir4 = f4(df_year,dir_lp_name[3])

from bokeh.models import BoxAnnotation

output_file('不同导演每年电影产量及均分.html')

hover_dir = HoverTool(tooltips = [('导演','@name'),
                                  ('产量','@count'),
                                  ('均分','@score')])
p_dir = figure(plot_width = 900,plot_height = 600,
               title = '不同导演每年电影产量及均分',
               tools = [hover_dir,'pan,reset,crosshair,xwheel_zoom,box_select'])

#结果中有四位导演，分别绘制散点图

source_dir1 = ColumnDataSource(datadir1)
p_dir.circle(x = 'year',y = 'score',size = 'size',source = source_dir1,
             legend = 'name',fill_color = 'red',fill_alpha = 0.5)

source_dir2 = ColumnDataSource(datadir2)
p_dir.circle(x = 'year',y = 'score',size = 'size',source = source_dir2,
             legend = 'name',fill_color = 'green',fill_alpha = 0.5)

source_dir3 = ColumnDataSource(datadir3)
p_dir.circle(x = 'year',y = 'score',size = 'size',source = source_dir3,
             legend = 'name',fill_color = 'blue',fill_alpha = 0.5)

source_dir4 = ColumnDataSource(datadir4)
p_dir.circle(x = 'year',y = 'score',size = 'size',source = source_dir4,
             legend = 'name',fill_color = 'black',fill_alpha = 0.5)

box = BoxAnnotation(top = 4.3,fill_alpha = 0.1,fill_color = 'gray')

p_dir.xgrid.grid_line_dash = 'dotted'
p_dir.ygrid.grid_line_dash = 'dotted'
p_dir.add_layout(box)
p_dir.legend.location = 'top_right'

show(p_dir)







