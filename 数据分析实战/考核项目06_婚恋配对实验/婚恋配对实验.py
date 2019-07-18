# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 09:04:56 2019

@author: Vodka
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.plotting import figure,show,output_file
from bokeh.models import HoverTool,ColumnDataSource
import warnings,os,time
warnings.filterwarnings('ignore')

#1.样本数据处理

#(1)创建数据

data_norm = pd.DataFrame({'正态分布':np.random.normal(loc = 60,scale = 15,size = 10000)})
data_exp = pd.DataFrame({'指数分布':np.random.exponential(scale = 15,size = 10000) + 45})

fig,axes = plt.subplots(1,2,figsize = (14,5))

data_norm.hist(bins = 50,ax = axes[0],color = 'red',alpha = 0.6)
data_exp.hist(bins = 50,ax = axes[1],color = 'green',alpha = 0.6)

#(2)构建函数生成样本数据

def create_sample(n,gender):
    sample_data = pd.DataFrame({'fortune':np.random.exponential(scale = 15,size = n) + 45,
                                'apperance':np.random.normal(loc = 60,scale = 15,size = n),
                                'character':np.random.normal(loc = 60,scale = 15,size = n)},
                                index = [gender + str(i) for i in range(1,n+1)])
    sample_data.index.name = 'id'
    sample_data['score'] = sample_data.sum(axis = 1) / 3
    return sample_data

sample_m = create_sample(10000,'m')
sample_f = create_sample(10000,'f')

fig,axes = plt.subplots(2,1,figsize = (14,10))

sample_m[['fortune','apperance','character']].iloc[:30].plot(kind = 'bar',stacked = True,
                            colormap = 'Reds_r',grid = True,edgecolor = 'black',ax = axes[0],alpha = 0.8)
sample_f[['fortune','apperance','character']].iloc[:30].plot(kind = 'bar',stacked = True,
                            colormap = 'Blues_r',grid = True,edgecolor = 'black',ax = axes[1],alpha = 0.8)


#2.生成99个男性、99个女性样本数据，分别针对三种策略构建算法函数

#(1)第一轮模拟

#创建样本数据,以男性出发匹配
sample_m_test = create_sample(99,'m')
sample_f_test = create_sample(99,'f')
sample_m_test['strategy'] = np.random.choice([1,2,3],99)

#创建匹配的空数据集
match_success = pd.DataFrame(columns = ['m','f','strategy_type','round_n'])

#复制源数据集，每轮匹配成功的数据不再参与后续匹配
round1_f = sample_f_test.copy()
round1_m = sample_m_test.copy()

#第一轮中，男性的选择
round1_m['choice'] = np.random.choice(round1_f.index,len(round1_m))

#合并数据
round1_match = pd.merge(round1_m,round1_f,left_on = 'choice',right_index = True).reset_index()

#计算男女相差值
round1_match['score_dis'] = np.abs(round1_match['score_x'] - round1_match['score_y'])
round1_match['cha_dis'] = np.abs(round1_match['character_x'] - round1_match['character_y'])
round1_match['for_dis'] = np.abs(round1_match['fortune_x'] - round1_match['fortune_y'])
round1_match['app_dis'] = np.abs(round1_match['apperance_x'] - round1_match['apperance_y'])

# 策略1:门当户对

round1_s1_m = round1_match[round1_match['strategy'] == 1]
round1_s1_success = round1_s1_m[round1_s1_m['score_dis'] <= 20].groupby('choice').max()
round1_s1_success = pd.merge(round1_s1_success,round1_m.reset_index(),left_on = 'score_x',right_on = 'score')[['id_y','choice']]
round1_s1_success.columns = ['m','f']
round1_s1_success['strategy_type'] = 1
round1_s1_success['round_n'] = 1
round1_match.index = round1_match['choice']
round1_match = round1_match.drop(round1_s1_success['f'])

# 策略2：郎才女貌

