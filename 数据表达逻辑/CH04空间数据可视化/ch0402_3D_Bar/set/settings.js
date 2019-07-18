// 此脚本用于修改图表的参数

// 颜色分配和透明度, 及数据的大小值
var colorRamp = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'];
var theOpac   = 0.5; // 0-1之间有效
var theMin = 0 ;
var theMax = 15 ;

// x轴 y轴 z轴是以数字还是文字作为坐标
var xType = 'category'; // 文字坐标
var yType = 'category'; // 文字坐标
var zType = 'value'; // 数字坐标

// xyz轴名称
var xAxisName = 'ok';
var yAxisName = 'y';
var zAxisName = 'z';

// x轴 y轴 z轴坐标
var xAxis = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
            '7a', '8a', '9a','10a','11a',
            '12p', '1p', '2p', '3p', '4p', '5p',
            '6p', '7p', '8p', '9p', '10p', '11p'];

var yAxis = ['Saturday', 'Friday', 'Thursday',
            'Wednesday', 'Tuesday', 'Monday', 'Sunday'];

var zAxis = []; // z轴为数字坐标，故不需定义坐标轴文字

// 各轴长度
var xLen  = 200;
var yLen  = 80;
var zLen  = 100;

// 是否直接显示高度值, 及字体大小及颜色
var labelShow = false; // or false
var labelSize = 10;
var labelColor = '#000'

// 点亮时是否显示标签，及字体大小
var emphaShow = true; // or false
var emphaSize = 10;
