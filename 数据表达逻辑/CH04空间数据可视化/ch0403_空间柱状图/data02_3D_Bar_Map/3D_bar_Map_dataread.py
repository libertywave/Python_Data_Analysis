import pandas as pd
import os

os.chdir('C:\\Users\\Hjx\\Desktop\\')  # 输入文件所在路径，例如：'C:/Users/Desktop/'
data = pd.read_excel('data.xlsx', sheetname=0,header=0)

datajs = data.to_json(orient='records',force_ascii=False)

print('转换后数据为：\n',datajs)

