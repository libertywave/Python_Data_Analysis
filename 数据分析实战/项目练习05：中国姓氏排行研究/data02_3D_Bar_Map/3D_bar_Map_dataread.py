import pandas as pd
import os

os.chdir(r'C:\Users\Vodka\Desktop\项目练习05：中国姓氏排行研究\data02_3D_Bar_Map')  # 输入文件所在路径，例如：'C:/Users/Desktop/'
data = pd.read_excel('data.xlsx', sheetname=0,header=0)

datajs = data.to_json(orient='records',force_ascii=False)

print('转换后数据为：\n',datajs)

