# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 08:11:45 2019

@author: Vodka
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time,os
import warnings
warnings.filterwarnings('ignore')


#(1)第一轮游戏分配模拟

#初始数据
person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)],index = person_n)
fortune.index.name = 'Id'

#不考虑财富值为0的情况
round_r1 = pd.DataFrame({'pre_round':fortune[0],'lost':1})
choice_r1 = pd.Series(np.random.choice(person_n,100))
gain_r1 = pd.DataFrame({'gain':choice_r1.value_counts()})

round_r1 = round_r1.join(gain_r1)
round_r1.fillna(0,inplace = True)
fortune[1] = round_r1['pre_round'] + round_r1['gain'] - round_r1['lost']

#考虑财富值为0的情况,不分配财富给别人

person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)],index = person_n)
fortune.index.name = 'Id'

#筛选条件
round_r1 = pd.DataFrame({'pre_round':fortune[0],'lost':0})
round_r1['lost'][round_r1['pre_round'] > 0] = 1

#筛选出此轮需要分给别人钱的玩家
round_players = round_r1[round_r1['pre_round'] > 0]

choice_r1 = pd.Series(np.random.choice(person_n,len(round_players)))
gain_ri = pd.DataFrame({'gain':choice_r1.value_counts()})

round_r1 = round_r1.join(gain_r1)
round_r1.fillna(0,inplace = True)
fortune[1] = round_r1['pre_round'] + round_r1['gain'] - round_r1['lost']


#(2)创建模型

def game1(data,roundi):
    if len(data[data[roundi - 1] == 0]) > 0:
        #当数据包含财富值为0的玩家时
        round_i = pd.DataFrame({'pre_round':data[roundi - 1],'lost':0})
        con = round_i['pre_round'] > 0    #构造临时变量，存储筛选条件
        round_i['lost'][con] = 1     #筛选出财富不为的玩家需要分配的金额
        round_players_i = round_i[con]
        choice_i = pd.Series(np.random.choice(person_n,len(round_players_i)))
        gain_i = pd.DataFrame({'gain':choice_i.value_counts()})
        round_i = round_i.join(gain_i)
        round_i.fillna(0,inplace = True)
        return round_i['pre_round'] - round_i['lost'] + round_i['gain']
        #合并数据并返回该轮财富分配的结果
        
    else:
        round_i = pd.DataFrame({'pre_round':data[roundi - 1],'lost':1})
        choice_i = pd.Series(np.random.choice(person_n,100))
        gain_i = pd.DataFrame({'gain':choice_i.value_counts()})
        round_i = round_i.join(gain_i)
        round_i.fillna(0,inplace = True)
        return round_i['pre_round'] - round_i['lost'] + round_i['gain']
        #合并数据并返回该轮财富分配的结果
    
person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)],index = person_n)
fortune.index.name = 'Id'

start_time = time.time()
for i in range(1,17001):
    fortune[i] = game1(fortune,i)
    print('已完成游戏%i轮'%i)
game1_result = fortune.T
end_time = time.time()
print('总计用时%.3f秒'%(end_time - start_time))

#(3)绘制柱状图,不排序
#前100轮，每十轮绘制一次
#100至1000轮，每100轮绘制一次
#1000至17000，每500轮绘制一次

