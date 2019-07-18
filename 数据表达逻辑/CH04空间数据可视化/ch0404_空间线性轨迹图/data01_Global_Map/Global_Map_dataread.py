import pandas as pd
import os

os.chdir('')  # 输入文件所在路径，例如：'C:/Users/Desktop/'
data = pd.read_excel('data.xlsx',  # 输入文件名字
					sheetname=0,
					header=0)

datalst = []
for i in range(len(data.index)):
	datai = [[data.ix[i,0],data.ix[i,1]],[data.ix[i,2],data.ix[i,3]],data.ix[i,4]]
	datalst.append(datai)

print('转换后数据为：\n',datalst)

