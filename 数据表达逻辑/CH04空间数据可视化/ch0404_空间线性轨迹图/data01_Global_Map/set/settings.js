// 此脚本用于修改图表的参数

// 路线属性
var theColor  = '#61a2af'; // 路线颜色 'rgb(250,242,179)'
var theWidth  = 1   // 路线粗细
var theOpac   = 20; // 线条的发亮程度代表了该线条值的大小，theOpac代表了放大倍数
// 通过调整theOpac的值，使原本值过小、几乎看不见的线条 变得可见

// 地球设置相关
var theBackground = 'background.jpg'; // 背景星空图名
var theHeight     = 'bathymetry_bw_composite_4k.jpg'; // 地球高程图名
var theBase       = 'world.topo.bathy.200401.jpg'; // 地表图像图名
var theHeightScale= 0.1; // 地球表面凹凸程度
var theRotate     = true; // 是否自动旋转 true or false

// 动画效果
var effectShow    = true; // 是否展示动画
var theSpeed      = 20;   // 尾迹速度
var theEffWidth   = 2;    // 尾迹宽度
var theEffLength  = 0.4;  // 尾迹长度
var theEffColor   = '#61a2af'; // 尾迹颜色
var theEffOpac    = 0.5; // 尾迹透明度
