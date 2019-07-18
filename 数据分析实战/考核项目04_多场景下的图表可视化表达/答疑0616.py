# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 01:06:18 2019

@author: iHJX_Alienware
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
问题1
有一个n行多列的dataframe，其中有一列的值由一堆数字和空值组成。
这一列的dtype是object类型，请问如何用这一列的均值去填补空值？
不需要转换这一列的dtype吗？
'''
df1 = pd.DataFrame({'a':np.random.randn(10)*10+10,
                    'b':np.random.randn(10)*10+20})
df1['a'].iloc[[1,3,4]] = np.nan
df1['b'].iloc[[2,5]] = np.nan
df1['a'].iloc[2] = 'hello'
df1['b'] = df1['b'].astype(np.object)
    # a列为object，有空值，有字符串数据
    # b列为float，有空值
df1['b'].fillna(df1['b'].mean(),inplace = True)
    # b列填充空值，这里b列没有字符，填充后自动转换格式
df1_digit = df1[df1['a'].str.isdigit().fillna(True)]
df1_digit['a'].fillna(df1_digit['a'].mean(),inplace = True)          
    # a列填充空值，先筛选出非字符的数据，然后填充


'''
问题2
当我用subplot方法循环创建雷达图时，怎么设置雷达图里的参数？
问题4
多场景下的图表可视化表达中第2题中的第2问：TOP8的运动员，绘制雷达图表示，能否详细讲下？
'''    
df2 = pd.read_excel('C:/Users/iHJX_Alienware/Desktop/top8data.xlsx') 
fig = plt.figure(figsize=(15,6))
plt.subplots_adjust(wspace=0.35,hspace=0.5)

n = 0
for i in df2['name'].tolist():
    n += 1
    c = plt.cm.BuPu_r(np.linspace(0, 0.7,10))[n-1]
    axi = plt.subplot(2,4,n, projection = 'polar')
    datai = df2[['BMI_nor','leg_nor','arm_nor','age_nor']][df2['name']==i].T
    scorei = df2['final'][df2['name']==i]
    angles = np.linspace(0, 2*np.pi, 4, endpoint=False)
    #axi.plot(angles,datai,linestyle = '-',lw=1,color = c)
    plt.polar(angles, datai, 'o-', linewidth=1,color = c)
    axi.fill(angles,datai,alpha=0.5,color=c)
    axi.set_thetagrids(np.arange(0.0, 360.0, 90),['BMI','腿长/身高','臂长/身高','年龄'])
    axi.set_rgrids(np.arange(0.2,1.5,0.2),'--')
    plt.title('Top%i %s: %.3f\n' %(n,i,scorei))
# 分别绘制每个运动员的评分雷达图   
    
    
'''
问题3
针对提取表格中的字段语法中“[]“的使用，有点混淆，
如data = df[['name','导演','主演']]  
'''
# 笔记
# https://mubu.com/doc/khWL0fRlNw


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    