#由于上文中round1_match已经重置index，后续用groupby时会报错列名和索引名重复，故此处重置index，后续同此
round1_match.index = list(range(0,len(round1_match)))
round1_s2_m = round1_match[round1_match['strategy'] == 2]
round1_s2_success = round1_s2_m[(round1_s2_m['apperance_y'] - round1_s2_m['apperance_x'] >= 10) &
                                (round1_s2_m['fortune_x'] - round1_s2_m['fortune_y'] >= 10)]
round1_s2_success = round1_s2_success.groupby(by = 'choice').max()
round1_s2_success = pd.merge(round1_s2_success,round1_m.reset_index(),left_on = 'score_x',right_on = 'score')[['id_y','choice']]
round1_s2_success.columns = ['m','f']
round1_s2_success['strategy_type'] = 2
round1_s2_success['round_n'] = 1
round1_match.index = round1_match['choice']
round1_match = round1_match.drop(round1_s2_success['f'])

# 策略3：志趣相投

round1_match.index = list(range(0,len(round1_match)))
round1_s3_m = round1_match[round1_match['strategy'] == 3]
round1_s3_success = round1_s3_m[(round1_s3_m['cha_dis'] < 10) & 
                                (round1_s3_m['for_dis'] < 5) &
                                (round1_s3_m['app_dis'] < 5)]
round1_s3_success = round1_s3_success.groupby('choice').max()
round1_s3_success = pd.merge(round1_s3_success,round1_m.reset_index(),left_on = 'score_x',right_on = 'score')[['id_y','choice']]
round1_s3_success.columns = ['m','f']
round1_s3_success['strategy_type'] = 3
round1_s3_success['round_n'] = 1

# 筛选出匹配成功的数据
match_success = pd.concat([match_success,round1_s1_success,round1_s2_success,round1_s3_success])

# 筛选出下一轮的匹配数据

round2_m = round1_m.drop(match_success['m'])
round2_f = round1_f.drop(match_success['f'])

#(2)构建样本数据模型

def different_strategy(data_m,data_f,roundnum):
    data_m['choice'] = np.random.choice(data_f.index,len(data_m))
    
    round_match = pd.merge(data_m,data_f,left_on = 'choice',right_index = True).reset_index()

    #计算男女相差值
    round_match['score_dis'] = np.abs(round_match['score_x'] - round_match['score_y'])
    round_match['cha_dis'] = np.abs(round_match['character_x'] - round_match['character_y'])
    round_match['for_dis'] = np.abs(round_match['fortune_x'] - round_match['fortune_y'])
    round_match['app_dis'] = np.abs(round_match['apperance_x'] - round_match['apperance_y'])

    # 策略1:门当户对
    
    s1_m = round_match[round_match['strategy'] == 1]
    s1_success = s1_m[s1_m['score_dis'] <= 20].groupby('choice').max()
    s1_success = pd.merge(s1_success,data_m.reset_index(),left_on = 'score_x',right_on = 'score')[['id_y','choice']]
    s1_success.columns = ['m','f']
    s1_success['strategy_type'] = 1
    s1_success['round_n'] = roundnum
    round_match.index = round_match['choice']
    round_match = round_match.drop(s1_success['f'])
    
    # 策略2：郎才女貌
    
    round_match.index = list(range(0,len(round_match)))
    s2_m = round_match[round_match['strategy'] == 2]
    s2_success = s2_m[(s2_m['apperance_y'] - s2_m['apperance_x'] >= 10) &
                                    (s2_m['fortune_x'] - s2_m['fortune_y'] >= 10)]
    s2_success = s2_success.groupby(by = 'choice').max()
    s2_success = pd.merge(s2_success,data_m.reset_index(),left_on = 'score_x',right_on = 'score')[['id_y','choice']]
    s2_success.columns = ['m','f']
    s2_success['strategy_type'] = 2
    s2_success['round_n'] = roundnum
    round_match.index = round_match['choice']
    round_match = round_match.drop(s2_success['f'])
    
    # 策略3：志趣相投
    
    round_match.index = list(range(0,len(round_match)))
    s3_m = round_match[round_match['strategy'] == 3]
    s3_success = s3_m[(s3_m['cha_dis'] < 10) & 
                                    (s3_m['for_dis'] < 5) &
                                    (s3_m['app_dis'] < 5)]
    s3_success = s3_success.groupby('choice').max()
    s3_success = pd.merge(s3_success,data_m.reset_index(),left_on = 'score_x',right_on = 'score')[['id_y','choice']]
    s3_success.columns = ['m','f']
    s3_success['strategy_type'] = 3
    s3_success['round_n'] = roundnum

    #设置该轮成功匹配数据
    
    data_success = pd.concat([s1_success,s2_success,s3_success])
    
    return data_success

