# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 08:54:03 2019

@author: Vodka
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os
os.chdir(r'C:\Users\Vodka\Desktop\项目练习09：泰坦尼克号获救问题')

#1.查看整体生存率情况

train_data = pd.read_csv('train.csv',engine = 'python')
test_data = pd.read_csv('test.csv',engine = 'python')

sns.set_style('ticks')
train_data['Survived'].value_counts().plot.pie(autopct = '%.2f%%')

#2.存活率与年龄，性别的关系情况，和老人、小孩的情况

train_data_age = train_data[train_data['Age'].notnull()]
plt.figure(figsize = (12,5))
plt.subplot(121)
train_data_age['Age'].hist(bins = 80)
plt.xlabel = 'Age'
plt.ylabel = 'Num'

plt.subplot(122)
train_data_age.boxplot(column = 'Age',showfliers = False)

train_data_age['Age'].describe()

# 男性和女性存活情况

train_data[['Sex','Survived']].groupby('Sex').mean().plot.bar()
survive_sex = train_data.groupby(['Sex','Survived'])['Survived'].count()
print('女性存活率%.2f%%,男性存活率%.2f%%'%(survive_sex.loc['female',1] / survive_sex['female'].sum() * 100,
                                         survive_sex.loc['male',1] / survive_sex['male'].sum() * 100))

#年龄与存活率关系

fig,ax = plt.subplots(1,2,figsize = (16,8))

sns.violinplot('Pclass','Age',hue = 'Survived',data = train_data_age,split = True,ax = ax[0])
ax[0].set_title('Pclass and Age vs suevived')

sns.violinplot('Sex','Age',hue = 'Survived',data = train_data_age,split = True,ax = ax[1])
ax[1].set_title('Sex and Age vs suevived')

#老人和小孩的存活率情况

plt.figure(figsize = (18,4))
train_data_age['Age_int'] = train_data_age['Age'].astype(np.int)
average_age = train_data_age[['Age_int','Survived']].groupby('Age_int',as_index = False).mean()
sns.barplot(x = 'Age_int',y = 'Survived',data = average_age,palette='Reds')
plt.grid(linestyle = '--',alpha = 0.7)

#3.研究亲人多少与存活率的关系

#筛选有无兄弟姐妹
sibsp_df = train_data[train_data['SibSp'] != 0]
no_sibsp_df = train_data[train_data['SibSp'] == 0]

#筛选有无父母子女
parch_df = train_data[train_data['Parch'] != 0]
no_parch_df = train_data[train_data['Parch'] == 0]

plt.figure(figsize = (12,3))
plt.subplot(141)
plt.axis('equal')
sibsp_df['Survived'].value_counts().plot.pie(labels = ['No Survived','Survived'],
                                             autopct = '%.2f%%',colormap = 'Blues')

plt.subplot(142)
plt.axis('equal')
no_sibsp_df['Survived'].value_counts().plot.pie(labels = ['No Survived','Survived'],
                                             autopct = '%.2f%%',colormap = 'Blues')

plt.subplot(143)
plt.axis('equal')
parch_df['Survived'].value_counts().plot.pie(labels = ['No Survived','Survived'],
                                             autopct = '%.2f%%',colormap = 'Reds')

plt.subplot(144)
plt.axis('equal')
no_parch_df['Survived'].value_counts().plot.pie(labels = ['No Survived','Survived'],
                                             autopct = '%.2f%%',colormap = 'Reds')

#亲戚多少与存活率的关系

fig,ax = plt.subplots(1,2,figsize = (15,4))
train_data[['Parch','Survived']].groupby('Parch').mean().plot.bar(ax = ax[0])
train_data[['SibSp','Survived']].groupby('SibSp').mean().plot.bar(ax = ax[1])

train_data['family_size'] = train_data['Parch'] + train_data['SibSp']
train_data[['family_size','Survived']].groupby('family_size').mean().plot.bar(figsize = (15,4))


#4.研究票价与存活率的关系

fig,ax = plt.subplots(1,2,figsize = (15,4))
train_data['Fare'].hist(bins = 70,ax = ax[0])
train_data.boxplot(column = 'Fare',by = 'Pclass',showfliers = False,ax = ax[1])

#筛选数据
fare_survived = train_data['Fare'][train_data['Survived'] == 1]
fare_not_survived = train_data['Fare'][train_data['Survived'] == 0]

average_fare = pd.DataFrame([fare_not_survived.mean(),fare_survived.mean()])
std_fare = pd.DataFrame([fare_not_survived.std(),fare_survived.std()])

average_fare.plot(yerr = std_fare,kind = 'bar',figsize = (15,4),grid = True)

#5.利用KNN分类预测

knn_train = train_data[['Survived','Pclass','Sex','Age','Fare','family_size']].dropna()
knn_train['Sex'][knn_train['Sex'] == 'male'] = 1 
knn_train['Sex'][knn_train['Sex'] == 'female'] = 0

test_data['family_size'] = test_data['Parch'] + test_data['SibSp']
knn_test = test_data[['Pclass','Sex','Age','Fare','family_size']].dropna()
knn_test['Sex'][knn_test['Sex'] == 'male'] = 1 
knn_test['Sex'][knn_test['Sex'] == 'female'] = 0

from sklearn import neighbors

knn = neighbors.KNeighborsClassifier()
knn.fit(knn_train[['Pclass','Sex','Age','Fare','family_size']],knn_train['Survived'])

knn_test['predict'] = knn.predict(knn_test)

pre_survived = knn_test[knn_test['predict'] == 1].reset_index()
del pre_survived['index']