def graph1(data,start,end,length):
    for n in range(start,end,length):
        datai = data.iloc[n]
        plt.bar(datai.index,datai.values,color = 'gray',alpha = 0.8,width = 0.9)
        plt.ylim([0,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('Player ID')
        plt.ylabel('Fortune')
        plt.grid(True,color = 'gray',linestyle = '--',linewidth = 0.5)
        plt.savefig('graph1_round_%d.png'%n,dpi = 200)
        print('成功绘制第%d轮结果柱状图'%n)

os.chdir(r'C:\Users\Vodka\Desktop\项目练习08：社会财富问题分配模拟\初始模型：不排序')

graph1(game1_result,0,100,10)
graph1(game1_result,100,1000,100)
graph1(game1_result,1000,17001,500)

#(4)绘制柱状图,排序
#前100轮，每十轮绘制一次
#100至1000轮，每100轮绘制一次
#1000至17000，每500轮绘制一次

def graph2(data,start,end,length):
    for n in range(start,end,length):
        datai = data.iloc[n].sort_values().reset_index()[n]
        plt.bar(datai.index,datai.values,color = 'gray',alpha = 0.8,width = 0.9)
        plt.ylim([0,400])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('Player ID')
        plt.ylabel('Fortune')
        plt.grid(True,color = 'gray',linestyle = '--',linewidth = 0.5)
        plt.savefig('graph2_round_%d.png'%n,dpi = 200)
        print('成功绘制第%d轮结果柱状图'%n)

os.chdir(r'C:\Users\Vodka\Desktop\项目练习08：社会财富问题分配模拟\初始模型：排序')

graph2(game1_result,0,100,10)
graph2(game1_result,100,1000,100)
graph2(game1_result,1000,17001,500)

#(5)结论

round_17000_1 = pd.DataFrame({'money':game1_result.iloc[17000]}).sort_values('money',ascending = False).reset_index()
round_17000_1['fortune_pre'] = round_17000_1['money'] / round_17000_1['money'].sum()
round_17000_1['fortune_cum'] = round_17000_1['fortune_pre'].cumsum()


#(6)允许借贷情况下建立模型

def game2(data,roundi):
    round_i = pd.DataFrame({'pre_round':data[roundi - 1],'lost':1})
    choice_i = pd.Series(np.random.choice(person_n,100))
    gain_i = pd.DataFrame({'gain':choice_i.value_counts()})
    round_i = round_i.join(gain_i)
    round_i.fillna(0,inplace = True)
    return round_i['pre_round'] + round_i['gain'] - round_i['lost']

person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)],index = person_n)
fortune.index.name = 'Id'
    
start_time = time.time()
for i in range(1,17001):
    fortune[i] = game2(fortune,i)
    print('已完成游戏%i轮'%i)
game2_result = fortune.T
end_time = time.time()
print('总计用时%.3f秒'%(end_time - start_time))

round_17000_2 = pd.DataFrame({'money':game2_result.iloc[17000]}).sort_values('money',ascending = False).reset_index()
round_17000_2['fortune_pre'] = round_17000_2['money'] / round_17000_2['money'].sum()
round_17000_2['fortune_cum'] = round_17000_2['fortune_pre'].cumsum()

#(7)允许借贷情况下绘制柱状图：排序
#前100轮，每十轮绘制一次
#100至1000轮，每100轮绘制一次
#1000至17000，每500轮绘制一次

def graph3(data,start,end,length):
    for n in range(start,end,length):
        datai = data.iloc[n].sort_values().reset_index()[n]
        plt.bar(datai.index,datai.values,color = 'gray',alpha = 0.8,width = 0.9)
        plt.ylim([-200,500])
        plt.xlim([-10,110])
        plt.title('Round %d'%n)
        plt.xlabel('Player ID')
        plt.ylabel('Fortune')
        plt.grid(True,color = 'gray',linestyle = '--',linewidth = 0.5)
        plt.savefig('graph3_round_%d.png'%n,dpi = 200)
        print('成功绘制第%d轮结果柱状图'%n)

os.chdir(r'C:\Users\Vodka\Desktop\项目练习08：社会财富问题分配模拟\允许借贷情况')

graph3(game2_result,0,100,10)
graph3(game2_result,100,1000,100)
graph3(game2_result,1000,17001,500)

#(8)游戏次数与财富标准差的关系

game2_std = game2_result.std(axis = 1)
game2_std.plot(grid = True,color = 'red',figsize = (12,5),alpha = 0.6)


#(9)玩家从18岁开始，17年后35岁，期间进行游戏6200次左右，
#此时财富值小于标记为破产