#(3) 运行模型
    
#生成样本数据
sample_m1 = create_sample(10000,'m')
sample_f1 = create_sample(10000,'f')
sample_m1['strategy'] = np.random.choice([1,2,3],10000)

#复制源数据
test_m1 = sample_m1.copy()
test_f1 = sample_f1.copy()

#设定实验次数变量
n = 1

#设定起始时间
starttime = time.time()

success_roundn = different_strategy(test_m1,test_f1,n)
match_success1 = success_roundn
test_m1 = test_m1.drop(match_success1['m'])
test_f1 = test_f1.drop(match_success1['f'])
print('成功进行第%i轮实验，本轮实验成功匹配%i对，总共匹配%i对，还剩下%i位男性和%i位女性'%
      (n,len(success_roundn),len(match_success1),len(test_m1),len(test_f1)))

#当某轮匹配不到数据时，循环结束
while len(success_roundn) != 0:
    n += 1
    success_roundn = different_strategy(test_m1,test_f1,n)
    match_success1 = pd.concat([match_success1,success_roundn])
    test_m1 = test_m1.drop(success_roundn['m'])
    test_f1 = test_f1.drop(success_roundn['f'])
    print('成功进行第%i轮实验，本轮实验成功匹配%i对，总共匹配%i对，还剩下%i位男性和%i位女性'%
          (n,len(success_roundn),len(match_success1),len(test_m1),len(test_f1)))

endtime = time.time()

print('--------------------')
print('本次实验总共进行了%i轮，配对成功%i对\n---------------'%(n,len(match_success1)))
print('总共用时%.3f秒\n'%(endtime - starttime))

#(4)结论

print('总共%.2f%%的样本数据匹配到了对象'%(len(match_success1) / len(sample_m1) * 100))

print('择偶策略1的匹配成功率为%.2f%%'%(len(match_success1[match_success1['strategy_type']==1]) / len(sample_m1[sample_m1['strategy']==1]) * 100))
print('择偶策略2的匹配成功率为%.2f%%'%(len(match_success1[match_success1['strategy_type']==2]) / len(sample_m1[sample_m1['strategy']==2]) * 100))
print('择偶策略3的匹配成功率为%.2f%%'%(len(match_success1[match_success1['strategy_type']==3]) / len(sample_m1[sample_m1['strategy']==3]) * 100))
print('\n------------------')

#采取不同策略的男性各项择偶平均分

#合并数据并构建DataFrame
match_m1 = pd.merge(match_success1,sample_m1,left_on = 'm',right_index = True)
result_df = pd.DataFrame([{'财富均值':match_m1[match_m1['strategy_type']==1]['fortune'].mean(),
                           '内涵均值':match_m1[match_m1['strategy_type']==1]['character'].mean(),
                           '外貌均值':match_m1[match_m1['strategy_type']==1]['apperance'].mean()},
                          {'财富均值':match_m1[match_m1['strategy_type']==2]['fortune'].mean(),
                           '内涵均值':match_m1[match_m1['strategy_type']==2]['character'].mean(),
                           '外貌均值':match_m1[match_m1['strategy_type']==2]['apperance'].mean()},
                          {'财富均值':match_m1[match_m1['strategy_type']==3]['fortune'].mean(),
                           '内涵均值':match_m1[match_m1['strategy_type']==3]['character'].mean(),
                           '外貌均值':match_m1[match_m1['strategy_type']==3]['apperance'].mean()}],
                          index = ['择偶策略1','择偶策略2','择偶策略3'])

