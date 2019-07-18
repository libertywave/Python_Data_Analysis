import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource,HoverTool
output_file('双十一折扣率情况.html')

# 1.导入数据
import os
os.chdir(r'C:\Users\Vodka\Desktop\项目练习04：电商打折套路分析')

df = pd.read_excel('双十一淘宝美妆数据.xlsx',sheetname = 0)
df.fillna(0,inplace = True)
df.index = df['update_time']
df['date'] = df.index.day

data2 = df[['id','title','店名','date','price']]
#pd.cut()   左开右闭区间
data2['period'] = pd.cut(data2['date'],[4,10,11,14],labels = ['双十一前','双十一当天','双十一后'])
# 2。针对每个商品，评估打折情况
#筛选出是否打折数量
price = data2[['id','price','period']].groupby(['id','price']).min()
price.reset_index(inplace=True)
id_count = price['id'].value_counts()
id_type1 = id_count[id_count == 1].index
id_type2 = id_count[id_count != 1].index


#3.针对打折商品，折扣率是多少

result3_data1 = data2[['id','price','period','店名']].groupby(['id','period']).min()
result3_data1.reset_index(inplace=True)
result3_data1.dropna(axis = 0,inplace = True)

result3_before11 = result3_data1[result3_data1['period'] == '双十一前']
result3_at11 = result3_data1[result3_data1['period'] == '双十一当天']
#折扣率
result3_data2 = pd.merge(result3_before11,result3_at11,on = 'id',how = 'inner')
result3_data2['zkl'] = result3_data2['price_y'] / result3_data2['price_x']

bokeh_data = result3_data2[['id','zkl']]
bokeh_data['zkl_range'] = pd.cut(bokeh_data['zkl'],bins=np.linspace(0,1,21))
bokeh_data2 = bokeh_data.groupby('zkl_range').count()
bokeh_data2 = bokeh_data.groupby('zkl_range').count().iloc[:-1]
#计算折扣区间占比情况
bokeh_data2['zkl_pre'] = bokeh_data2['zkl'] / bokeh_data2['zkl'].sum()

bokeh_data2.index = bokeh_data2.index.astype('str')
source1 = ColumnDataSource(bokeh_data2)

lst_zkl = bokeh_data2.index.tolist()



hover1 = HoverTool(tooltips = [('折扣率','@zkl_pre')])
p1 = figure(x_range = lst_zkl,plot_width = 900,plot_height = 350,
           title = '商品折扣率统计',
           tools = [hover1,'pan,reset,xwheel_zoom,crosshair'],
           )

p1.line(x = 'zkl_range',y = 'zkl_pre',source = source1,line_color = 'black',line_dash = 'dotted')
p1.circle(x = 'zkl_range',y = 'zkl_pre',source = source1,size = 8,color = 'red',alpha = 0.8,
         legend = '折扣率',
         muted_color = 'black')

#p1.legend.click_policy = 'mute'

show(p1)	


#4.按照品牌分析打折力度

from bokeh.transform import jitter

brand = result3_data2['店名_x'].unique().tolist()
bokeh_data3 = result3_data2[['id','zkl','店名_x']] 
bokeh_data3['zkl'] = bokeh_data3['zkl'][bokeh_data3['zkl'] < 0.96]

source2 = ColumnDataSource(bokeh_data3)

output_file('不同品牌打折力度.html')
hover2 = HoverTool(tooltips = [('折扣率','@zkl')])
p2 = figure(y_range = brand,plot_width = 900,plot_height = 750,
            title = '不同品牌的折扣情况',
            tools = [hover2,'pan,reset,xwheel_zoom,crosshair'])

p2.circle(x = 'zkl',
         y = jitter('店名_x',width = 0.7,range = p2.y_range),
         source = source2,alpha = 0.3)
show(p2)


#3.套路分析

# 筛选不同品牌的折扣情况
data_zk = result3_data2[result3_data2['zkl']<0.95]
result4_zkld = data_zk.groupby('店名_y').mean()['zkl']

n_dz = data_zk['店名_y'].value_counts()
n_zs = result3_data2['店名_y'].value_counts()

result4_dzspbl = pd.DataFrame({'打折商品数':n_dz,
                               '商品总数':n_zs})

result4_dzspbl['参与打折商品比例'] = result4_dzspbl['打折商品数'] / result4_dzspbl['商品总数']
result4_dzspbl.dropna(inplace=True)

result4_sum = result2_data.copy()

#合并数据
result4_data = pd.merge(pd.DataFrame(result4_zkld),result4_dzspbl,left_index = True,right_index = True)
result4_data = pd.merge(result4_data,result4_sum,left_index = True,right_index = True)


#bokeh，制图

from bokeh.models.annotations import Span,Label,BoxAnnotation

bokeh_data4 = result4_data[['zkl','sum','参与打折商品比例']]
bokeh_data4.columns = ['zkl','amount','pre']
bokeh_data4['size'] = bokeh_data4['amount'] * 0.03

source4 = ColumnDataSource(bokeh_data4)
output_file('各品牌双十一打折情况.html')
x_mean = bokeh_data4['pre'].mean()
y_mean = bokeh_data4['zkl'].mean()

hover4 = HoverTool(tooltips = [
        ('品牌','@index'),
        ('折扣率','@zkl'),
        ('商品总数','@amount'),
        ('参与打折商品比例','@pre')
        ]) 

p4 = figure(plot_width = 600,plot_height = 600,
            title = '各品牌双十一打折情况',
            tools = [hover4,'pan,reset,wheel_zoom,crosshair,box_select'])

p4.circle(x = 'pre',y = 'zkl',source = source4,size = 'size',
          fill_color = 'red',line_color = 'black',fill_alpha = 0.6,line_dash = 'dotted'
          )

p4.xgrid.grid_line_dash = [6,4]
p4.ygrid.grid_line_dash = [6,4]

# 绘制辅助线
x = Span(location = x_mean,dimension = 'height',line_color = 'red',line_alpha = 0.8,line_width = 3)
y = Span(location = y_mean,dimension = 'width',line_color = 'red',line_alpha = 0.8,line_width = 3)
p4.add_layout(x)
p4.add_layout(y)

#第一象限
bg1 = BoxAnnotation(bottom = y_mean,left = x_mean,fill_alpha = 0.1,fill_color = 'olive')
label1 = Label(x = 0.7,y = 0.78,text = '大量少打折',text_font_size = '10pt')
p4.add_layout(bg1)
p4.add_layout(label1)


#第二象限
bg2 = BoxAnnotation(bottom = y_mean,right = x_mean,fill_alpha = 0.1,fill_color = 'olive')
label2 = Label(x = 0.2,y = 0.78,text = '少量少打折',text_font_size = '10pt')
p4.add_layout(bg2)
p4.add_layout(label2)



#第三象限
bg3 = BoxAnnotation(top = y_mean,right = x_mean,fill_alpha = 0.1,fill_color = 'olive')
label3 = Label(x = 0.2,y = 0.55,text = '少量大打折',text_font_size = '10pt')
p4.add_layout(bg3)
p4.add_layout(label3)



#第四象限
bg4 = BoxAnnotation(top = y_mean,left = x_mean,fill_alpha = 0.1,fill_color = 'olive')
label4 = Label(x = 0.7,y = 0.55,text = '大量大打折',text_font_size = '10pt')
p4.add_layout(bg4)
p4.add_layout(label4)



show(p4)

print('finished')