game2_round6200 = pd.DataFrame({'money':game2_result.iloc[6200].sort_values().reset_index()[6200],
                                'Id':game2_result.iloc[6200].sort_values().reset_index()['Id'],
                                'color':'gray'})
game2_round6200['color'][game2_round6200['money'] < 0] = 'red'
id_pc = game2_round6200['Id'][game2_round6200['money'] < 0].tolist()

plt.figure(figsize = (12,5))
plt.bar(game2_round6200.index,game2_round6200['money'],color = game2_round6200['color'],alpha = 0.7)
plt.xlim([-10,110])
plt.ylim([-300,500])
plt.title('Round 6200')
plt.grid(True,linestyle = '--',color = 'gray',alpha = 0.8,linewidth = 0.5)


#(10)破产玩家是否逆袭

os.chdir(r'C:\Users\Vodka\Desktop\项目练习08：社会财富问题分配模拟\是否逆袭')

def graph4(data,start,end,length):
    for n in range(start,end,length):
        datai = pd.DataFrame({'money':data.iloc[n],
                              'color':'gray'})
        datai['color'].loc[id_pc] = 'red'
        datai = datai.sort_values('money').reset_index()
        plt.figure(figsize = (12,5))
        plt.bar(datai.index,datai['money'],color = datai['color'],alpha = 0.8,width = 0.8)
        plt.ylim([-300,500])
        plt.xlim([-10,110])
        plt.xlabel('Player ID')
        plt.ylabel('Fortune')
        plt.grid(True,linestyle = '--',linewidth = 0.5,color = 'gray')
        plt.savefig('graph4_round_%d.png'%n,dpi = 200)
        print('成功绘制第%d轮结果图'%n)

graph4(game2_result,6200,17000,500)

#(11)挑选10人概率增加1%，观察结果

person_p = [0.899/90 for i in range(1,101)]
for i in range(1,11):
    person_p[i] = 0.0101
    
def game3(data,roundi):
    round_i = pd.DataFrame({'pre_round':data[roundi - 1],'lost':1})
    choice_i = pd.Series(np.random.choice(person_n,100,p = person_p))
    gain_i = pd.DataFrame({'gain':choice_i.value_counts()})
    round_i = round_i.join(gain_i)
    round_i.fillna(0,inplace = True)
    return round_i['pre_round'] + round_i['gain'] - round_i['lost']

person_n = [x for x in range(1,101)]
fortune = pd.DataFrame([100 for i in range(100)],index = person_n)
fortune.index.name = 'Id'

start_time = time.time()
for n in range(1,17001):
    fortune[n] = game3(fortune,n)
    print('已经完成%d轮'%n)
game3_result = fortune.T
end_time = time.time()
print('总共用时%.3f秒'%(end_time - start_time))

#(12)绘图分析

os.chdir(r'C:\Users\Vodka\Desktop\项目练习08：社会财富问题分配模拟\概率优势')

def graph5(data,start,end,length):
    for n in range(start,end,length):
        datai = pd.DataFrame({'money':data.iloc[n],
                              'color':'gray'})
        datai['color'].loc[list(range(1,11))] = 'red'
        datai = datai.sort_values('money').reset_index()
        plt.figure(figsize = (12,5))
        plt.bar(datai.index,datai['money'],color = datai['color'],alpha = 0.8,width = 0.8)
        plt.ylim([-300,500])
        plt.xlim([-10,110])
        plt.xlabel('Player ID')
        plt.ylabel('Fortune')
        plt.title('Round %d'%n)
        plt.grid(True,linestyle = '--',linewidth = 0.5,color = 'gray')
        plt.savefig('graph5_round_%d.png'%n,dpi = 200)
        print('成功绘制第%d轮结果图'%n)

graph5(game3_result,0,100,10)
graph5(game3_result,100,1000,100)
graph5(game3_result,1000,17001,500)



print('finished')