print('择偶策略1的男性 👉 财富均值%.2f，内涵均值%.2f，外貌均值%.2f'%
      (result_df.iloc[0][0],result_df.iloc[0][1],result_df.iloc[0][2]))

print('择偶策略2的男性 👉 财富均值%.2f，内涵均值%.2f，外貌均值%.2f'%
      (result_df.iloc[1][0],result_df.iloc[1][1],result_df.iloc[1][2]))

print('择偶策略3的男性 👉 财富均值%.2f，内涵均值%.2f，外貌均值%.2f'%
      (result_df.iloc[2][0],result_df.iloc[2][1],result_df.iloc[2][2]))

match_m1.boxplot(column = ['fortune','apperance','character'],figsize = (15,6),
                 by = 'strategy_type',layout = (1,3))
plt.ylim(0,150)
plt.show()


# 3.以99男+99女的样本数据，绘制匹配折线图

#（1）模拟实验，生成数据
sample_m2 = create_sample(99,'m')
sample_f2 = create_sample(99,'f')
sample_m2['strategy'] = np.random.choice([1,2,3],99)

#复制源数据
test_m2 = sample_m2.copy()
test_f2 = sample_f2.copy()

#设定实验次数变量
n = 1

#设定起始时间
starttime = time.time()

success_roundn = different_strategy(test_m2,test_f2,n)
match_success2 = success_roundn
test_m2 = test_m2.drop(match_success2['m'])
test_f2 = test_f2.drop(match_success2['f'])
print('成功进行第%i轮实验，本轮实验成功匹配%i对，总共匹配%i对，还剩下%i位男性和%i位女性'%
      (n,len(success_roundn),len(match_success2),len(test_m2),len(test_f2)))

while len(success_roundn) != 0:
    n += 1
    success_roundn = different_strategy(test_m2,test_f2,n)
    match_success2 = pd.concat([match_success2,success_roundn])
    test_m2 = test_m2.drop(success_roundn['m'])
    test_f2 = test_f2.drop(success_roundn['f'])
    print('成功进行第%i轮实验，本轮实验成功匹配%i对，总共匹配%i对，还剩下%i位男性和%i位女性'%
          (n,len(success_roundn),len(match_success2),len(test_m2),len(test_f2)))

endtime = time.time()

print('--------------------')
print('本次实验总共进行了%i轮，配对成功%i对\n---------------'%(n,len(match_success2)))
print('总共用时%.3f秒\n'%(endtime - starttime))

#（2）生成数据表格

#合并数据
graphdata1 = match_success2.copy()
graphdata1 = pd.merge(graphdata1,sample_m2,left_on = 'm',right_index = True)
graphdata1 = pd.merge(graphdata1,sample_f2,left_on = 'f',right_index = True)

#筛选编号id，制作x，y
graphdata1['x'] = '0,' + graphdata1['f'].str[1:] + ',' + graphdata1['f'].str[1:]
graphdata1['x'] = graphdata1['x'].str.split(',')
graphdata1['y'] = graphdata1['m'].str[1:] + ',' + graphdata1['m'].str[1:] + ',0'
graphdata1['y'] = graphdata1['y'].str.split(',')

from bokeh.palettes import brewer

#为每轮分配不同的颜色
round_num = graphdata1['round_n'].max()
color = brewer['Reds'][round_num + 2]
graphdata1['color'] = ''
for rn in graphdata1['round_n'].value_counts().index:
    graphdata1['color'][graphdata1['round_n'] == rn] = color[rn - 1]

graphdata1 = graphdata1[['m','f','strategy_type','round_n','score_x','score_y','x','y','color']]


