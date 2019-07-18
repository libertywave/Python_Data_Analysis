import pandas as pd
import os

os.chdir('')  # 输入文件所在路径，例如：'C:/Users/Desktop/'
data = pd.read_excel('data.xlsx',  # 输入文件名字
					sheetname=0,
					header=0)

xAxis = list(data.index)

yAxis = list(data.columns)

datalst = []
xlen = len(data.index)
ylen = len(data.columns)
for x in range(xlen):
	for y in range(ylen):
		lst = [y,x,data.ix[x,y]]
		datalst.append(lst)

print('转换后数据为：\n',datalst)
print('xAxis值为：\n',xAxis)
print('yAxis值为：\n',yAxis)
print('xlen参考值为：\n',xlen*10)  # 乘10是指柱状图的格子大小为10
print('ylen参考值为：\n',ylen*10)
