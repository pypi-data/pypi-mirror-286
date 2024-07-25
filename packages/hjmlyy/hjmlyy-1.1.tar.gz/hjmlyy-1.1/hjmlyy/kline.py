# -*- coding:utf-8 -*-
#! python3
from facecat import *
import qstock as qs
import os
from datetime import datetime
#pip install qstock
#pip install pywencai
#pip install lxml

#请求历史数据
def queryHistoryData():
	global chart
	df = qs.get_data("600000")
	securityDatas = [] #数据集合
	print(df)
	for i in range(0, len(df)):
		sData = SecurityData()
		sData.open = float(df.iloc[i][df.columns[2]]) #开盘价
		sData.high = float(df.iloc[i][df.columns[3]]) #最高价
		sData.low = float(df.iloc[i][df.columns[4]]) #最低价
		sData.close = float(df.iloc[i][df.columns[5]]) #收盘价
		sData.volume = float(df.iloc[i][df.columns[6]]) #成交量
		sData.date = i
		securityDatas.append(sData) #放到集合中
	chart.data = securityDatas
	resetChartVisibleRecord(chart)
	calcChartIndicator(chart)
	invalidate(chart.paint)

gPaint = FCPaint() #创建绘图对象
gPaint.defaultUIStyle = "dark"

#消息循环
def WndProc(hwnd,msg,wParam,lParam):
	return WndProcDefault(gPaint,hwnd,msg,wParam,lParam)

#初始化窗体
createMainWindow(gPaint, "facecat-py", WndProc)
xml = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="facecat">
	<body>
	<chart size="200,200" name="Chart" text="Chart" dock="Fill"/>
	</body>
</html>"""
renderFaceCat(gPaint, xml)
chart = findViewByName("Chart", gPaint.views)
chart.mainIndicator = "BOLL"
chart.showIndicator = "BIAS"
chart.leftVScaleWidth = 70
chart.rightVScaleWidth = 70
chart.cycle = "tick"
invalidateView(chart)
queryHistoryData()
showWindow(gPaint)