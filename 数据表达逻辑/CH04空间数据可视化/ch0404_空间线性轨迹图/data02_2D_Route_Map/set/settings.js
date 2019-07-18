// 此脚本用于修改图表的参数

// 路线属性
var colorOrWidth  = 3 ; // 0代表既不用色彩也不用宽度来表示值，1代表用色彩，2代表用宽度，3代表二者皆用
var theColorRamp  = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027']; // 路线颜色
var theWidthRatio = 0.2 // 宽度与值的比值

// 固定属性，当该属性没有和值相关，会自动设成如下值
var theColor  = 'rgb(200, 35, 45)'; // 线的颜色
var theWidth  = 2;    // 线的宽度
var theOpac   = 0.3;  // 线的透明度

// 地图相关
var theCenter = [109.64630126953125,18.984220415249744]; // 中心点坐标
var theZoom   = 9; //视角远近 数字

// 动画效果
var effectShow  = true;// 是否展示动画
var theSpeed    = 0;   // 尾迹速度，当尾迹速度不等于 0 时，使用单次循环时间作为速度依据
var thePeriod   = 6;   // 单次循环时间，只有当尾迹速度为 0 时才能生效
var theEffWidth = 8;   // 尾迹宽度
var theEffLength= 0.3; // 尾迹长度

// 百度地图
// 百度地图的accesstoken需要到 html 的第18行 自行进行替换
var mapStyle= [
          {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": {
                              "color": "#021019"
                    }
          },
          {
                    "featureType": "highway",
                    "elementType": "geometry.fill",
                    "stylers": {
                              "color": "#000000"
                    }
          },
          {
                    "featureType": "highway",
                    "elementType": "geometry.stroke",
                    "stylers": {
                              "color": "#147a92"
                    }
          },
          {
                    "featureType": "arterial",
                    "elementType": "geometry.fill",
                    "stylers": {
                              "color": "#000000"
                    }
          },
          {
                    "featureType": "arterial",
                    "elementType": "geometry.stroke",
                    "stylers": {
                              "color": "#0b3d51"
                    }
          },
          {
                    "featureType": "local",
                    "elementType": "geometry",
                    "stylers": {
                              "color": "#000000"
                    }
          },
          {
                    "featureType": "land",
                    "elementType": "all",
                    "stylers": {
                              "color": "#08304b"
                    }
          },
          {
                    "featureType": "railway",
                    "elementType": "geometry.fill",
                    "stylers": {
                              "color": "#000000"
                    }
          },
          {
                    "featureType": "railway",
                    "elementType": "geometry.stroke",
                    "stylers": {
                              "color": "#08304b"
                    }
          },
          {
                    "featureType": "subway",
                    "elementType": "geometry",
                    "stylers": {
                              "lightness": -70
                    }
          },
          {
                    "featureType": "building",
                    "elementType": "geometry.fill",
                    "stylers": {
                              "color": "#000000"
                    }
          },
          {
                    "featureType": "all",
                    "elementType": "labels.text.fill",
                    "stylers": {
                              "color": "#857f7f"
                    }
          },
          {
                    "featureType": "all",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                              "color": "#000000"
                    }
          },
          {
                    "featureType": "building",
                    "elementType": "geometry",
                    "stylers": {
                              "color": "#022338"
                    }
          },
          {
                    "featureType": "green",
                    "elementType": "geometry",
                    "stylers": {
                              "color": "#062032"
                    }
          },
          {
                    "featureType": "boundary",
                    "elementType": "all",
                    "stylers": {
                              "color": "#1e1c1c"
                    }
          },
          {
                    "featureType": "manmade",
                    "elementType": "geometry",
                    "stylers": {
                              "color": "#022338"
                    }
          },
          {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": {
                              "visibility": "off"
                    }
          },
          {
                    "featureType": "all",
                    "elementType": "labels.icon",
                    "stylers": {
                              "visibility": "off"
                    }
          },
          {
                    "featureType": "all",
                    "elementType": "labels.text.fill",
                    "stylers": {
                              "color": "#2da0c6",
                              "visibility": "on"
                    }
          }
]