#(3)bokeh绘图

output_file('不同男女匹配结果折线图.html')

p = figure(plot_width = 800,plot_height = 800,title = '配对实验过程模拟实验',
           tools = 'pan,reset,wheel_zoom,crosshair')

for datai in graphdata1.values:
    p.line(datai[-3],datai[-2],line_width = 1,line_alpha = 0.7,line_color = datai[-1],
           line_dash = 'dotted',legend = 'round %i'%datai[3])
    p.circle(datai[-3],datai[-2],size = 3,color = datai[-1],legend = 'round %i'%datai[3])

p.xgrid.grid_line_dash = [6,4]
p.ygrid.grid_line_dash = [6,4]
p.legend.location = 'top_right'
p.legend.click_policy = 'hide'
show(p)

#4.生成“不同类型男女配对成功率”矩阵图

graphdata2 = match_success1.copy()
graphdata2 = pd.merge(graphdata2,sample_m1,left_on = 'm',right_index = True)
graphdata2 = pd.merge(graphdata2,sample_f1,left_on = 'f',right_index = True)

graphdata2 = graphdata2[['m','f','apperance_x','character_x','fortune_x','apperance_y','character_y','fortune_y']]

#指标区间划分
graphdata2['app_m'] = pd.cut(graphdata2['apperance_x'],[0,50,70,300],labels = ['颜低','颜中','颜高'])
graphdata2['cha_m'] = pd.cut(graphdata2['character_x'],[0,50,70,300],labels = ['品低','品中','品高'])
graphdata2['for_m'] = pd.cut(graphdata2['fortune_x'],[0,50,70,300],labels = ['财低','财中','财高'])
graphdata2['app_f'] = pd.cut(graphdata2['apperance_y'],[0,50,70,300],labels = ['颜低','颜中','颜高'])
graphdata2['cha_f'] = pd.cut(graphdata2['character_y'],[0,50,70,300],labels = ['品低','品中','品高'])
graphdata2['for_f'] = pd.cut(graphdata2['fortune_y'],[0,50,70,300],labels = ['财低','财中','财高'])

graphdata2['type_m'] = graphdata2['app_m'].astype(np.str) + graphdata2['cha_m'].astype(np.str) + graphdata2['for_m'].astype(np.str)
graphdata2['type_f'] = graphdata2['app_f'].astype(np.str) + graphdata2['cha_f'].astype(np.str) + graphdata2['for_f'].astype(np.str)

graphdata2 = graphdata2[['m','f','type_m','type_f']]

#成功匹配率计算并标准化处理几率值

success_n = len(graphdata2)
success_chance = graphdata2.groupby(['type_m','type_f']).count().reset_index()
success_chance['chance'] = success_chance['m'] / success_n
success_chance['alpha'] = (success_chance['chance'] - success_chance['chance'].min()) / (success_chance['chance'].max() - success_chance['chance'].min()) * 10

#绘制bokeh图

output_file('不同类型男女配对成功率矩阵图.html')

mlst = success_chance['type_m'].value_counts().index.tolist()
flst = success_chance['type_f'].value_counts().index.tolist()

source = ColumnDataSource(success_chance)
hover = HoverTool(tooltips = [('男性类别','@type_m'),
                               ('女性类别','@type_f'),
                               ('匹配成功率','@chance')])
    
p1 = figure(plot_width = 800,plot_height = 800,x_range = mlst,y_range = flst,
           title = '不同类型男女配对成功率',x_axis_label = '男',y_axis_label = '女',
           tools = [hover,'reset,pan,crosshair,wheel_zoom,lasso_select'])    

p1.square_cross(x = 'type_m',y = 'type_f',source = source,size = 20,alpha = 'alpha',color = 'red')

p1.xgrid.grid_line_dash = [6,4]
p1.ygrid.grid_line_dash = [6,4]
p1.xaxis.major_label_orientation = 'vertical'

show(p1)



