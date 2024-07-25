# -*- coding:utf-8 -*-
#! python3

# FaceCat-Python
#Shanghai JuanJuanMao Information Technology Co., Ltd 

import math
import time
import datetime
from operator import attrgetter
from ctypes import *
import uuid
import os
from xml.etree import ElementTree as ET
import threading
import ctypes as ct
import ctypes.wintypes as cwintypes

HCURSOR = ct.c_void_p
LRESULT = ct.c_ssize_t
wndproc_args = (cwintypes.HWND, cwintypes.UINT, cwintypes.WPARAM, cwintypes.LPARAM)
WNDPROC = ct.CFUNCTYPE(LRESULT, *wndproc_args)
kernel32 = ct.WinDLL("Kernel32")
user32 = ct.WinDLL("User32")

class WNDCLASSEXW(ct.Structure):
    _fields_ = (
        ("cbSize", cwintypes.UINT),
        ("style", cwintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ct.c_int),
        ("cbWndExtra", ct.c_int),
        ("hInstance", cwintypes.HINSTANCE),
        ("hIcon", cwintypes.HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", cwintypes.HBRUSH),
        ("lpszMenuName", cwintypes.LPCWSTR),
        ("lpszClassName", cwintypes.LPCWSTR),
        ("hIconSm", cwintypes.HICON),
    )

DefWindowProc = user32.DefWindowProcW
DefWindowProc.argtypes = wndproc_args
DefWindowProc.restype = LRESULT

CreateWindowEx = user32.CreateWindowExW
CreateWindowEx.argtypes = (cwintypes.DWORD, cwintypes.LPCWSTR, cwintypes.LPCWSTR, cwintypes.DWORD, ct.c_int, ct.c_int, ct.c_int, ct.c_int, cwintypes.HWND, cwintypes.HMENU, cwintypes.HINSTANCE, cwintypes.LPVOID)
CreateWindowEx.restype = cwintypes.HWND

CS_HREDRAW = 0x00000002
CS_VREDRAW = 0x00000001
CS_DBLCLKS = 0x00000008
WS_OVERLAPPEDWINDOW = 0X00000000 | 0X00C00000 | 0X00080000 | 0X00040000 | 0X00020000 | 0X00010000
SW_SHOW = 5
SW_HIDE = 0
SW_SHOWMAXIMIZED = 3
WM_CHAR = 258
WM_KEYDOWN = 256
WM_SYSKEYDOWN = 260
WM_KEYUP = 257
WM_SYSKEYUP = 261
WM_PAINT = 15
WM_MOUSEMOVE = 512
WM_MOUSEWHEEL = 522
WM_LBUTTONUP = 514
WM_LBUTTONDBLCLK = 515
WM_LBUTTONDOWN = 513
WM_RBUTTONDOWN = 516
WM_RBUTTONUP = 517
WM_RBUTTONDBLCLK = 518
WM_SIZE = 5
WM_ERASEBKGND = 20
WM_DESTROY = 2
CW_USEDEFAULT = -2147483648

class RECT(ct.Structure):
    _fields_ = [
        ('left', ct.c_long),
        ('top', ct.c_long),
        ('right', ct.c_long),
        ('bottom', ct.c_long),
    ]

class POINT(ct.Structure):
    _fields_ = [
        ('x', ct.c_long),
        ('y', ct.c_long)
    ]

#坐标结构
class FCPoint(object):
	def __init__(self, x, y):
		self.x = x #横坐标
		self.y = y #纵坐标
	
#大小结构
class FCSize(object):
	def __init__(self, cx, cy):
		self.cx = cx #长
		self.cy = cy #宽

#矩形结构
class FCRect(object):
	def __init__(self, left, top, right, bottom):
		self.left = left #左侧
		self.top = top #上侧
		self.right = right #右侧
		self.bottom = bottom #底部

#边距信息
class FCPadding(object):
	def __init__(self, left, top, right, bottom):
		self.left = left #左侧
		self.top = top #上侧
		self.right = right #右侧
		self.bottom = bottom #底部
#转换颜色
#strColor:颜色字符
def toColorGdiPlus(strColor):
	strColor = strColor.replace("(", "").replace(")","")
	if strColor.find("rgba") == 0:
		strColor = strColor.replace("rgba", "")
		strs = strColor.split(",")
		if len(strs) >= 4:
			r = int(strs[0])
			g = int(strs[1])
			b = int(strs[2])
			a = int(strs[3])
			rgb = ((r | (g << 8)) | (b << 0x10))
			if a == 255:
				return rgb
			elif a == 0:
				return -2000000000
			else:
				return -(rgb * 1000 + a)
	elif strColor.find("rgb") == 0:
		strColor = strColor.replace("rgb", "")
		strs = strColor.split(",")
		if len(strs) >= 3:
			r = int(strs[0])
			g = int(strs[1])
			b = int(strs[2])
			rgb = ((r | (g << 8)) | (b << 0x10))
			return rgb
	elif strColor != "none" and len(strColor) > 0:
		return int(float(strColor))
	return 0

#绘图API
class FCPaint(object):
	def __init__(self):
		self.allowPartialPaint = True #是否允许局部绘图
		self.cancelClick = False #是否退出点击
		self.clipRect = None #裁剪区域
		self.defaultUIStyle = "light" #默认样式
		self.dragBeginPoint = FCPoint(0, 0) #拖动开始时的触摸位置
		self.dragBeginRect = FCRect(0, 0, 0, 0) #拖动开始时的区域
		self.draggingView = None #正被拖动的控件
		self.drawHDC = None #双倍缓冲的hdc
		self.focusedView = None #焦点视图
		self.fontSize = 19 #当前的字体大小
		self.gdiPlusPaint = None #GDI+对象
		self.hdc = None #绘图对象
		self.hFont = None #字体
		self.hOldFont = None #旧的字体
		self.hWnd = None #句柄
		self.innerHDC = None #内部HDC
		self.innerBM = None #内部BM
		self.isDoubleClick = False #是否双击
		self.isPath = False #是否路径
		self.offsetX = 0 #横向偏移
		self.offsetY = 0 #纵向偏移
		self.memBM = None #绘图对象
		self.moveTo = False
		self.resizeColumnState = 0 #改变列宽度的状态
		self.resizeColumnBeginWidth = 0 #改变列宽度的起始值
		self.resizeColumnIndex = -1 #改变列宽度的索引
		self.scaleFactorX = 1 #横向缩放比例
		self.scaleFactorY = 1 #纵向缩放比例
		self.size = FCSize(0,0) #布局大小
		self.systemFont = "Segoe UI" #系统字体
		self.touchDownView = None #鼠标按下的视图
		self.touchMoveView = None #鼠标移动的视图
		self.touchDownPoint = FCPoint(0,0)
		self.views = [] #子视图
		self.onCalculateChartMaxMin = None #计算最大最小值的回调
		self.onClick = None #点击的回调
		self.onClickGridCell = None #点击单元格的事件回调
		self.onClickGridColumn = None #点击列头的事件回调
		self.onClickTreeNode = None #点击树节点的事件回调
		self.onContainsPoint = None #是否包含点
		self.onInvalidate = None
		self.onInvalidateView = None
		self.onInvoke = None #跨线程调用
		self.onKeyDown = None #键盘按下的回调
		self.onKeyUp = None #键盘抬起的回调
		self.onChar = None #键盘输入的回调
		self.onPaint = None #绘图回调
		self.onPaintBorder = None #绘制边线的回调
		self.onPaintCalendarDayButton = None
		self.onPaintCalendarMonthButton = None
		self.onPaintCalendarYearButton = None
		self.onPaintChartScale = None #绘制坐标轴回调
		self.onPaintChartHScale = None #绘制横坐标回调
		self.onPaintChartStock = None #绘制图表回调
		self.onPaintChartPlot = None #绘制画线回调
		self.onPaintChartCrossLine = None #绘制十字线回调
		self.onPaintGridCell = None #绘制单元格的事件回调
		self.onPaintGridColumn = None #绘制列头的事件回调
		self.onPaintCalendarHeadDiv = None
		self.onPaintTreeNode = None #绘图树节点的事件回调
		self.onMouseDown = None #鼠标按下的回调
		self.onMouseMove = None #鼠标移动的回调
		self.onMouseUp = None #鼠标抬起的回调
		self.onMouseWheel = None #鼠标滚动的回调
		self.onMouseEnter = None #鼠标进入的回调
		self.onMouseLeave = None #鼠标离开的回调
		self.onRenderViews = None
		self.onUpdateView = None #更新布局的回调
		self.textSizeCache = dict()
		self.lock = threading.Lock()
		self.invokeArgs = dict()
		self.invokeViews = dict()
		self.pInvokeMsgID = 0x0401
		self.invokeSerialID = 0
	#初始化
	def init(self):
		if self.gdiPlusPaint == None:
			self.gdiPlusPaint = GdiPlusPaint()
			self.gdiPlusPaint.init()
			self.gdiPlusPaint.createGdiPlus(self.hWnd)
	#开始绘图 
	#rect:区域
	def beginPaint(self, rect, pRect):
		self.init()
		self.gdiPlusPaint.gdiPlus.beginPaintGdiPlus(self.gdiPlusPaint.gID, self.hdc, c_int(int(rect.left)), c_int(int(rect.top)), c_int(int(rect.right)), c_int(int(rect.bottom)), c_int(int(pRect.left)), c_int(int(pRect.top)), c_int(int(pRect.right)), c_int(int(pRect.bottom )))
		self.offsetX = 0
		self.offsetY = 0
	#绘制线
	#color:颜色 
	#width:宽度 
	#style:样式 
	#x1:横坐标1 
	#y1:纵坐标1 
	#x2:横坐标2 
	#y2:纵坐标2
	def drawLine(self, color, width, style, x1, y1, x2, y2):
		inStyle = int(style)
		self.gdiPlusPaint.gdiPlus.drawLineGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_float(int(width)), c_int(inStyle), c_int(int(x1)), c_int(int(y1)), c_int(int(x2)), c_int(int(y2)))
	#绘制连续线
	#color:颜色 
	#width:宽度 
	#style:样式 
	#apt:坐标集合
	def drawPolyline(self, color, width, style, apt):
		if len(apt) > 1:
			strApt = ""
			for i in range(0,len(apt)):
				x = apt[i].x
				y = apt[i].y
				strApt += str(x) + "," + str(y)
				if i != len(apt) - 1:
					strApt += " "
			inStyle = int(style)
			self.gdiPlusPaint.gdiPlus.drawPolylineGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_float(int(width)), c_int(inStyle), c_char_p(strApt.encode(self.gdiPlusPaint.encoding)))
	#绘制多边形
	#color:颜色 
	#width:宽度 
	#style:样式 
	#apt:坐标集合
	def drawPolygon(self, color, width, style, apt):
		if len(apt) > 1:
			strApt = ""
			for i in range(0,len(apt)):
				x = apt[i].x
				y = apt[i].y
				strApt += str(x) + "," + str(y)
				if i != len(apt) - 1:
					strApt += " "
			inStyle = int(style)
			self.gdiPlusPaint.gdiPlus.drawPolygonGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_float(int(width)), c_int(inStyle), c_char_p(strApt.encode(self.gdiPlusPaint.encoding)))
	#绘制矩形 
	#color:颜色 
	#width:宽度 
	#style:样式 
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:下方坐标
	def drawRect(self, color, width, style, left, top, right, bottom):
		inStyle = int(style)
		self.gdiPlusPaint.gdiPlus.drawRectGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_float(int(width)), c_int(inStyle), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)))
	#绘制矩形 
	#color:颜色 
	#width:宽度 
	#style:样式 
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:下方坐标
	#cornerRadius:圆角
	def drawRoundRect(self, color, width, style, left, top, right, bottom, cornerRadius):
		if cornerRadius > 0:
			inStyle = int(style)
			self.gdiPlusPaint.gdiPlus.drawRoundRectGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_float(int(width)), c_int(inStyle), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)), c_int(int(cornerRadius)))
		else:
			self.drawRect(color, width, style, left, top, right, bottom)
	#绘制椭圆 
	#color:颜色 
	#width:宽度 
	#style:样式 
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:下方坐标
	def drawEllipse(self, color, width, style, left, top, right, bottom):
		inStyle = int(style)
		self.gdiPlusPaint.gdiPlus.drawEllipseGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_float(int(width)), c_int(inStyle), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)))
	#绘制文字大小 
	#text:文字 
	#color:颜色 
	#font:字体 
	#x:横坐标 
	#y:纵坐标
	def drawText(self, text, color, font, x, y):
		newFont = font.replace("Default", self.systemFont)
		self.gdiPlusPaint.gdiPlus.drawTextWithPosGdiPlus(self.gdiPlusPaint.gID, c_char_p(text.encode(self.gdiPlusPaint.encoding)), c_longlong(toColorGdiPlus(color)), c_char_p(newFont.encode(self.gdiPlusPaint.encoding)), c_int(int(x)), c_int(int(y)))
	#结束绘图
	def endPaint(self):
		self.gdiPlusPaint.gdiPlus.endPaintGdiPlus(self.gdiPlusPaint.gID)
	#填充矩形 
	#color:颜色
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:下方坐标
	def fillRect(self, color, left, top, right, bottom):
		self.gdiPlusPaint.gdiPlus.fillRectGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)))
	#填充矩形 
	#color:颜色
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#cornerRadius:圆角
	def fillRoundRect(self, color, left, top, right, bottom, cornerRadius):
		if cornerRadius > 0:
			self.gdiPlusPaint.gdiPlus.fillRoundRectGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)), c_int(int(cornerRadius)))
		else:
			self.fillRect(color, left, top, right, bottom)
	#填充多边形 
	#color:颜色
	#apt:坐标集合
	def fillPolygon(self, color, apt):
		if len(apt) > 1:
			strApt = ""
			for i in range(0,len(apt)):
				x = apt[i].x
				y = apt[i].y
				strApt += str(x) + "," + str(y)
				if i != len(apt) - 1:
					strApt += " "
			self.gdiPlusPaint.gdiPlus.fillPolygonGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_char_p(strApt.encode(self.gdiPlusPaint.encoding)))
	#填充椭圆 
	#color:颜色
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:下方坐标
	def fillEllipse(self, color, left, top, right, bottom):
		self.gdiPlusPaint.gdiPlus.fillEllipseGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)))
	#填充饼图
	#color:颜色
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:下方坐标
	#startAngle:开始角度
	#sweepAngle:持续角度
	def fillPie(self, color, left, top, right, bottom, startAngle, sweepAngle):
		self.gdiPlusPaint.gdiPlus.fillPieGdiPlus(self.gdiPlusPaint.gID, c_longlong(toColorGdiPlus(color)), c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)), c_float(startAngle), c_float(sweepAngle))
	#设置偏移量
	#offsetX:横向偏移 
	#offsetY:纵向偏移
	def setOffset(self, offsetX, offsetY):
		self.gdiPlusPaint.gdiPlus.setOffsetGdiPlus(self.gdiPlusPaint.gID, c_int(int(offsetX)), c_int(int(offsetY)))
	#获取字体大小 
	#text:文字 
	#font:字体
	def textSize(self, text, font):
		newFont = font.replace("Default", self.systemFont)
		key = text + newFont
		if (key in self.textSizeCache) == False:
			recvData = create_string_buffer(1024)
			self.gdiPlusPaint.gdiPlus.textSizeGdiPlus(self.gdiPlusPaint.gID, c_char_p(text.encode(self.gdiPlusPaint.encoding)), c_char_p(newFont.encode(self.gdiPlusPaint.encoding)), c_int(-1), recvData)
			sizeStr = str(recvData.value, encoding=self.gdiPlusPaint.encoding)
			tSize = FCSize(int(sizeStr.split(",")[0]),int(sizeStr.split(",")[1]))
			self.textSizeCache[key] = tSize
			return tSize
		else:
			return self.textSizeCache[key]
	#绘制矩形 
	#text文字 
	#color:颜色 
	#font:字体 
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:方坐标
	def drawTextAutoEllipsis(self, text, color, font, left, top, right, bottom):
		tSize = self.textSize(text, font)
		if tSize.cx < right - left:
			self.drawText(text, color, font, left, top)
		else:
			if tSize.cx > 0:
				subLen = 3
				while (1 == 1):
					newLen = len(text) - subLen
					if newLen > 0:
						newText = text[:newLen] + "..."
						tSize = self.textSize(newText, font)
						if tSize.cx < right - left:
							self.drawText(newText, color, font, left, top)
							break
						else:
							subLen += 3
					else:
						break
	#设置裁剪
	#left:左侧坐标 
	#top:上方坐标 
	#right:右侧坐标 
	#bottom:方坐标
	def setClip(self, left, top, right, bottom):
		return self.gdiPlusPaint.gdiPlus.setClipGdiPlus(self.gdiPlusPaint.gID, c_int(int(left)), c_int(int(top)), c_int(int(right)), c_int(int(bottom)))

#调用Gdi+的DLL
class GdiPlusPaint(object):
	def __init__(self):
		self.gdiPlus = None #GDI+对象
		self.gID = 0 #GDI+的编号
		self.encoding = "gbk" #解析编码
	#初始化
	def init(self):
		current_file_path = os.path.abspath(__file__)
		current_file_dir = os.path.dirname(current_file_path)
		self.gdiPlus = cdll.LoadLibrary(current_file_dir + r"\\facecatcpp.dll")
		cdll.argtypes = [c_char_p, c_int, c_float, c_double, c_long, c_wchar_p, c_longlong]
	#创建GDI+
	def createGdiPlus(self, hWnd):
		self.gID = self.gdiPlus.createGdiPlus(hWnd)
	#销毁GDI+
	def deleteGdiPlus(self):
		return self.gdiPlus.deleteGdiPlus(self.gID)
    #添加曲线
    #rect 矩形区域
    #startAngle 从x轴到弧线的起始点沿顺时针方向度量的角（以度为单位）
    #sweepAngle 从startAngle参数到弧线的结束点沿顺时针方向度量的角（以度为单位）
	def addArc(self, left, top, right, bottom, startAngle, sweepAngle):
		return self.gdiPlus.addArcGdiPlus(self.gID, c_int(left), c_int(top), c_int(right), c_int(bottom), c_float(startAngle), c_float(sweepAngle))
	#添加贝赛尔曲线
    #strApt 点阵字符串 x1,y1 x2,y2...
	def addBezier(self, strApt):
		return self.gdiPlus.addBezierGdiPlus(self.gID, c_char_p(strApt.encode(self.encoding)))
	#添加曲线
    #strApt 点阵字符串 x1,y1 x2,y2...
	def addCurve(self, strApt):
		return self.gdiPlus.addCurveGdiPlus(self.gID, c_char_p(strApt.encode(self.encoding)))
	#添加椭圆
    #rect 矩形
	def addEllipse(self, left, top, right, bottom):
		return self.gdiPlus.addEllipseGdiPlus(self.gID, c_int(left), c_int(top), c_int(right), c_int(bottom))
	#添加直线
    #x1 第一个点的横坐标
    #y1 第一个点的纵坐标
    #x2 第二个点的横坐标
    #y2 第二个点的纵坐标
	def addLine(self, x1, y1, x2, y2):
		return self.gdiPlus.addLineGdiPlus(self.gID, c_int(x1), c_int(y1), c_int(x2), c_int(y2))
	#添加矩形
    #rect 区域
	def addRect(self, left, top, right, bottom):
		return self.gdiPlus.addRectGdiPlus(self.gID, c_int(left), c_int(top), c_int(right), c_int(bottom))
	#添加扇形
    #rect 矩形区域
    #startAngle 从x轴到弧线的起始点沿顺时针方向度量的角（以度为单位）
    #sweepAngle 从startAngle参数到弧线的结束点沿顺时针方向度量的角（以度为单位）
	def addPie(self, left, top, right, bottom, startAngle, sweepAngle):
		return self.gdiPlus.addPieGdiPlus(self.gID, c_int(left), c_int(top), c_int(right), c_int(bottom), c_float(startAngle), c_float(sweepAngle))
    #添加文字
    #text 文字
    #font 字体
    #rect 区域
	def addText(self, text, font, left, top, right, bottom, width):
		return self.gdiPlus.addTextGdiPlus(self.gID, c_char_p(text.encode(self.encoding)), c_char_p(font.encode(self.encoding)), c_int(left), c_int(top), c_int(right), c_int(bottom), c_int(width))
	#开始导出
    #exportPath  路径
    #rect 区域
	def beginExport(self, exportPath, left, top, right, bottom):
		return self.gdiPlus.beginExportGdiPlus(self.gID, c_char_p(exportPath.encode(self.encoding)), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#开始绘图
	#hdc HDC
	#wRect 窗体区域
	#pRect 刷新区域
	def beginPaint(self, hDC, wLeft, wTop, wRight, wBottom, pLeft, pTop, pRight, pBottom):
		return self.gdiPlus.beginPaintGdiPlus(self.gID, hDC, c_int(wLeft), c_int(wTop), c_int(wRight), c_int(wBottom), c_int(pLeft), c_int(pTop), c_int(pRight), c_int(pBottom))
	#开始一段路径
	def beginPath(self):
		return self.gdiPlus.beginPathGdiPlus(self.gID)
	#裁剪路径
	def clipPath(self):
		return self.gdiPlus.clipPathGdiPlus(self.gID)
	#清除缓存
	def clearCaches(self):
		return self.gdiPlus.clearCachesGdiPlus(self.gID)
	#闭合路径
	def closeFigure(self):
		return self.gdiPlus.closeFigureGdiPlus(self.gID)
	#结束一段路径
	def closePath(self):
		return self.gdiPlus.closePathGdiPlus(self.gID)
	#绘制弧线
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #rect 矩形区域
    #startAngle 从x轴到弧线的起始点沿顺时针方向度量的角（以度为单位）
    #sweepAngle 从startAngle参数到弧线的结束点沿顺时针方向度量的角（以度为单位）
	def drawArc(self, dwPenColor, width, style, left, top, right, bottom, startAngle, sweepAngle):
		return self.gdiPlus.drawArcGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_int(left), c_int(top), c_int(right), c_int(bottom), c_float(startAngle), c_float(sweepAngle))
	#设置贝赛尔曲线
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #strApt 点阵字符串 x1,y1 x2,y2...
	def drawBezier(self, dwPenColor, width, style, strApt):
		return self.gdiPlus.drawBezierGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_char_p(strApt.encode(self.encoding)))
	#绘制曲线
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #strApt 点阵字符串 x1,y1 x2,y2...
	def drawCurve(self, dwPenColor, width, style, strApt):
		return self.gdiPlus.drawCurveGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_char_p(strApt.encode(self.encoding)))
	#绘制椭圆
    #dwPenColor 颜色
    #width 宽度
    # style 样式
    #left 左侧坐标
    #top 顶部左标
    #right 右侧坐标
    #bottom 底部坐标
	def drawEllipse(self, dwPenColor, width, style, left, top, right, bottom):
		return self.gdiPlus.drawEllipseGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#绘制图片
    #imagePath 图片路径
    #rect 绘制区域
	def drawImage(self, imagePath, left, top, right, bottom):
		return self.gdiPlus.drawImageGdiPlus(self.gID, c_char_p(imagePath.encode(self.encoding)), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#绘制直线
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #x1 第一个点的横坐标
    #y1 第一个点的纵坐标
    #x2 第二个点的横坐标
    #y2 第二个点的纵坐标
	def drawLine(self, dwPenColor, width, style, x1, y1, x2, y2):
		return self.gdiPlus.drawLineGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_int(x1), c_int(y1), c_int(x2), c_int(y2))
	#绘制直线
    #dwPenColor 颜色
    #width 宽度
    #style 样式
	def drawPath(self, dwPenColor, width, style):
		return self.gdiPlus.drawPathGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style))
	#绘制扇形
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #rect 矩形区域
    #startAngle 从x轴到弧线的起始点沿顺时针方向度量的角（以度为单位）
    #sweepAngle 从startAngle参数到弧线的结束点沿顺时针方向度量的角（以度为单位）
	def drawPie(self, dwPenColor, width, style, left, top, right, bottom, startAngle, sweepAngle):
		return self.gdiPlus.drawPieGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_int(left), c_int(top), c_int(right), c_int(bottom), c_float(startAngle), c_float(sweepAngle))
	#绘制多边形
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #strApt 点阵字符串 x1,y1 x2,y2...
	def drawPolygon(self, dwPenColor, width, style, strApt):
		return self.gdiPlus.drawPolygonGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_char_p(strApt.encode(self.encoding)))
	#绘制大量直线
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #strApt 点阵字符串 x1,y1 x2,y2...
	def drawPolyline(self, dwPenColor, width, style, strApt):
		return self.gdiPlus.drawPolylineGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_char_p(strApt.encode(self.encoding)))
	#绘制矩形
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #rect 矩形区域
	def drawRect(self, dwPenColor, width, style, left, top, right, bottom):
		return self.gdiPlus.drawRectGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#绘制圆角矩形
    #dwPenColor 颜色
    #width 宽度
    #style 样式
    #rect 矩形区域
    #cornerRadius 边角半径
	def drawRoundRect(self, dwPenColor, width, style, left, top, right, bottom, cornerRadius):
		return self.gdiPlus.drawRoundRectGdiPlus(self.gID, dwPenColor, c_float(width), c_int(style), c_int(left), c_int(top), c_int(right), c_int(bottom), c_int(cornerRadius))
	#绘制文字
    #text 文字
    #dwPenColor 颜色
    #font 字体
    #rect 矩形区域
	def drawText(self, strText, dwPenColor, font, left, top, right, bottom, width):
		return self.gdiPlus.drawTextGdiPlus(self.gID, c_char_p(strText.encode(self.encoding)), dwPenColor, c_char_p(font.encode(self.encoding)), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#绘制文字
    #text 文字
    #dwPenColor 颜色
    #font 字体
    #rect 矩形区域
	def drawTextWithPos(self, strText, dwPenColor, font, x, y):
		return self.gdiPlus.drawTextWithPosGdiPlus(self.gID, c_char_p(strText.encode(self.encoding)), dwPenColor, c_char_p(font.encode(self.encoding)), c_int(x), c_int(y))
	#绘制自动省略结尾的文字
    #text 文字
    #dwPenColor 颜色
    #font 字体
    #rect 矩形区域
	def drawTextAutoEllipsis(self, strText, dwPenColor, font, left, top, right, bottom):
		return self.gdiPlus.drawTextAutoEllipsisGdiPlus(self.gID, c_char_p(strText.encode(self.encoding)), dwPenColor, c_char_p(font.encode(self.encoding)), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#结束导出
	def endExport(self):
		return self.gdiPlus.endExportGdiPlus(self.gID)
	#结束绘图
	def endPaint(self):
		return self.gdiPlus.endPaintGdiPlus(self.gID)
	#反裁剪路径
	def excludeClipPath(self):
		return self.gdiPlus.excludeClipPathGdiPlus(self.gID)
	#填充椭圆
    #dwPenColor 颜色
    #rect 矩形区域
	def fillEllipse(self, dwPenColor, left, top, right, bottom):
		return self.gdiPlus.fillEllipseGdiPlus(self.gID, dwPenColor, c_int(left), c_int(top), c_int(right), c_int(bottom))
	#绘制渐变椭圆
    #dwFirst 开始颜色
    #dwSecond  结束颜色
    #rect 矩形区域
    #angle 角度
	def fillGradientEllipse(self, dwFirst, dwSecond, left, top, right, bottom, angle):
		return self.gdiPlus.fillGradientEllipseGdiPlus(self.gID, dwFirst, dwSecond, c_int(left), c_int(top), c_int(right), c_int(bottom), c_int(angle))
	#填充渐变路径
    #dwFirst 开始颜色
    #dwSecond  结束颜色
    #rect 矩形区域
    #angle 角度
	def fillGradientPath(self, dwFirst, dwSecond, left, top, right, bottom, angle):
		return self.gdiPlus.fillGradientPathGdiPlus(self.gID, dwFirst, dwSecond, c_int(left), c_int(top), c_int(right), c_int(bottom), c_int(angle))
	#绘制渐变的多边形
    #dwFirst 开始颜色
    #dwSecond  开始颜色
    #strApt 点阵字符串 x1,y1 x2,y2...
    #angle 角度
	def fillGradientPolygon(self, dwFirst, dwSecond, strApt, angle):
		return self.gdiPlus.fillGradientPolygonGdiPlus(self.gID, dwFirst, dwSecond, c_char_p(strApt.encode(self.encoding)), c_int(angle))
	#绘制渐变矩形
    #dwFirst 开始颜色
    #dwSecond 开始颜色
    #rect 矩形
    #cornerRadius 边角半径
    #angle 角度
	def fillGradientRect(self, dwFirst, dwSecond, left, top, right, bottom, cornerRadius, angle):
		return self.gdiPlus.fillGradientRectGdiPlus(self.gID, dwFirst, dwSecond, c_int(left), c_int(top), c_int(right), c_int(bottom), c_int(cornerRadius), c_int(angle))
	#填充路径
    #dwPenColor 颜色
	def fillPath(self, dwPenColor):
		return self.gdiPlus.fillPathGdiPlus(self.gID, dwPenColor)
	#绘制扇形
    #dwPenColor 颜色
    #rect 矩形区域
    #startAngle 从x轴到弧线的起始点沿顺时针方向度量的角（以度为单位）
    #sweepAngle 从startAngle参数到弧线的结束点沿顺时针方向度量的角（以度为单位）
	def fillPie(self, dwPenColor, left, top, right, bottom, startAngle, sweepAngle):
		return self.gdiPlus.fillPieGdiPlus(self.gID, dwPenColor, c_int(left), c_int(top), c_int(right), c_int(bottom), c_float(startAngle), c_float(sweepAngle))
	#填充多边形
    #dwPenColor 颜色
    #strApt 点阵字符串 x1,y1 x2,y2...
	def fillPolygon(self, dwPenColor, strApt):
		return self.gdiPlus.fillPolygonGdiPlus(self.gID, dwPenColor, c_char_p(strApt.encode(self.encoding)))
	#填充矩形
    #dwPenColor 颜色
    #left 左侧坐标
    #top 顶部左标
    #right 右侧坐标
    #bottom 底部坐标
	def fillRect(self, dwPenColor, left, top, right, bottom):
		return self.gdiPlus.fillRectGdiPlus(self.gID, dwPenColor, c_int(left), c_int(top), c_int(right), c_int(bottom))
	#填充圆角矩形
    #dwPenColor 颜色
    #rect 矩形区域
    #cornerRadius 边角半径
	def fillRoundRect(self, dwPenColor, left, top, right, bottom, cornerRadius):
		return self.gdiPlus.fillRoundRectGdiPlus(self.gID, dwPenColor, c_int(left), c_int(top), c_int(right), c_int(bottom), c_int(cornerRadius))
	#设置裁剪区域
    #rect 区域
	def setClip(self, left, top, right, bottom):
		return self.gdiPlus.setClipGdiPlus(self.gID, c_int(left), c_int(top), c_int(right), c_int(bottom))
	#设置直线两端的样式
    #startLineCap 开始的样式
    #endLineCap  结束的样式
	def setLineCap(self, startLineCap, endLineCap):
		return self.gdiPlus.setLineCapGdiPlus(self.gID, c_int(startLineCap), c_int(endLineCap))
	#设置偏移
    #mp 偏移坐标
	def setOffset(self, offsetX, offsetY):
		return self.gdiPlus.setOffsetGdiPlus(self.gID, c_int(offsetX), c_int(offsetY))
	#设置透明度
    #opacity 透明度
	def setOpacity(self, opacity):
		return self.gdiPlus.setOpacityGdiPlus(self.gID, c_float(opacity))
	#设置资源的路径
    #resourcePath 资源的路径
	def setResourcePath(self, resourcePath):
		return self.gdiPlus.setResourcePathGdiPlus(self.gID, c_char_p(resourcePath.encode(self.encoding)))
	#设置旋转角度
    #rotateAngle 旋转角度
	def setRotateAngle(self, rotateAngle):
		return self.gdiPlus.setRotateAngleGdiPlus(self.gID, c_int(rotateAngle))
	#设置缩放因子
    #scaleFactorX 横向因子
    #scaleFactorY 纵向因子
	def setScaleFactor(self, scaleFactorX, scaleFactorY):
		return self.gdiPlus.setScaleFactorGdiPlus(self.gID, c_double(scaleFactorX), c_double(scaleFactorY))
	#获取文字大小
    #text 文字
    #font 字体
	#width 字符最大宽度
	#data 返回数据 create_string_buffer(1024000) cx,cy
	def textSize(self, strText, font, width, data):
		return self.gdiPlus.textSizeGdiPlus(self.gID, c_char_p(strText.encode(self.encoding)), c_char_p(font.encode(self.encoding)), c_int(width), data)
	#消息循环
	#hWnd 句柄
	#message 消息ID
	def onMessage(self, hWnd, message, wParam, lParam):
		return self.gdiPlus.onMessage(self.gID, hWnd, message, wParam, lParam)
	#创建视图
	#typeStr 类型
	#name 名称
	def createView(self, typeStr, name):
		return self.gdiPlus.createView(self.gID, c_char_p(typeStr.encode(self.encoding)), c_char_p(name.encode(self.encoding)))
	#设置属性
	#name 名称
	#atrName 属性名称
	#atrValue 属性值
	def setAttribute(self, name, atrName, atrValue):
		return self.gdiPlus.setAttribute(self.gID, c_char_p(name.encode("gbk")), c_char_p(atrName.encode("gbk")), c_char_p(atrValue.encode("gbk")))
	#获取属性
	#name 名称
	#atrName 属性名称
	#data 返回数据 create_string_buffer(1024000)
	def getAttribute(self, name, atrName, data):
		return self.gdiPlus.getAttribute(self.gID, c_char_p(name.encode("gbk")), c_char_p(atrName.encode("gbk")), data)
	#获取属性
	#name 名称
    #left 左侧坐标
    #top 顶部左标
    #right 右侧坐标
    #bottom 底部坐标
	def paintView(self, name, left, top, right, bottom):
		return self.gdiPlus.paintView(self.gID, c_char_p(name.encode(self.encoding)), c_int(left), c_int(top), c_int(right), c_int(bottom))
	#设置焦点
	#name 名称
	def focusView(self, name):
		return self.gdiPlus.focusView(self.gID, c_char_p(name.encode(self.encoding)))
	#设置焦点
	#name 名称
	def unFocusView(self, name):
		return self.gdiPlus.unFocusView(self.gID, c_char_p(name.encode(self.encoding)))
	#鼠标按下视图
	#name 名称
	#x 横坐标
	#y 纵坐标
	#buttons 按钮
	#clicks 点击次数
	def mouseDownView(self, name, x, y, buttons, clicks):
		return self.gdiPlus.mouseDownView(self.gID, c_char_p(name.encode(self.encoding)), c_int(x), c_int(y), c_int(buttons), c_int(clicks))
	#鼠标抬起视图
	#name 名称
	#x 横坐标
	#y 纵坐标
	#buttons 按钮
	#clicks 点击次数
	def mouseUpView(self, name, x, y, buttons, clicks):
		return self.gdiPlus.mouseUpView(self.gID, c_char_p(name.encode(self.encoding)), c_int(x), c_int(y), c_int(buttons), c_int(clicks))
	#鼠标移动视图
	#name 名称
	#x 横坐标
	#y 纵坐标
	#buttons 按钮
	#clicks 点击次数
	def mouseMoveView(self, name, x, y, buttons, clicks):
		return self.gdiPlus.mouseMoveView(self.gID, c_char_p(name.encode(self.encoding)), c_int(x), c_int(y), c_int(buttons), c_int(clicks))
	#鼠标滚动视图
	#name 名称
	#x 横坐标
	#y 纵坐标
	#buttons 按钮
	#clicks 点击次数
	#delta 滚动值
	def mouseWheelView(self, name, x, y, buttons, clicks, delta):
		return self.gdiPlus.mouseWheelView(self.gID, c_char_p(name.encode(self.encoding)), c_int(x), c_int(y), c_int(buttons), c_int(clicks), c_int(delta))
	#设置光标
	#cursor 光标
	def setCursor(self, cursor):
		return self.gdiPlus.setCursor(self.gID, c_char_p(cursor.encode("gbk")))
	#移除原生视图
	#name 名称
	def removeView(self, name):
		return self.gdiPlus.removeView(self.gID, c_char_p(name.encode("gbk")))

#基础视图
class FCView(object):
	def __init__(self):
		self.align = "left" #横向布局
		self.allowDrag = False #是否允许拖动
		self.allowResize = False #是否可以拖动改变大小
		self.allowDraw = True #是否允许绘图
		self.allowDragScroll = False #是否允许拖动滚动
		self.allowPreviewsEvent = False #是否允许预处理事件
		self.autoHide = False #是否自动隐藏
		self._backColor = "rgb(255,255,255)" #背景色
		self.backImage = "" #背景图片
		self._borderColor = "rgb(150,150,150)" #边线色
		self.borderWidth = 1 #边线宽度
		self.clipRect = None #裁剪区域
		self.cornerRadius = 0 #圆角
		self.cursor = "" #光标
		self.dock = "none" #悬浮状态
		self.downScrollHButton = False #是否按下横向滚动条
		self.downScrollVButton = False #是否按下纵向滚动条
		self.displayOffset = True #是否显示偏移量
		self.enabled = True #是否可用
		self.exAttributes = dict() #额外属性
		self.exView = False #是否扩展视图
		self._font = "Default,14" #字体
		self.hoverScrollHButton = False #是否悬停横向滚动条
		self.hoverScrollVButton = False #是否悬停纵向滚动条
		self.hoveredColor = "none" #鼠标悬停时的颜色
		self.hScrollIsVisible = False #横向滚动是否显示
		self.hWnd = None #子视图句柄
		self.location = FCPoint(0,0) #坐标
		self.margin = FCPadding(0,0,0,0) #外边距
		self.maximumSize = FCSize(0,0) #最大大小
		self.padding = FCPadding(0,0,0,0) #内边距
		self.paint = None #绘图对象
		self.parent = None #父视图
		self.pushedColor = "rgb(200,200,200)" #鼠标按下时的颜色
		self.resizePoint = -1 #调整尺寸的点
		self.scrollV = 0 #纵向滚动
		self.scrollH = 0 #横向滚动
		self.scrollSize = 8 #滚动条的大小
		self.showHScrollBar = False #是否显示横向滚动条
		self.showVScrollBar = False #是否显示横向滚动条
		self.scrollBarColor = "rgb(200,200,200)" #滚动条的颜色
		self.scrollBarHoveredColor = "rgb(42,138,195)" #滚动条悬停的颜色
		self.size = FCSize(100,20) #大小
		self.startPoint = None #起始点
		self.startScrollH = 0 #开始滚动的值
		self.startScrollV = 0 #结束滚动的值
		self.startRect = FCRect(0,0,0,0) #移动开始时的视图矩形
		self.tabIndex = 0 #Tab索引
		self.tabStop = False #是否支持Tab
		self._text = "" #文字
		self._textColor = "rgb(0,0,0)" #前景色
		self.topMost = False #是否置顶
		self.touchDownTime = 0 #鼠标按下的时间
		self.verticalAlign = "top" #纵向布局
		self.viewName = "" #名称
		self.visible = True #可见性
		self.views = [] #子视图
		self.viewType = "" #类型
		self.vScrollIsVisible = False #纵向滚动是否显示
		self.onPaint = None #重绘回调
		self.onPaintBorder = None #重绘边线回调
		self.onClick = None #点击方法
		self.onMouseDown = None  #鼠标按下
		self.onMouseMove = None #鼠标移动
		self.onMouseWheel = None #鼠标滚动
		self.onMouseUp = None #鼠标抬起
		self.onKeyDown = None #键盘按下
		self.onKeyUp = None #键盘抬起
		self.onMouseEnter = None #鼠标进入的回调
		self.onMouseLeave = None #鼠标离开的回调
		self.onInvoke = None #跨线程调用
	@property
	def text(self):
		if self.exView and self.viewType == "textbox":
			self._text = getViewAttribute(self, "text")
		return self._text
	@text.setter
	def text(self, value):
		self._text = value
		if self.exView and self.viewType == "textbox":
			setViewAttribute(self, "text", value)
	@property
	def backColor(self):
		if self.exView and self.viewType == "textbox":
			self._backColor = getViewAttribute(self, "backcolor")
		return self._backColor
	@backColor.setter
	def backColor(self, value):
		self._backColor = value
		if self.exView and self.viewType == "textbox":
			setViewAttribute(self, "backcolor", value)
	@property
	def borderColor(self):
		if self.exView and self.viewType == "textbox":
			self._borderColor = getViewAttribute(self, "bordercolor")
		return self._borderColor
	@borderColor.setter
	def borderColor(self, value):
		self._borderColor = value
		if self.exView and self.viewType == "textbox":
			setViewAttribute(self, "bordercolor", value)
	@property
	def textColor(self):
		if self.exView and self.viewType == "textbox":
			self._textColor = getViewAttribute(self, "textcolor")
		return self._textColor
	@textColor.setter
	def textColor(self, value):
		self._textColor = value
		if self.exView and self.viewType == "textbox":
			setViewAttribute(self, "textcolor", value)
	@property
	def font(self):
		if self.exView and self.viewType == "textbox":
			self._font = getViewAttribute(self, "font")
		return self._font
	@font.setter
	def font(self, value):
		self._font = value
		if self.exView and self.viewType == "textbox":
			setViewAttribute(self, "font", value)

#按钮
class FCButton(FCView):
	def __init__(self):
		super().__init__()
		self.viewType = "button" #类型
	pass

#标签
class FCLabel(FCView):
	def __init__(self):
		super().__init__()
		self.backColor = "none" #背景色
		self.viewType = "label" #类型
	pass

#文本框
class FCTextBox(FCView):
	def __init__(self):
		super().__init__()
		self.viewType = "textbox" #类型
	pass

#图层
class FCDiv(FCView):
	def __init__(self):
		super().__init__()
		self.viewType = "div" #类型
	pass
	
#复选按钮
class FCCheckBox(FCView):
	def __init__(self):
		super().__init__()
		self.buttonSize = FCSize(16,16) #按钮的大小
		self.checked = True #是否选中
		self.viewType = "checkbox" #类型
	pass

#单选按钮
class FCRadioButton(FCView):
	def __init__(self):
		super().__init__()
		self.buttonSize = FCSize(16,16) #按钮的大小
		self.checked = False #是否选中
		self.groupName = "" #组别
		self.viewType = "radiobutton" #类型
	pass

#页
class FCTabPage(FCView):
	def __init__(self):
		super().__init__()
		self.headerButton = None #页头的按钮
		self.viewType = "tabpage" #类型
		self.visible = False #是否可见
	pass

#多页夹
class FCTabView(FCView):
	def __init__(self):
		super().__init__()
		self.animationSpeed = 20 #动画速度
		self.layout = "top" #布局方式
		self.tabPages = [] #子页
		self.underLineColor = "none" #下划线的颜色
		self.underLineSize = 0 #下划线的宽度
		self.underPoint = None #下划点
		self.useAnimation = False #是否使用动画
		self.viewType = "tabview" #类型
	pass

#横竖布局层
class FCLayoutDiv(FCView):
	def __init__(self):
		super().__init__()
		self.autoWrap = False #是否自动换行
		self.layoutStyle = "lefttoright" #分割方式
		self.viewType = "layout" #类型
	pass

#分割布局层
class FCSplitLayoutDiv(FCView):
	def __init__(self):
		super().__init__()
		self.firstView = None #第一个视图
		self.layoutStyle = "lefttoright" #分割方式
		self.oldSize = FCSize(0,0) #上次的尺寸
		self.secondView = None #第二个视图
		self.splitMode = "absolutesize" #分割模式 percentsize百分比 或absolutesize绝对值
		self.splitPercent = -1 #分割百分比
		self.splitter = None #分割线 
		self.viewType = "split" #类型
	pass

#表格列
class FCGridColumn(object):	
	def __init__(self):
		self.allowSort = True #是否允许排序
		self.allowResize = False #是否允许改变大小
		self.backColor = "rgb(200,200,200)" #背景色
		self.borderColor = "rgb(150,150,150)" #边线颜色
		self.bounds = FCRect(0,0,0,0) #区域
		self.cellAlign = "left" #left:居左 center:居中 right:居右
		self.colName = "" #名称
		self.colType = "" #类型 string:字符串 double:浮点型 int:整型 bool:布尔型
		self.font = "Default,14" #字体
		self.frozen = False #是否冻结
		self.index = -1 #索引
		self.sort = "none" #排序模式
		self.text = "" #文字
		self.textColor = "rgb(50,50,50)" #文字颜色
		self.visible = True #是否可见
		self.width = 120 #宽度
		self.widthStr = "" #宽度字符串

#单元格
class FCGridCell(object):	
	def __init__(self):
		self.backColor = "none" #背景色
		self.borderColor = "none" #边线颜色
		self.colSpan = 1 #列距
		self.column = None #所在列
		self.digit = -1 #保留小数的位数
		self.font = "Default,14" #字体
		self.rowSpan = 1 #行距
		self.textColor = "rgb(0,0,0)" #文字颜色
		self.value = None #值
		self.view = None #包含的视图

#表格行
class FCGridRow(object):	
	def __init__(self):
		self.cells = [] #单元格
		self.index = -1 #索引
		self.key = "" #排序键值
		self.selected = False #是否选中
		self.visible = True #是否可见

#表格
class FCGrid(FCView):
	def __init__(self):
		super().__init__()
		self.columns = [] #列
		self.headerHeight = 30 #头部高度
		self.rowHeight = 30 #行高
		self.rows = [] #行
		self.selectedRowColor = "rgb(125,125,125)" #选中行的颜色
		self.showHScrollBar = True #是否显示横向滚动条
		self.showVScrollBar = True #是否显示横向滚动条
		self.viewType = "grid" #类型
		self.onClickGridCell = None #点击单元格的回调
		self.onClickGridColumn = None #点击列的回调
		self.onPaintGridCell = None #绘制单元格的回调
		self.onPaintGridColumn = None #绘制表格列的回调
	pass

#表格列
class FCTreeColumn(object):
	def __init__(self):
		self.bounds = FCRect(0,0,0,0) #区域
		self.index = -1 #索引
		self.visible = True #是否可见
		self.width = 120 #宽度
		self.widthStr = "" #宽度字符串

#表格行
class FCTreeRow(object):	
	def __init__(self):
		self.cells = [] #单元格
		self.index = -1 #索引
		self.selected = False #是否选中
		self.visible = True #是否可见

#单元格
class FCTreeNode(object):
	def __init__(self):
		self.allowCollapsed = True #是否允许折叠
		self.backColor = "none" #背景色
		self.checked = False #是否选中
		self.childNodes = [] #子节点
		self.collapsed = False #是否折叠
		self.column = None #所在列
		self.font = "Default,14" #字体
		self.indent = 0 #缩进
		self.parentNode = None #父节点
		self.row = None #所在行
		self.value = None #值
		self.textColor = "rgb(0,0,0)" #文字颜色	

#树
class FCTree(FCView):
	def __init__(self):
		super().__init__()
		self.checkBoxWidth = 25 #复选框占用的宽度
		self.childNodes = [] #子节点
		self.collapsedWidth = 25 #折叠按钮占用的宽度
		self.columns = [] #列
		self.headerHeight = 0 #头部高度
		self.indent = 20 #缩进
		self.rowHeight = 30 #行高
		self.rows = [] #行
		self.showCheckBox = False #是否显示复选框
		self.showHScrollBar = True #是否显示横向滚动条
		self.showVScrollBar = True #是否显示横向滚动条
		self.viewType = "tree" #类型
		self.onClickTreeNode = None #点击树节点的回调
		self.onPaintTreeNode = None #绘制树节点的回调
	pass

#证券数据结构
class SecurityData(object):
	def __init__(self):
		self.amount = 0 #成交额
		self.close = 0 #收盘价
		self.date = 0 #日期，为1970年到现在的秒
		self.high = 0 #最高价
		self.low = 0 #最低价
		self.open = 0 #开盘价
		self.volume = 0 #成交额
	#拷贝数值
	def copy(self, securityData):
		self.amount = securityData.amount
		self.close = securityData.close
		self.date = securityData.date
		self.high = securityData.high
		self.low = securityData.low
		self.open = securityData.open
		self.volume = securityData.volume

#基础图形
class BaseShape(object):
	def __init__(self):
		self.color = "none" #颜色
		self.color2 = "none" #颜色2
		self.datas = [] #第一组数据
		self.datas2 = [] #第二组数据
		self.divIndex = 0 #所在层
		self.leftOrRight = True #依附于左轴或右轴
		self.lineWidth = 1 #线的宽度
		self.shapeName = "" #名称
		self.shapeType = "line" #类型
		self.showHideDatas = [] #控制显示隐藏的数据
		self.style = "" #样式
		self.text = "" #显示的文字
		self.title = "" #第一个标题
		self.title2 = "" #第二个标题
		self.value = 0 #显示文字的值

#画线工具结构
class FCPlot(object):
	def __init__(self):
		self.key1 = None #第一个键
		self.key2 = None #第二个键
		self.key3 = None #第三个键
		self.plotType = "Line" #线的类型
		self.pointColor = "rgba(0,0,0,125)" #线的颜色
		self.lineColor = "rgb(0,0,0)" #线的颜色
		self.lineWidth = 1 #线的宽度
		self.startKey1 = None #移动前第一个键
		self.startValue1 = None #移动前第一个值
		self.startKey2 = None #移动前第二个键
		self.startValue2 = None #移动前第二个值
		self.startKey3 = None #移动前第三个键
		self.startValue3 = None #移动前第三个值
		self.value1 = None #第一个值
		self.value2 = None #第二个值
		self.value3 = None #第三个值

#图表
class FCChart(FCView):
	def __init__(self):
		super().__init__()
		self.addingPlot = "" #要添加的画线
		self.allowDragScroll = True #是否允许拖动滚动
		self.autoFillHScale = False #是否填充满X轴
		self.allowDragChartDiv = False #是否允许拖拽图层
		self.candleDistance = 0 #蜡烛线的距离
		self.candleMax = 0 #蜡烛线的最大值
		self.candleMin = 0 #蜡烛线的最小值
		self.candleMaxRight = 0 #蜡烛线的右轴最大值
		self.candleMinRight = 0 #蜡烛线的右轴最小值
		self.crossTipColor = "rgb(50,50,50)" #十字线标识的颜色
		self.crossLineColor = "rgb(100,100,100)" #十字线的颜色
		self.candleDivPercent = 0.5 #图表层的占比
		self.candleDigit = 2 #图表层保留小数的位数
		self.candlePaddingTop = 30 #图表层的上边距
		self.candlePaddingBottom = 30 #图表层的下边距
		self.crossStopIndex = -1 #鼠标停留位置
		self.cycle = "second" #周期
		self.data = [] #图表数据
		self.downColor = "rgb(15,193,118)" #下跌颜色
		self.firstVisibleIndex = -1 #起始可见的索引
		self.font = "Default,14" #字体
		self.gridColor = "rgb(50,0,0)" #网格颜色 
		self.hScalePixel = 11 #蜡烛线的宽度
		self.hScaleHeight = 30 #X轴的高度
		self.hScaleFormat = "" #X轴的格式化字符，例如%Y-%m-%d %H:%M:%S
		self.hScaleTextDistance = 10 #X轴的文字间隔
		self.indMax = 0 #指标层的最大值
		self.indMin = 0 #指标层的最小值
		self.indMax2 = 0 #指标层2的最大值
		self.indMin2 = 0 #指标层2的最小值
		self.indMaxRight = 0 #指标层的右轴最大值
		self.indMinRight = 0 #指标层的右轴最小值
		self.indMax2Right = 0 #指标层2的右轴最大值
		self.indMin2Right = 0 #指标层2的右轴最小值
		self.indDigit = 2 #指标层保留小数的位数
		self.indDigit2 = 2 #指标层2保留小数的位数
		self.indDivPercent = 0.3 #指标层的占比
		self.indDivPercent2 = 0.0 #指标层2的占比
		self.indPaddingTop = 20 #指标层的上边距
		self.indPaddingBottom = 20 #指标层的下边距
		self.indPaddingTop2 = 20 #指标层2的上边距
		self.indPaddingBottom2 = 20 #指标层2的下边距
		self.indicatorColors = [] #指标的颜色
		self.leftVScaleWidth = 0 #左轴宽度
		self.lastVisibleIndex = -1 #结束可见的索引
		self.lastRecordIsVisible = True #最后记录是否可见
		self.lastVisibleKey = 0 #最后可见的主键
		self.lastValidIndex = -1 #最后有效数据索引
		self.lineWidthChart = 1
		self.mainIndicator = "" #主图指标
		self.magnitude = 1 #成交量的比例
		self.midColor = "none" #中间色
		self.offsetX = 0 #横向绘图偏移
		self.plots = [] #画线的集合
		self.plotPointSizeChart = 5 #画线的选中点大小
		self.rightVScaleWidth = 100 #右轴宽度
		self.rightSpace = 0 #右侧空间
		self.shapes = [] #扩展图形
		self.scaleColor = "rgb(100,0,0)" #刻度的颜色
		self.showIndicator = "" #显示指标
		self.showCrossLine = False #是否显示十字线
		self.selectPlotPoint = -1 #选中画线的点
		self.sPlot = None #选中的画线
		self.startMovePlot = False #选中画线
		self.selectShape = "" #选中的图形
		self.selectShapeEx = "" #选中的图形信息
		self.targetOldX = 0 #缩小时旧的位置1
		self.targetOldX2 = 0 #放大时旧的位置2
		self.touchPosition = FCPoint(0,0) #鼠标坐标
		self.touchDownPointChart = FCPoint(0, 0)
		self.volMax = 0 #成交量层的最大值
		self.volMin = 0 #成交量层的最小值
		self.volMaxRight = 0 #成交量层的右轴最大值
		self.volMinRight = 0 #成交量层的右轴最小值
		self.volDigit = 0 #成交量层保留小数的位数
		self.volDivPercent = 0.2 #成交量层的占比
		self.volPaddingTop = 20 #成交量层的上边距
		self.volPaddingBottom = 0 #成交量层的下边距
		self.vScaleDistance = 35 #纵轴的间隔
		self.vScaleType = "standard" #纵轴的类型 math.log10代表指数坐标
		self.viewType = "chart" #类型
		self.upColor = "rgb(219,68,83)" #上涨颜色
		self.candleStyle = "rect"
		self.barStyle = "rect"
		self.firstOpen = 0
		self.closearr = []
		self.allema12 = []
		self.allema26 = []
		self.alldifarr = []
		self.alldeaarr = []
		self.allmacdarr = []
		self.boll_up = []
		self.boll_down = []
		self.boll_mid = []
		self.bias1 = []
		self.bias2 = []
		self.bias3 = []
		self.kdj_k = []
		self.kdj_d = []
		self.kdj_j = []
		self.rsi1 = []
		self.rsi2 = []
		self.rsi3 = []
		self.roc = []
		self.roc_ma = []
		self.wr1 = []
		self.wr2 = []
		self.cci = []
		self.bbi = []
		self.trix = []
		self.trix_ma = []
		self.dma1 = []
		self.dma2 = []
		self.ma5 = []
		self.ma10 = []
		self.ma20 = []
		self.ma30 = []
		self.ma120 = []
		self.ma250 = []
		self.gridStep = 0 #网格计算临时变量
		self.gridDigit = 0 #网格计算临时变量
		self.firstIndexCache = -1
		self.firstTouchIndexCache = -1
		self.firstTouchPointCache = FCPoint(0,0)
		self.lastIndexCache = -1
		self.secondTouchIndexCache = -1
		self.secondTouchPointCache = FCPoint(0,0)
		self.firstPaddingTop = 0
		self.firstPaddingBottom = 0
		self.kChart = 0
		self.bChart = 0
		self.oXChart = 0
		self.oYChart = 0
		self.rChart = 0
		self.x4Chart = 0
		self.y4Chart = 0
		self.nHighChart = 0
		self.nLowChart = 0
		self.xChart = 0
		self.yChart = 0
		self.wChart = 0
		self.hChart = 0
		self.upSubValue = 0
		self.downSubValue = 0
		self.nMaxHigh = 0;
		self.nMaxLow = 0;
		self.indicatorColors.append("rgb(100,100,100)")
		self.indicatorColors.append("rgb(206,147,27)")
		self.indicatorColors.append("rgb(150,0,150)")
		self.indicatorColors.append("rgb(255,0,0)")
		self.indicatorColors.append("rgb(0,150,150)")
		self.indicatorColors.append("rgb(0,150,0)")
		self.indicatorColors.append("rgb(59,174,218)")
		self.indicatorColors.append("rgb(50,50,50)")
		self.onCalculateChartMaxMin = None #计算最大最小值的回调
		self.onPaintChartScale = None #绘制坐标轴回调
		self.onPaintChartHScale = None #绘制坐标轴回调
		self.onPaintChartStock = None #绘制图表回调
		self.onPaintChartPlot = None #绘制画线回调
		self.onPaintChartCrossLine = None #绘制十字线回调
	pass

#日期按钮
class DayButton(object):
	def __init__(self):
		self.backColor = "none" #背景颜色
		self.borderColor = "rgb(150,150,150)" #文字颜色 
		self.bounds = FCRect(0,0,0,0) #显示区域
		self.calendar = None #日历视图
		self.day = None #日
		self.font = "Default,16" #字体
		self.inThisMonth = False #是否在本月
		self.selected = False #是否被选中
		self.textColor = "rgb(0,0,0)" #文字颜色
		self.textColor2 = "rgb(50,50,50)" #第二个文字颜色
		self.visible = True #是否可见

#月的按钮
class MonthButton(object):
	def __init__(self):
		self.backColor = "none" #背景颜色
		self.borderColor = "rgb(150,150,150)" #文字颜色 
		self.bounds = FCRect(0,0,0,0) #显示区域
		self.calendar = None #日历视图
		self.font = "Default,16" #字体
		self.month = 0 #月
		self.textColor = "rgb(0,0,0)" #文字颜色
		self.visible = True #是否可见
		self.year = 0 #年

#年的按钮
class YearButton(object):
	def __init__(self):
		self.backColor = "none" #背景颜色
		self.borderColor = "rgb(150,150,150)" #文字颜色 
		self.bounds = FCRect(0,0,0,0) #显示区域
		self.calendar = None #日历视图
		self.font = "Default,16" #字体
		self.textColor = "rgb(0,0,0)" #文字颜色
		self.visible = True #是否可见
		self.year = 0 #年

#日期层
class DayDiv(object):
	def __init__(self):
		self.aClickRowFrom = 0 #点击时的上月的行
		self.aClickRowTo = 0 #点击时的当月的行
		self.aDirection = 0 #动画的方向
		self.aTick = 0 #动画当前帧数
		self.aTotalTick = 40 #动画总帧数
		self.calendar = None #日历视图
		self.dayButtons = [] #日期的集合
		self.dayButtons_am = []  #动画日期的集合

#月层
class MonthDiv(object):
	def __init__(self):
		self.aDirection = 0 #动画的方向
		self.aTick = 0 #动画当前帧数
		self.aTotalTick = 40 #动画总帧数
		self.calendar = None #日历视图
		self.month = 0 #月份
		self.monthButtons = [] #月的按钮
		self.monthButtons_am = [] #月的动画按钮
		self.year = 0 #年份

#年层
class YearDiv(object):
	def __init__(self):
		self.aDirection = 0 #动画的方向
		self.aTick = 0 #动画当前帧数
		self.aTotalTick = 40 #动画总帧数
		self.calendar = None #日历视图
		self.startYear = 0 #开始年份
		self.yearButtons = [] #月的按钮
		self.yearButtons_am = [] #月的动画按钮

#头部层
class HeadDiv(object):
	def __init__(self):
		self.arrowColor = "rgb(150,150,150)" #箭头颜色
		self.backColor = "rgb(255,255,255)" #箭头颜色
		self.calendar = None #日历视图
		self.bounds = FCRect(0,0,0,0) #显示区域
		self.textColor = "rgb(0,0,0)" #文字颜色
		self.titleFont = "Default,20" #标题字体
		self.weekFont = "Default,14" #星期字体

#时间层
class TimeDiv(object):
	def __init__(self):
		self.bounds = FCRect(0,0,0,0) #显示区域
		self.calendar = None #日历视图
		
#年的结构
class CYear(object):
	def __init__(self):
		self.months = dict() #月的集合
		self.year = 0 #年

#月的结构
class CMonth(object):
	def __init__(self):
		self.days = dict() #日的集合
		self.month = 0 #月
		self.year = 0 #年

#日的结构
class CDay(object):
	def __init__(self):
		self.day = 0 #日
		self.month = 0 #月
		self.year = 0 #年

#多页夹
class FCCalendar(FCView):
	def __init__(self):
		super().__init__()
		self.dayDiv = DayDiv() #日层
		self.headDiv = HeadDiv() #头部层
		self.mode = "day" #模式
		self.monthDiv = MonthDiv() #月层
		self.selectedDay = None #选中日
		self.timeDiv = TimeDiv() #时间层
		self.useAnimation = False #是否使用动画
		self.viewType = "calendar" #类型
		self.yearDiv = YearDiv() #年层
		self.years = dict() #日历
		self.onPaintCalendarDayButton = None  #绘制日历的日按钮回调
		self.onPaintCalendarMonthButton = None #绘制日历的月按钮回调
		self.onPaintCalendarYearButton = None #绘制日历的年按钮回调
		self.onPaintCalendarHeadDiv = None #绘制日历头部回调

#饼图
class FCPie(FCView):
	def __init__(self):
		super().__init__()
		self.items = [] #数据项
		self.pieRadius = 70 #饼图半径
		self.startAngle = 0 #开始角度
		self.textRadius = 80 #是否可见
		self.viewType = "pie" #类型
	pass

#饼图项
class FCPieItem(object):
	def __init__(self):
		self.color = "rgb(0,0,0)" #颜色
		self.text = "" #文字
		self.value = 0 #数值

#菜单
class FCMenu(FCLayoutDiv):
	def __init__(self):
		super().__init__()
		self.autoSize = True #是否自动适应尺寸
		self.autoWrap = False
		self.comboBox = None #所在的下拉菜单
		self.items = [] #菜单项
		self.layoutStyle = "toptobottom"
		self.maximumSize = FCSize(100,300) #最大大小
		self.popup = True #是否弹出
		self.showHScrollBar = True
		self.showVScrollBar = True 
		self.size = FCSize(100, 100)
		self.viewType = "menu"
		self.visible = False
	pass

#菜单项
class FCMenuItem(FCView):
	def __init__(self):
		super().__init__()
		self.checked = False #是否选中
		self.dropDownMenu = None #下拉菜单
		self.hoveredColor = "rgb(150,150,150)"
		self.items = [] #菜单项
		self.parentMenu = None #所在菜单
		self.parentItem = None #父菜单项
		self.pushedColor = "rgb(200,200,200)"
		self.size = FCSize(100, 25)
		self.value = "" #值
		self.viewType = "menuitem"
	pass

#下拉选择
class FCComboBox(FCView):
	def __init__(self):
		super().__init__()
		self.dropDownMenu = None #下拉菜单 
		self.selectedIndex = -1 #选中索引
		self.viewType = "combobox"
	pass

#添加顶层视图
#view 视图
#paint 绘图对象
def addView(view, paint):
	view.paint = paint
	paint.views.append(view)
	if view.viewType == "textbox":
		if len(view.viewName) > 0:
			view.exView = True
			paint.init()
			paint.gdiPlusPaint.createView(view.viewType, view.viewName)
			
#添加到父视图
#view 视图
#parent 父视图
def addViewToParent(view, parent):
	view.parent = parent
	view.paint = parent.paint
	parent.views.append(view)
	paint = view.paint
	if view.viewType == "textbox":
		if len(view.viewName) > 0:
			view.exView = True
			paint.init()
			paint.gdiPlusPaint.createView(view.viewType, view.viewName)

#隐藏视图
#mp 坐标
#paint 绘图对象
def autoHideView(mp, paint):
	hideView = False
	for i in range(0, len(paint.views)):
		view = paint.views[i]
		if view.autoHide:
			size = view.size
			location = view.location
			if mp.x < location.x or mp.x > location.x + size.cx or mp.y < location.y or mp.y > location.y + size.cy:
				if view.visible:
					view.visible = False
					hideView = True
	if hideView:
		invalidate(paint)

#清除输入框
#views:视图集合
def clearViewInputs(views):
	for i in range(0, len(views)):
		view = views[i]
		if view.exView:
			if len(view.viewName) > 0:
				view.exView = False
				view.paint.gdiPlusPaint.removeView(view.viewName)
		clearViewInputs(view.views)

#清除全部的视图
def clearViews(paint):
	clearViewInputs(paint.views)
	paint.views = []

#移除顶层视图
#view 视图
#paint 绘图对象
def removeView(view, paint):
	for i in range(0, len(paint.views)):
		if paint.views[i] == view:
			paint.views.remove(view)
			if view.exView:
				removeViews = []
				removeViews.append(view)
				clearViewInputs(removeViews)
			break

#从父视图中移除
#view 视图
#parent 父视图
def removeViewFromParent(view, parent):
	for i in range(0, len(parent.views)):
		if parent.views[i] == view:
			parent.views.remove(view)
			if view.exView:
				removeViews = []
				removeViews.append(view)
				clearViewInputs(removeViews)
			break

#获取绝对位置X 
#view:视图
def clientX(view):
	if view != None:
		cLeft = view.location.x
		if view.parent != None:
			if view.parent.displayOffset:
				return cLeft + clientX(view.parent) - view.parent.scrollH
			else:
				return cLeft + clientX(view.parent)
		else:
			return cLeft
	else:
		return 0

#获取绝对位置Y 
#view:视图
def clientY(view):
	if view != None:
		cTop = view.location.y
		if view.parent != None:
			if view.parent.displayOffset:
				return cTop + clientY(view.parent) - view.parent.scrollV
			else:
				return cTop + clientY(view.parent)
		else:
			return cTop
	else:
		return 0

#是否重绘时可见 
#view:视图
def isPaintVisible(view):
    if view.visible:
        if view.parent != None:
            if view.parent.visible:
                return isPaintVisible(view.parent)
            else:
                return False
        else:
            return True
    else:
        return False

#是否可用 
#view:视图
def isViewEnabled(view):
	if view.enabled:
		if view.parent != None:
			if view.parent.enabled:
				return isViewEnabled(view.parent)
			else:
				return False
		else:
			return True
	else:
		return False

#是否包含坐标 
#view:视图 
#mp:坐标
def containsPoint(view, mp):
	if isViewEnabled(view):
		clx = clientX(view)
		cly = clientY(view)
		size = view.size
		cp = FCPoint(0,0)
		cp.x = mp.x - clx
		cp.y = mp.y - cly
		if cp.x >= 0 and cp.x <= size.cx and cp.y >= 0 and cp.y <= size.cy:
			return True
		else:
			return False
	else:
		return False

#根据名称查找视图 
#name:名称
#views:视图集合
def findViewByName(name, views):
	size = len(views)
	for view in views:
		if view.viewName == name:
			return view
		else:
			subViews = view.views
			if len(subViews) > 0:
				subView = findViewByName(name, subViews)
				if subView != None:
					return subView
	return None

#获取区域的交集
def getIntersectRect(lpDestRect, lpSrc1Rect, lpSrc2Rect):
	lpDestRect.left = max(lpSrc1Rect.left, lpSrc2Rect.left)
	lpDestRect.right = min(lpSrc1Rect.right, lpSrc2Rect.right)
	lpDestRect.top = max(lpSrc1Rect.top, lpSrc2Rect.top)
	lpDestRect.bottom = min(lpSrc1Rect.bottom, lpSrc2Rect.bottom)
	if lpDestRect.right > lpDestRect.left and lpDestRect.bottom > lpDestRect.top:
		return 1
	else:
		lpDestRect.left = 0
		lpDestRect.right = 0
		lpDestRect.top = 0
		lpDestRect.bottom = 0
		return 0

#根据坐标查找视图 
#mp:坐标 
#views:视图集合
def findView(mp, views):
	size = len(views)
	#先判断置顶视图
	for i in range(0, size):
		view = views[size - i - 1]
		if view.visible and view.topMost:
			hasPoint = False
			if view.paint.onContainsPoint != None:
				hasPoint = view.paint.onContainsPoint(view, mp)
			else:
				hasPoint = containsPoint(view, mp)
			if hasPoint:
				if view.vScrollIsVisible and view.scrollSize > 0:
					clx = clientX(view)
					if mp.x >= clx + view.size.cx - view.scrollSize:
						return view
				if view.hScrollIsVisible and view.scrollSize > 0:
					cly = clientY(view)
					if mp.y >= cly + view.size.cy - view.scrollSize:
						return view
				subViews = view.views
				if len(subViews) > 0:
					subView = findView(mp, subViews)
					if subView != None:
						return subView
				return view
	#再判断非置顶视图
	for i in range(0, size):
		view = views[size - i - 1]
		if view.visible and view.topMost == False:
			hasPoint = False
			if view.paint.onContainsPoint != None:
				hasPoint = view.paint.onContainsPoint(view, mp)
			else:
				hasPoint = containsPoint(view, mp)
			if hasPoint:
				if view.vScrollIsVisible and view.scrollSize > 0:
					clx = clientX(view)
					if mp.x >= clx + view.size.cx - view.scrollSize:
						return view
				if view.hScrollIsVisible and view.scrollSize > 0:
					cly = clientY(view)
					if mp.y >= cly + view.size.cy - view.scrollSize:
						return view
				subViews = view.views
				if len(subViews) > 0:
					subView = findView(mp, subViews)
					if subView != None:
						return subView
				return view
	return None

#跨线程调用
def beginInvoke(view, args):
	paint = view.paint
	seraialID = 0
	paint.lock.acquire()
	paint.invokeSerialID = paint.invokeSerialID + 1
	seraialID = paint.invokeSerialID
	paint.invokeArgs[seraialID] = args
	paint.invokeViews[seraialID] = view
	paint.lock.release()
	user32.PostMessageW(paint.hWnd, paint.pInvokeMsgID, seraialID, 0)

#重绘复选按钮 
#checkBox:视图 
#paint:绘图对象 
#clipRect:裁剪区域
def drawCheckBox(checkBox, paint, clipRect):
	width = checkBox.size.cx
	height = checkBox.size.cy
	if checkBox.textColor != "none":
		eRight = checkBox.buttonSize.cx + 10
		eRect = FCRect(1, (height - checkBox.buttonSize.cy) / 2, checkBox.buttonSize.cx + 1, (height + checkBox.buttonSize.cy) / 2)
		paint.drawRect(checkBox.textColor, 1, 0, eRect.left, eRect.top, eRect.right, eRect.bottom)
		#绘制选中区域
		if checkBox.checked:
			eRect.left += 2
			eRect.top += 2
			eRect.right -= 2
			eRect.bottom -= 2
			drawPoints = []
			drawPoints.append(FCPoint(eRect.left, eRect.top + 8))
			drawPoints.append(FCPoint(eRect.left + 6, eRect.bottom))
			drawPoints.append(FCPoint(eRect.right - 1, eRect.top))
			paint.drawPolyline(checkBox.textColor, 1, 0, drawPoints)
		tSize = paint.textSize(checkBox.text, checkBox.font)
		paint.drawText(checkBox.text, checkBox.textColor, checkBox.font, eRight, (height - tSize.cy) / 2)		

#重绘单选按钮 
#checkBox:视图 
#paint:绘图对象 
#clipRect:裁剪区域
def drawRadioButton(radioButton, paint, clipRect):
	width = radioButton.size.cx
	height = radioButton.size.cy
	if radioButton.textColor != "none":
		eRight = radioButton.buttonSize.cx + 10
		eRect = FCRect(1, (height - radioButton.buttonSize.cy) / 2, radioButton.buttonSize.cx + 1, (height + radioButton.buttonSize.cy) / 2)
		paint.drawEllipse(radioButton.textColor, 1, 0, eRect.left, eRect.top, eRect.right, eRect.bottom)
		#绘制选中区域
		if radioButton.checked:
			eRect.left += 2
			eRect.top += 2
			eRect.right -= 2
			eRect.bottom -= 2
			paint.fillEllipse(radioButton.textColor, eRect.left, eRect.top, eRect.right, eRect.bottom)
		tSize = paint.textSize(radioButton.text, radioButton.font)
		paint.drawText(radioButton.text, radioButton.textColor, radioButton.font, eRight, (height - tSize.cy) / 2)		

#点击复选按钮 
#checkBox:视图
#mp: 坐标
def clickCheckBox(checkBox, mp):
	if checkBox.checked:
		checkBox.checked = False
	else:
		checkBox.checked = True

#点击单选按钮 
#radioButton:视图
#mp: 坐标
def clickRadioButton(radioButton, mp):
	hasOther = False
	if radioButton.parent != None and len(radioButton.parent.views) > 0:
		#将相同groupName的单选按钮都取消选中
		for i in range(0, len(radioButton.parent.views)):
			rView = radioButton.parent.views[i]
			if rView.viewType == "radiobutton":
				if rView != radioButton and rView.groupName == radioButton.groupName:
					rView.checked = False
	radioButton.checked = True

#重绘按钮 
#button:视图 
#paint:绘图对象 
#clipRect:裁剪区域
def drawButton(button, paint, clipRect):
	#鼠标按下
	if button == paint.touchDownView:
		if button.pushedColor != "none":
			paint.fillRoundRect(button.pushedColor, 0, 0, button.size.cx, button.size.cy, button.cornerRadius)
		else:
			if button.backColor != "none":
				paint.fillRoundRect(button.backColor, 0, 0, button.size.cx, button.size.cy, button.cornerRadius)
	#鼠标悬停
	elif button == paint.touchMoveView:
		if button.hoveredColor != "none":
			paint.fillRoundRect(button.hoveredColor, 0, 0, button.size.cx, button.size.cy, button.cornerRadius)
		else:
			if button.backColor != "none":
				paint.fillRoundRect(button.backColor, 0, 0, button.size.cx, button.size.cy, button.cornerRadius)
	#常规情况
	elif button.backColor != "none":
		paint.fillRoundRect(button.backColor, 0, 0, button.size.cx, button.size.cy, button.cornerRadius)
	#绘制文字
	if button.textColor != "none" and len(button.text) > 0:
		tSize = paint.textSize(button.text, button.font)
		paint.drawText(button.text, button.textColor, button.font, (button.size.cx - tSize.cx) / 2, (button.size.cy  - tSize.cy) / 2)
	#绘制边线
	if button.borderColor != "none":
		paint.drawRoundRect(button.borderColor, button.borderWidth, 0, 0, 0, button.size.cx, button.size.cy, button.cornerRadius)

#获取内容的宽度 
#div:图层
def getDivContentWidth(div):
	cWidth = 0
	subViews = div.views
	for view in subViews:
		if view.visible:
			if cWidth < view.location.x + view.size.cx:
				cWidth = view.location.x + view.size.cx
	return cWidth

#获取内容的高度 
#div:图层
def getDivContentHeight(div):
	cHeight = 0
	subViews = div.views
	for view in subViews:
		if view.visible:
			if cHeight < view.location.y + view.size.cy:
				cHeight = view.location.y + view.size.cy
	return cHeight

#绘制滚动条 
#div:图层 
#paint:绘图对象 
#clipRect:裁剪区域
def drawDivScrollBar(div, paint, clipRect):
	div.hScrollIsVisible = False
	div.vScrollIsVisible = False
	#判断横向滚动条
	if div.showHScrollBar:
		contentWidth = getDivContentWidth(div)
		if contentWidth > 0 and contentWidth > div.size.cx:
			sLeft = div.scrollH / contentWidth * div.size.cx
			sRight = (div.scrollH + div.size.cx) / contentWidth * div.size.cx
			if sRight - sLeft < div.scrollSize:
				sRight = sLeft + div.scrollSize
			if paint.touchMoveView == div and (div.hoverScrollHButton or div.downScrollHButton):
				paint.fillRect(div.scrollBarHoveredColor, sLeft, div.size.cy - div.scrollSize, sRight, div.size.cy)
			else:
				paint.fillRect(div.scrollBarColor, sLeft, div.size.cy - div.scrollSize, sRight, div.size.cy)
			div.hScrollIsVisible = True
	#判断纵向滚动条
	if div.showVScrollBar:
		contentHeight = getDivContentHeight(div)	
		if contentHeight > 0 and contentHeight > div.size.cy:
			sTop = div.scrollV / contentHeight * div.size.cy
			sBottom = sTop + (div.size.cy / contentHeight * div.size.cy)
			if sBottom - sTop < div.scrollSize:
				sBottom = sTop + div.scrollSize
			if paint.touchMoveView == div and (div.hoverScrollVButton or div.downScrollVButton):
				paint.fillRect(div.scrollBarHoveredColor, div.size.cx - div.scrollSize, sTop, div.size.cx, sBottom)
			else:
				paint.fillRect(div.scrollBarColor, div.size.cx - div.scrollSize, sTop, div.size.cx, sBottom)
			div.vScrollIsVisible = True

#重绘图层边线 
#div:视图 
#paint:绘图对象 
#clipRect:裁剪区域
def drawDivBorder(div, paint, clipRect):
	if div.borderColor != "none":
		paint.drawRoundRect(div.borderColor, div.borderWidth, 0, 0, 0, div.size.cx, div.size.cy, div.cornerRadius)

#重绘图形 
#div:视图 
#paint:绘图对象 
#clipRect:裁剪区域
def drawDiv(div, paint, clipRect):
	if div.backColor != "none":
		paint.fillRoundRect(div.backColor, 0, 0, div.size.cx, div.size.cy, div.cornerRadius)

#图层的鼠标滚轮方法 
#div:图层 
#delta:滚轮值
def touchWheelDiv(div, delta):
	oldScrollV = div.scrollV
	if delta > 0:
		oldScrollV -= 10
	elif delta < 0:
		oldScrollV += 10
	contentHeight = getDivContentHeight(div)
	if contentHeight < div.size.cy:
		div.scrollV = 0
	else:
		if oldScrollV < 0:
			oldScrollV = 0
		elif oldScrollV > contentHeight - div.size.cy:
			oldScrollV = contentHeight - div.size.cy
		div.scrollV = oldScrollV


#图层的鼠标抬起方法 
#div: 图层 
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks 点击次数
def touchUpDiv(div, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	div.downScrollHButton = False
	div.downScrollVButton = False
	div.hoverScrollHButton = False
	div.hoverScrollVButton = False

#图层的鼠标按下方法 
#div: 图层 
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks 点击次数
def touchDownDiv(div, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	mp = firstPoint
	div.startPoint = mp
	div.downScrollHButton = False
	div.downScrollVButton = False
	div.hoverScrollHButton = False
	div.hoverScrollVButton = False
	#判断横向滚动条
	if div.showHScrollBar:
		contentWidth = getDivContentWidth(div)
		if contentWidth > 0 and contentWidth > div.size.cx:
			sLeft = div.scrollH / contentWidth * div.size.cx
			sRight = (div.scrollH + div.size.cx) / contentWidth * div.size.cx
			if sRight - sLeft < div.scrollSize:
				sRight = sLeft + div.scrollSize
			if mp.x >= sLeft and mp.x <= sRight and mp.y >= div.size.cy - div.scrollSize and mp.y <= div.size.cy:
				div.downScrollHButton = True
				div.startScrollH = div.scrollH
				return
	#判断纵向滚动条
	if div.showVScrollBar:
		contentHeight = getDivContentHeight(div)
		if contentHeight > 0 and contentHeight > div.size.cy:
			sTop = div.scrollV / contentHeight * div.size.cy
			sBottom = (div.scrollV + div.size.cy) / contentHeight * div.size.cy
			if sBottom - sTop < div.scrollSize:
				sBottom = sTop + div.scrollSize
			if mp.x >= div.size.cx - div.scrollSize and mp.x <= div.size.cx and mp.y >= sTop and mp.y <= sBottom:
				div.downScrollVButton = True
				div.startScrollV = div.scrollV
				return
	if div.allowDragScroll:
		div.startScrollH = div.scrollH
		div.startScrollV = div.scrollV

#图层的鼠标移动方法 
#div: 图层 
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
def touchMoveDiv(div, firstTouch, firstPoint, secondTouch, secondPoint):
	div.hoverScrollHButton = False
	div.hoverScrollVButton = False
	mp = firstPoint
	if firstTouch:
		if div.showHScrollBar or div.showVScrollBar:
			#判断横向滚动条
			if div.downScrollHButton:
				contentWidth = getDivContentWidth(div)
				subX = (mp.x - div.startPoint.x) / div.size.cx * contentWidth
				newScrollH = div.startScrollH + subX
				if newScrollH < 0:
					newScrollH = 0
				elif newScrollH > contentWidth - div.size.cx:
					newScrollH = contentWidth - div.size.cx
				div.scrollH = newScrollH
				div.paint.cancelClick = True
				return
			#判断纵向滚动条
			elif div.downScrollVButton:
				contentHeight = getDivContentHeight(div)
				subY = (mp.y - div.startPoint.y) / div.size.cy * contentHeight
				newScrollV = div.startScrollV + subY
				if newScrollV < 0:
					newScrollV = 0
				elif newScrollV > contentHeight - div.size.cy:
					newScrollV = contentHeight - div.size.cy
				div.scrollV = newScrollV
				div.paint.cancelClick = True
				return
		#判断拖动
		if div.allowDragScroll:
			contentWidth = getDivContentWidth(div)
			if contentWidth > div.size.cx:
				subX = div.startPoint.x - mp.x
				newScrollH = div.startScrollH + subX
				if newScrollH < 0:
					newScrollH = 0
				elif newScrollH > contentWidth - div.size.cx:
					newScrollH = contentWidth - div.size.cx
				div.scrollH = newScrollH
				if abs(subX) > 5:
					div.paint.cancelClick = True
			contentHeight = getDivContentHeight(div)
			if contentHeight > div.size.cy:
				subY = div.startPoint.y - mp.y
				newScrollV = div.startScrollV + subY
				if newScrollV < 0:
					newScrollV = 0
				elif newScrollV > contentHeight - div.size.cy:
					newScrollV = contentHeight - div.size.cy
				div.scrollV = newScrollV
				if abs(subY) > 5:
					div.paint.cancelClick = True
	else:
		#判断横向滚动条
		if div.showHScrollBar:
			contentWidth = getDivContentWidth(div)
			if contentWidth > 0 and contentWidth > div.size.cx:
				sLeft = div.scrollH / contentWidth * div.size.cx
				sRight = (div.scrollH + div.size.cx) / contentWidth * div.size.cx
				if sRight - sLeft < div.scrollSize:
					sRight = sLeft + div.scrollSize
				if mp.x >= sLeft and mp.x <= sRight and mp.y >= div.size.cy - div.scrollSize and mp.y <= div.size.cy:
					div.hoverScrollHButton = True
					return
				else:
					div.hoverScrollHButton = False
		#判断纵向滚动条
		if div.showVScrollBar:
			contentHeight = getDivContentHeight(div)
			if contentHeight > 0 and contentHeight > div.size.cy:
				sTop = div.scrollV / contentHeight * div.size.cy
				sBottom = (div.scrollV + div.size.cy) / contentHeight * div.size.cy
				if sBottom - sTop < div.scrollSize:
					sBottom = sTop + div.scrollSize
				if mp.x >= div.size.cx - div.scrollSize and mp.x <= div.size.cx and mp.y >= sTop and mp.y <= sBottom:
					div.hoverScrollVButton = True
					return
				else:
					div.hoverScrollVButton = False

#重绘多页加 
#tabView:多页夹 
#paint:绘图对象 
#clipRect:裁剪区域
def drawTabViewBorder(tabView, paint, clipRect):
	if tabView.underLineColor != "none":
		tabPages = tabView.tabPages
		for tp in tabPages:
			if tp.visible:
				headerButton = tp.headerButton
				location = FCPoint(headerButton.location.x, headerButton.location.y)
				size = headerButton.size
				if tabView.useAnimation:
					if tabView.underPoint != None:
						location.x = tabView.underPoint.x
						location.y = tabView.underPoint.y
				if tabView.layout == "bottom":
					paint.fillRect(tabView.underLineColor, location.x, location.y, location.x + size.cx, location.y + tabView.underLineSize)
				elif tabView.layout == "left":
					paint.fillRect(tabView.underLineColor, location.x + size.cx - tabView.underLineSize, location.y, location.x + size.cx, location.y + size.cy)
				elif tabView.layout == "top":
					paint.fillRect(tabView.underLineColor, location.x, location.y + size.cy - tabView.underLineSize, location.x + size.cx, location.y + size.cy)
				elif tabView.layout == "right":
					paint.fillRect(tabView.underLineColor, location.x, location.y, location.x + tabView.underLineSize, location.y + size.cy)
				break

#更新页的布局 
#tabView:多页夹 
#tabPage:页 
#left:左侧坐标 
#top:上方坐标 
#width:宽度 
#height:高度 
#tw:页头按钮的宽度 
#th:页头按钮的高度
def updataPageLayout(tabView, tabPage, left, top, width, height, tw, th):
	newBounds = FCRect(0, 0, 0, 0)
	#下方
	if tabView.layout == "bottom":
		newBounds.left = 0
		newBounds.top = 0
		newBounds.right = width
		newBounds.bottom = height - th
		tabPage.headerButton.location = FCPoint(left, height - th)
	#左侧
	elif tabView.layout == "left":
		newBounds.left = tw
		newBounds.top = 0
		newBounds.right = width
		newBounds.bottom = height
		tabPage.headerButton.location = FCPoint(0, top)
	#右侧
	elif tabView.layout == "right":
		newBounds.left = 0
		newBounds.top = 0
		newBounds.right = width - tw
		newBounds.bottom = height
		tabPage.headerButton.location = FCPoint(width - tw, top)
	#上方
	elif tabView.layout == "top":
		newBounds.left = 0
		newBounds.top = th
		newBounds.right = width
		newBounds.bottom = height
		tabPage.headerButton.location = FCPoint(left, 0)
	tabPage.location = FCPoint(newBounds.left, newBounds.top)
	tabPage.size = FCSize(newBounds.right - newBounds.left, newBounds.bottom - newBounds.top)

#更新多页夹的布局 
#tabView:多页夹
def updateTabLayout(tabView):
	width = tabView.size.cx
	height = tabView.size.cy
	left = 0
	top = 0
	tabPages = tabView.tabPages
	for tabPage in tabPages:
		headerButton = tabPage.headerButton
		if headerButton.visible:
			tw = headerButton.size.cx
			th = headerButton.size.cy
			updataPageLayout(tabView, tabPage, left, top, width, height, tw, th)
			left += tw
			top += th
		else:
			tabPage.visible = False

#添加页 
#tabView:多页夹 
#tabPage:页 
#tabButton:页头按钮
def addTabPage(tabView, tabPage, tabButton):
	tabPage.headerButton = tabButton
	tabPage.parent = tabView
	tabPage.paint = tabView.paint
	tabButton.parent = tabView
	tabButton.paint = tabView.paint
	tabView.tabPages.append(tabPage)
	tabView.views.append(tabPage)
	tabView.views.append(tabButton)

#删除页
#tabView:多页夹 
#pageOrButton:页或者按钮
def removeTabPage(tabView, pageOrButton):
	for i in range(0, len(tabView.tabPages)):
		tabPage = tabView.tabPages[i]
		if tabPage.headerButton == pageOrButton or tabPage == pageOrButton:
			tabView.tabPages.remove(tabPage)
			removeViewFromParent(tabPage, tabView)
			removeViewFromParent(tabPage.headerButton, tabView)
			break
	if len(tabView.tabPages) > 0:
		selectTabPage(tabView, tabView.tabPages[0])
	updateTabLayout(tabView)
			
#选中页 
#tabView:多页夹 
#tabPage:页
def selectTabPage(tabView, tabPage):
	tabPages = tabView.tabPages
	for tp in tabPages:
		if tp == tabPage:
			tp.visible = True
		else:
			tp.visible = False
	updateTabLayout(tabView)

#重置布局图层 
#layout:布局层
def resetLayoutDiv(layout):
	reset = False
	padding = layout.padding
	vPos = 0
	left = padding.left
	top = padding.top
	width = layout.size.cx - padding.left - padding.right
	height = layout.size.cy - padding.top - padding.bottom
	i = 0
	subViews = layout.views
	for view in subViews:
		if view.visible:
			size = FCSize(view.size.cx, view.size.cy)
			margin = view.margin
			cLeft = view.location.x
			cTop = view.location.y
			cWidth = size.cx
			cHeight = size.cy
			nLeft = cLeft
			nTop = cTop
			nWidth = cWidth
			nHeight = cHeight
			#从下至上
			if layout.layoutStyle == "bottomtotop":
				if i == 0:
					top = height - padding.top
				lWidth = 0
				if layout.autoWrap:
					lWidth = size.cx
					lTop = top - margin.top - cHeight - margin.bottom
					if lTop < padding.top:
						if vPos != 0:
							left += cWidth + margin.left
						top = height - padding.top
				else:
					lWidth = width - margin.left - margin.right
				top -= cHeight + margin.bottom
				nLeft = left + margin.left
				nWidth = lWidth
				nTop = top
			#从左到右
			elif layout.layoutStyle == "lefttoright":
				lHeight = 0
				if layout.autoWrap:
					lHeight = size.cy
					lRight = left + margin.left + cWidth + margin.right
					if lRight > width:
						left = padding.left
						if vPos != 0:
							top += cHeight + margin.top
				else:
					lHeight = height - margin.top - margin.bottom
				left += margin.left
				nLeft = left
				nTop = top + margin.top
				nHeight = lHeight
				left += cWidth + margin.right
			#从右到左
			elif layout.layoutStyle == "righttoleft":
				if i == 0:
					left = width - padding.left
				lHeight = 0
				if layout.autoWrap:
					lHeight = size.cy
					lLeft = left - margin.left - cWidth - margin.right
					if lLeft < padding.left:
						left = width - padding.left
						if vPos != 0:
							top += cHeight + margin.top
				else:
					lHeight = height - margin.top - margin.bottom
				left -= cWidth + margin.left
				nLeft = left
				nTop = top + margin.top
				nHeight = lHeight
			#从上至下
			elif layout.layoutStyle == "toptobottom":
				lWidth = 0
				if layout.autoWrap:
					lWidth = size.cx
					lBottom = top + margin.top + cHeight + margin.bottom
					if lBottom > height:
						if vPos != 0:
							left += cWidth + margin.left + margin.right
						top = padding.top
				else:
					lWidth = width - margin.left - margin.right
					top += margin.top
					nTop = top
					nLeft = left + margin.left
					nWidth = lWidth
					top += cHeight + margin.bottom
			if cLeft != nLeft or cTop != nTop or cWidth != nWidth or cHeight != nHeight:
				view.location = FCPoint(nLeft, nTop)
				view.size = FCSize(nWidth, nHeight)
				reset = True
			vPos = vPos + 1
			i = i + 1
	return reset

#重置分割线的布局
#split:分割视图
def resetSplitLayoutDiv(split):
	reset = False
	splitRect = FCRect(0, 0, 0, 0)
	width = split.size.cx
	height = split.size.cy
	fRect = FCRect(0, 0, 0, 0)
	sRect = FCRect(0, 0, 0, 0)
	splitterSize = FCSize(0, 0)
	if split.splitter.visible:
		splitterSize.cx = split.splitter.size.cx
		splitterSize.cy = split.splitter.size.cy
	layoutStyle = split.layoutStyle 
	#从下至上
	if layoutStyle == "bottomtotop":
		if split.splitMode == "absolutesize" or split.oldSize.cy == 0:
			splitRect.left = 0
			splitRect.top = height - (split.oldSize.cy - split.splitter.location.y)
			splitRect.right = width
			splitRect.bottom = splitRect.top + splitterSize.cy
		elif split.splitMode == "percentsize":
			splitRect.left = 0
			if split.splitPercent == -1:
				split.splitPercent = split.splitter.location.y / split.oldSize.cy
			splitRect.top = height * split.splitPercent
			splitRect.right = width
			splitRect.bottom = splitRect.top + splitterSize.cy
		fRect.left = 0
		fRect.top = splitRect.bottom
		fRect.right = width
		fRect.bottom = height
		sRect.left = 0
		sRect.top = 0
		sRect.right = width
		sRect.bottom = splitRect.top
	#从左至右
	elif layoutStyle == "lefttoright":
		if split.splitMode == "absolutesize" or split.oldSize.cx == 0:
			splitRect.left = split.splitter.location.x
			splitRect.top = 0
			splitRect.right = splitRect.left + splitterSize.cx
			splitRect.bottom = height
		elif split.splitMode == "percentsize":
			if split.splitPercent == -1:
				split.splitPercent = split.splitter.location.x / split.oldSize.cx
			splitRect.left = width * split.splitPercent
			splitRect.top = 0
			splitRect.right = splitRect.left + splitterSize.cx
			splitRect.bottom = height
		fRect.left = 0
		fRect.top = 0
		fRect.right = splitRect.left
		fRect.bottom = height
		sRect.left = splitRect.right
		sRect.top = 0
		sRect.right = width
		sRect.bottom = height
	#从右到左
	elif layoutStyle == "righttoleft":
		if split.splitMode == "absolutesize" or split.oldSize.cx == 0:
			splitRect.left = width - (split.oldSize.cx - split.splitter.location.x)
			splitRect.top = 0
			splitRect.right = splitRect.left + splitterSize.cx
			splitRect.bottom = height
		elif split.splitMode == "percentsize":
			if split.splitPercent == -1:
				split.splitPercent = split.splitter.location.x / split.oldSize.cx
			splitRect.left = width * split.splitPercent
			splitRect.top = 0
			splitRect.right = splitRect.left + splitterSize.cx
			splitRect.bottom = height
		fRect.left = splitRect.right
		fRect.top = 0
		fRect.right = width
		fRect.bottom = height
		sRect.left = 0
		sRect.top = 0
		sRect.right = splitRect.left
		sRect.bottom = height
	#从上至下
	elif layoutStyle == "toptobottom":
		if split.splitMode == "absolutesize" or split.oldSize.cy == 0:
			splitRect.left = 0
			splitRect.top = split.splitter.location.y
			splitRect.right = width
			splitRect.bottom = splitRect.top + splitterSize.cy
		elif split.splitMode == "percentsize":
			splitRect.left = 0
			if split.splitPercent == -1:
				split.splitPercent = split.splitter.location.y / split.oldSize.cy
			splitRect.top = height * split.splitPercent
			splitRect.right = width
			splitRect.bottom = splitRect.top + splitterSize.cy
		fRect.left = 0
		fRect.top = 0
		fRect.right = width
		fRect.bottom = splitRect.top
		sRect.left = 0
		sRect.top = splitRect.bottom
		sRect.right = width
		sRect.bottom = height
	#重置分割条
	if split.splitter.visible:
		spRect = FCRect(split.splitter.location.x,  split.splitter.location.y, split.splitter.location.x + split.splitter.size.cx, split.splitter.location.y + split.splitter.size.cy)
		if spRect.left != splitRect.left or spRect.top != splitRect.top or spRect.right != splitRect.right or spRect.bottom != splitRect.bottom:
			split.splitter.location = FCPoint(splitRect.left, splitRect.top)
			split.splitter.size = FCSize(splitRect.right - splitRect.left, splitRect.bottom - splitRect.top)
			reset = True
	fcRect = FCRect(split.firstView.location.x,  split.firstView.location.y, split.firstView.location.x + split.firstView.size.cx, split.firstView.location.y + split.firstView.size.cy)
	#重置第一个视图
	if fcRect.left != fRect.left or fcRect.top != fRect.top or fcRect.right != fRect.right or fcRect.bottom != fRect.bottom:
		reset = True
		split.firstView.location = FCPoint(fRect.left, fRect.top)
		split.firstView.size = FCSize(fRect.right - fRect.left, fRect.bottom - fRect.top)
	scRect = FCRect(split.secondView.location.x,  split.secondView.location.y, split.secondView.location.x + split.secondView.size.cx, split.secondView.location.y + split.secondView.size.cy)
	#重置第二个视图
	if scRect.left != sRect.left or scRect.top != sRect.top or scRect.right != sRect.right or scRect.bottom != sRect.bottom:
		reset = True
		split.secondView.location = FCPoint(sRect.left, sRect.top)
		split.secondView.size = FCSize(sRect.right - sRect.left, sRect.bottom - sRect.top)
	split.oldSize = FCSize(width, height)
	return reset

#快速添加表格列
#grid:表格
#columns:列名集合
def fastAddGridColumns(grid, columns):
	columnsSize = len(columns)
	for i in range(0,columnsSize):
		gridColumn = FCGridColumn()
		gridColumn.text = columns[i]
		grid.columns.append(gridColumn)

#快速添加表格行
#grid:表格
#datas:数据集合
def fastAddGridRow(grid, datas):
	gridRow = FCGridRow()
	datasSize = len(datas)
	for i in range(0,datasSize):
		gridCell = FCGridCell()
		gridCell.value = datas[i]
		gridRow.cells.append(gridCell)
	return gridRow

#添加视图到单元格
#view:视图
#cell:单元格
#grid:表格
def addViewToGridCell(view, cell, grid):
	view.displayOffset = False
	view.visible = False
	cell.view = view
	addViewToParent(view, grid)

#表格的鼠标滚轮方法 
#grid:表格 
#delta:滚轮值
def touchWheelGrid(grid, delta):
	oldScrollV = grid.scrollV
	if delta > 0:
		oldScrollV -= grid.rowHeight
	elif delta < 0:
		oldScrollV += grid.rowHeight
	contentHeight = getGridContentHeight(grid)
	if contentHeight < grid.size.cy - grid.headerHeight - grid.scrollSize:
		grid.scrollV = 0
	else:
		if oldScrollV < 0:
			oldScrollV = 0
		elif oldScrollV > contentHeight - grid.size.cy + grid.headerHeight + grid.scrollSize:
			oldScrollV = contentHeight - grid.size.cy + grid.headerHeight + grid.scrollSize
		grid.scrollV = oldScrollV

#绘制单元格 
#grid:表格 
#row:行 
#column:列 
#cell:单元格
#paint:绘图对象 
#left:左侧坐标 
#top:上方坐标 
#right:右侧坐标 
#bottom:下方坐标
def drawGridCell(grid, row, column, cell, paint, left, top, right, bottom):
	#绘制背景
	if cell.backColor != "none":
		paint.fillRect(cell.backColor, left, top, right, bottom)
	#绘制选中
	if row.selected:
		if grid.selectedRowColor != "none":
			paint.fillRect(grid.selectedRowColor, left, top, right, bottom)
	#绘制边线
	if cell.borderColor != "none":
		#paint.drawRect(cell.borderColor, 1, 0, left, top, right, bottom)
		paint.drawLine(cell.borderColor, 1, 0, left, bottom, right, bottom)
		paint.drawLine(cell.borderColor, 1, 0, right - 1, top, right - 1, bottom)
	#绘制数值
	if cell.value != None:
		showText = str(cell.value)
		if column.colType == "double":
			if cell.digit >= 0:
				numValue = float(showText)
				showText = toFixed(numValue, cell.digit)
		tSize = paint.textSize(showText, cell.font)
		if tSize.cx > right - left:
			paint.drawTextAutoEllipsis(showText, cell.textColor, cell.font, left + 2, top + grid.rowHeight / 2 - tSize.cy / 2, right - 2, top + grid.rowHeight / 2 + tSize.cy / 2)
		else:
			if column.cellAlign == "left":
				paint.drawText(showText, cell.textColor, cell.font, left + 2, top + grid.rowHeight / 2 - tSize.cy / 2)
			elif column.cellAlign == "center":
				paint.drawText(showText, cell.textColor, cell.font, left + (right - left - tSize.cx) / 2, top + grid.rowHeight / 2 - tSize.cy / 2)
			elif column.cellAlign == "right":
				paint.drawText(showText, cell.textColor, cell.font, right - tSize.cx, top + grid.rowHeight / 2 - tSize.cy / 2)	

#获取内容的宽度 
#grid:表格
def getGridContentWidth(grid):
	cWidth = 0
	for column in grid.columns:
		if column.visible:
			cWidth += column.width
	return cWidth

#获取内容的高度 
#grid:表格
def getGridContentHeight(grid):
	cHeight = 0
	for row in grid.rows:
		if row.visible:
			cHeight += grid.rowHeight
	return cHeight

#绘制列 
#grid:表格 
#column:列
#paint:绘图对象 
#left:左侧坐标 
#top:上方坐标 
#right:右侧坐标 
#bottom:下方坐标
def drawGridColumn(grid, column, paint, left, top, right, bottom):
	tSize = paint.textSize(column.text, column.font)
	#绘制背景
	if column.backColor != "none":
		paint.fillRect(column.backColor, left, top, right, bottom)
	#绘制边线
	if column.borderColor != "none":
		paint.drawRect(column.borderColor, 1, 0, left, top, right, bottom)
	paint.drawText(column.text, column.textColor, column.font, left + (column.width - tSize.cx) / 2, top + grid.headerHeight / 2 - tSize.cy / 2)
	#绘制升序箭头
	if column.sort == "asc":
		cR = (bottom - top) / 4
		oX = right - cR * 2
		oY = top + (bottom - top) / 2
		drawPoints = []
		drawPoints.append(FCPoint(oX, oY - cR))
		drawPoints.append(FCPoint(oX - cR, oY + cR))
		drawPoints.append(FCPoint(oX + cR, oY + cR))
		paint.fillPolygon(column.textColor, drawPoints)
	#绘制降序箭头
	elif column.sort == "desc":
		cR = (bottom - top) / 4
		oX = right - cR * 2
		oY = top + (bottom - top) / 2
		drawPoints = []
		drawPoints.append(FCPoint(oX, oY + cR))
		drawPoints.append(FCPoint(oX - cR, oY - cR))
		drawPoints.append(FCPoint(oX + cR, oY - cR))
		paint.fillPolygon(column.textColor, drawPoints)

#绘制表格 
#grid:表格
#paint:绘图对象 
#clipRect:裁剪区域
def drawGrid(grid, paint, clipRect):
	cTop = -grid.scrollV + grid.headerHeight
	colLeft = 0
	for i in range(0, len(grid.views)):
		grid.views[i].visible = False
	#重置列头
	for i in range(0, len(grid.columns)):
		column = grid.columns[i]
		if len(column.widthStr) > 0:
			newWidthStr = column.widthStr.replace("%", "")
			grid.columns[i].width = int(float(newWidthStr) * grid.size.cx / 100)
		colRect = FCRect(colLeft, 0, colLeft + grid.columns[i].width, grid.headerHeight)
		column.bounds = colRect
		column.index = i
		colLeft += column.width
	for i in range(0, len(grid.rows)):
		row = grid.rows[i]
		row.index = i
		if row.visible:
			rTop = cTop
			rBottom = cTop + grid.rowHeight
			#绘制非冻结列
			if rBottom >= 0 and cTop <= grid.size.cy:
				for j in range(0, len(row.cells)):
					cell = row.cells[j]
					gridColumn = cell.column
					if gridColumn == None:
						gridColumn = grid.columns[j]
					if gridColumn.visible:
						if gridColumn.frozen == False:
							cellWidth = gridColumn.width
							colSpan = cell.colSpan
							if colSpan > 1:
								for n in range(1,colSpan):
									spanColumn = grid.columns[gridColumn.index + n]
									if spanColumn != None and spanColumn.visible:
										cellWidth += spanColumn.width
							cellHeight = grid.rowHeight
							rowSpan = cell.rowSpan
							if rowSpan > 1:
								for n in range(1,rowSpan):
									spanRow = grid.rows[i + n]
									if spanRow != None and spanRow.visible:
										cellHeight += grid.rowHeight
							cRect = FCRect(gridColumn.bounds.left - grid.scrollH, rTop, gridColumn.bounds.left + cellWidth - grid.scrollH, rTop + cellHeight)
							if cRect.right >= 0 and cRect.left < grid.size.cx:
								if grid.onPaintGridCell != None:
									grid.onPaintGridCell(grid, row, gridColumn, cell, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
								elif grid.paint.onPaintGridCell != None:
									grid.paint.onPaintGridCell(grid, row, gridColumn, cell, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
								else:
									drawGridCell(grid, row, gridColumn, cell, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
								if cell.view != None:
									cell.view.visible = True
									cell.view.location = FCPoint(cRect.left + grid.scrollH, cRect.top + grid.scrollV)
									cell.view.size = FCSize(cRect.right - cRect.left, cRect.bottom - cRect.top)
			#绘制冻结列
			if rBottom >= 0 and cTop <= grid.size.cy:
				for j in range(0, len(row.cells)):
					cell = row.cells[j]
					gridColumn = cell.column
					if gridColumn == None:
						gridColumn = grid.columns[j]
					if gridColumn.visible:
						if gridColumn.frozen:
							cellWidth = gridColumn.width
							colSpan = cell.colSpan
							if colSpan > 1:
								for n in range(1,colSpan):
									spanColumn = grid.columns[gridColumn.index + n]
									if spanColumn != None and spanColumn.visible:
										cellWidth += spanColumn.width
							cellHeight = grid.rowHeight
							rowSpan = cell.rowSpan
							if rowSpan > 1:
								for n in range(1,rowSpan):
									spanRow = grid.rows[i + n]
									if spanRow != None and spanRow.visible:
										cellHeight += grid.rowHeight
							cRect = FCRect(gridColumn.bounds.left, rTop, gridColumn.bounds.left + cellWidth, rTop + cellHeight)
							if cRect.right >= 0 and cRect.left < grid.size.cx:
								if grid.onPaintGridCell != None:
									grid.onPaintGridCell(grid, row, gridColumn, cell, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
								elif grid.paint.onPaintGridCell != None:
									grid.paint.onPaintGridCell(grid, row, gridColumn, cell, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
								else:
									drawGridCell(grid, row, gridColumn, cell, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
								if cell.view != None:
									cell.view.visible = True
									cell.view.location = FCPoint(cRect.left + grid.scrollH, cRect.top + grid.scrollV)
									cell.view.size = FCSize(cRect.right - cRect.left, cRect.bottom - cRect.top)
			if cTop > grid.size.cy:
				break
			cTop += grid.rowHeight
	

#绘制表格的滚动条 
#grid:表格 
#paint:绘图对象
#clipRect:裁剪区域
def drawGridScrollBar(grid, paint, clipRect):
	grid.hScrollIsVisible = False
	grid.vScrollIsVisible = False
	if grid.headerHeight > 0:
		cLeft = -grid.scrollH
		#绘制非冻结列
		for gridColumn in grid.columns:
			if gridColumn.visible:
				if gridColumn.frozen == False:
					if grid.onPaintGridColumn != None:
						grid.onPaintGridColumn(grid, gridColumn, paint, cLeft, 0, cLeft + gridColumn.width, grid.headerHeight)
					elif grid.paint.onPaintGridColumn != None:
						grid.paint.onPaintGridColumn(grid, gridColumn, paint, cLeft, 0, cLeft + gridColumn.width, grid.headerHeight)
					else:
						drawGridColumn(grid, gridColumn, paint, cLeft, 0, cLeft + gridColumn.width, grid.headerHeight)
				cLeft += gridColumn.width
		cLeft = 0
		#绘制冻结列
		for gridColumn in grid.columns:
			if gridColumn.visible:
				if gridColumn.frozen:
					if grid.onPaintGridColumn != None:
						grid.onPaintGridColumn(grid, gridColumn, paint, cLeft, 0, cLeft + gridColumn.width, grid.headerHeight)
					elif grid.paint.onPaintGridColumn != None:
						grid.paint.onPaintGridColumn(grid, gridColumn, paint, cLeft, 0, cLeft + gridColumn.width, grid.headerHeight)
					else:
						drawGridColumn(grid, gridColumn, paint, cLeft, 0, cLeft + gridColumn.width, grid.headerHeight)
				cLeft += gridColumn.width
	#绘制横向滚动条
	if grid.showHScrollBar:
		contentWidth = getGridContentWidth(grid)
		if contentWidth > 0 and contentWidth > grid.size.cx:
			sLeft = grid.scrollH / contentWidth * grid.size.cx
			sRight = (grid.scrollH + grid.size.cx) / contentWidth * grid.size.cx
			if sRight - sLeft < grid.scrollSize:
				sRight = sLeft + grid.scrollSize
			if paint.touchMoveView == grid and (grid.hoverScrollHButton or grid.downScrollHButton):
				paint.fillRect(grid.scrollBarHoveredColor, sLeft, grid.size.cy - grid.scrollSize, sRight, grid.size.cy)
			else:
				paint.fillRect(grid.scrollBarColor, sLeft, grid.size.cy - grid.scrollSize, sRight, grid.size.cy)
			grid.hScrollIsVisible = True
	#绘制纵向滚动条
	if grid.showVScrollBar:
		contentHeight = getGridContentHeight(grid)
		if contentHeight > 0 and contentHeight > grid.size.cy - grid.headerHeight and contentHeight > 0 and grid.size.cy - grid.headerHeight - grid.scrollSize > 0:
			sTop = grid.headerHeight + grid.scrollV / contentHeight * (grid.size.cy - grid.headerHeight - grid.scrollSize)
			sBottom = sTop + ((grid.size.cy - grid.headerHeight - grid.scrollSize)) / contentHeight * (grid.size.cy - grid.headerHeight - grid.scrollSize)
			if sBottom - sTop < grid.scrollSize:
				sBottom = sTop + grid.scrollSize
			if paint.touchMoveView == grid and (grid.hoverScrollVButton or grid.downScrollVButton):
				paint.fillRect(grid.scrollBarHoveredColor, grid.size.cx - grid.scrollSize, sTop, grid.size.cx, sBottom)
			else:
				paint.fillRect(grid.scrollBarColor, grid.size.cx - grid.scrollSize, sTop, grid.size.cx, sBottom)
			grid.vScrollIsVisible = True

#表格的鼠标移动方法 
#grid: 表格 
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
def touchMoveGrid(grid, firstTouch, firstPoint, secondTouch, secondPoint):
	grid.hoverScrollHButton = False
	grid.hoverScrollVButton = False
	if grid.paint.resizeColumnState != 0:
		gridColumn = grid.columns[grid.paint.resizeColumnIndex]
		newWidth = grid.paint.resizeColumnBeginWidth + (firstPoint.x - grid.startPoint.x)
		if newWidth > 10:
			gridColumn.width = newWidth
		return
	mp = firstPoint
	if firstTouch:
		if grid.showHScrollBar or grid.showVScrollBar:
			#判断横向滚动条
			if grid.downScrollHButton:
				contentWidth = getGridContentWidth(grid)
				subX = (mp.x - grid.startPoint.x) / grid.size.cx * contentWidth
				newScrollH = grid.startScrollH + subX
				if newScrollH < 0:
					newScrollH = 0
				elif newScrollH > contentWidth - grid.size.cx:
					newScrollH = contentWidth - grid.size.cx
				grid.scrollH = newScrollH
				grid.paint.cancelClick = True
				return
			#判断纵向滚动条
			elif grid.downScrollVButton:
				contentHeight = getGridContentHeight(grid)
				subY = (mp.y - grid.startPoint.y) / (grid.size.cy - grid.headerHeight - grid.scrollSize) * contentHeight
				newScrollV = grid.startScrollV + subY
				if newScrollV < 0:
					newScrollV = 0
				elif newScrollV > contentHeight - (grid.size.cy - grid.headerHeight - grid.scrollSize):
					newScrollV = contentHeight - (grid.size.cy - grid.headerHeight - grid.scrollSize)
				grid.scrollV = newScrollV
				grid.paint.cancelClick = True
				return
		#处理拖动
		if grid.allowDragScroll:
			contentWidth = getGridContentWidth(grid)
			if contentWidth > grid.size.cx - grid.scrollSize:
				subX = grid.startPoint.x - mp.x
				newScrollH = grid.startScrollH + subX
				if newScrollH < 0:
					newScrollH = 0
				elif newScrollH > contentWidth - grid.size.cx:
					newScrollH = contentWidth - grid.size.cx
				grid.scrollH = newScrollH
				if abs(subX) > 5:
					grid.paint.cancelClick = True
			contentHeight = getGridContentHeight(grid)
			if contentHeight > grid.size.cy - grid.headerHeight - grid.scrollSize:
				subY = grid.startPoint.y - mp.y
				newScrollV = grid.startScrollV + subY
				if newScrollV < 0:
					newScrollV = 0
				elif newScrollV > contentHeight - (grid.size.cy - grid.headerHeight - grid.scrollSize):
					newScrollV = contentHeight - (grid.size.cy - grid.headerHeight - grid.scrollSize)
				grid.scrollV = newScrollV
				if abs(subY) > 5:
					grid.paint.cancelClick = True
	else:
		#判断横向滚动条
		if grid.showHScrollBar:
			contentWidth = getGridContentWidth(grid)
			if contentWidth > 0 and contentWidth > grid.size.cx - grid.scrollSize:
				sLeft = grid.scrollH / contentWidth * grid.size.cx
				sRight = (grid.scrollH + grid.size.cx) / contentWidth * grid.size.cx
				if sRight - sLeft < grid.scrollSize:
					sRight = sLeft + grid.scrollSize
				if mp.x >= sLeft and mp.x <= sRight and mp.y >= grid.size.cy - grid.scrollSize and mp.y <= grid.size.cy:
					grid.hoverScrollHButton = True
					return
				else:
					grid.hoverScrollHButton = False
		#判断纵向滚动条
		if grid.showVScrollBar:
			contentHeight = getGridContentHeight(grid)
			if contentHeight > 0 and contentHeight > grid.size.cy - grid.headerHeight - grid.scrollSize:
				sTop = grid.headerHeight + grid.scrollV / contentHeight * (grid.size.cy - grid.headerHeight - grid.scrollSize)
				sBottom = grid.headerHeight + (grid.scrollV + (grid.size.cy - grid.headerHeight - grid.scrollSize)) / contentHeight * (grid.size.cy - grid.headerHeight - grid.scrollSize)
				if sBottom - sTop < grid.scrollSize:
					sBottom = sTop + grid.scrollSize
				if mp.x >= grid.size.cx - grid.scrollSize and mp.x <= grid.size.cx and mp.y >= sTop and mp.y <= sBottom:
					grid.hoverScrollVButton = True
					return
				else:
					grid.hoverScrollVButton = False

#表格的鼠标按下方法 
#grid: 表格 
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks:点击次数
def touchDownGrid(grid, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	mp = firstPoint
	grid.startPoint = mp
	grid.downScrollHButton = False
	grid.downScrollVButton = False
	grid.hoverScrollHButton = False
	grid.hoverScrollVButton = False
	#判断横向滚动条
	if grid.showHScrollBar:
		contentWidth = getGridContentWidth(grid)
		if contentWidth > 0 and contentWidth > grid.size.cx - grid.scrollSize:
			sLeft = grid.scrollH / contentWidth * grid.size.cx
			sRight = (grid.scrollH + grid.size.cx) / contentWidth * grid.size.cx
			if sRight - sLeft < grid.scrollSize:
				sRight = sLeft + grid.scrollSize
			if mp.x >= sLeft and mp.x <= sRight and mp.y >= grid.size.cy - grid.scrollSize and mp.y <= grid.size.cy:
				grid.downScrollHButton = True
				grid.startScrollH = grid.scrollH
				return
	#判断纵向滚动条
	if grid.showVScrollBar:
		contentHeight = getGridContentHeight(grid)
		if contentHeight > 0 and contentHeight > grid.size.cy - grid.headerHeight - grid.scrollSize:
			sTop = grid.headerHeight + grid.scrollV / contentHeight * (grid.size.cy - grid.headerHeight - grid.scrollSize)
			sBottom = grid.headerHeight + (grid.scrollV + (grid.size.cy - grid.headerHeight - grid.scrollSize)) / contentHeight * (grid.size.cy - grid.headerHeight - grid.scrollSize)
			if sBottom - sTop < grid.scrollSize:
				sBottom = sTop + grid.scrollSize
			if mp.x >= grid.size.cx - grid.scrollSize and mp.x <= grid.size.cx and mp.y >= sTop and mp.y <= sBottom:
				grid.downScrollVButton = True
				grid.startScrollV = grid.scrollV
				return
	if grid.allowDragScroll:
		grid.startScrollH = grid.scrollH
		grid.startScrollV = grid.scrollV
	colLeft = 0
	#重置列
	for i in range(0, len(grid.columns)):
		column = grid.columns[i]
		colRect = FCRect(colLeft, 0, colLeft + grid.columns[i].width, grid.headerHeight)
		column.bounds = colRect
		column.index = i
		colLeft += column.width
	grid.paint.resizeColumnState = 0
	grid.paint.resizeColumnBeginWidth = 0
	if grid.headerHeight > 0 and mp.y <= grid.headerHeight:
		for gridColumn in grid.columns:
			if gridColumn.visible:
				bounds = gridColumn.bounds
				if mp.x >= bounds.left - grid.scrollH and mp.x <= bounds.right - grid.scrollH:
					if gridColumn.index > 0 and mp.x < bounds.left + 5 - grid.scrollH:
						grid.paint.resizeColumnState = 1
						grid.paint.resizeColumnBeginWidth = grid.columns[gridColumn.index - 1].bounds.right - grid.columns[gridColumn.index - 1].bounds.left
						grid.paint.resizeColumnIndex = gridColumn.index - 1
						return
					elif mp.x > bounds.right - 5 - grid.scrollH:
						grid.paint.resizeColumnState = 2
						grid.paint.resizeColumnBeginWidth = bounds.right - bounds.left
						grid.paint.resizeColumnIndex = gridColumn.index
						return
					break

#表格的鼠标抬起方法 
#grid: 表格 
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks:点击次数
def touchUpGrid(grid, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	grid.downScrollHButton = False
	grid.downScrollVButton = False
	grid.hoverScrollHButton = False
	grid.hoverScrollVButton = False
	if grid.paint.cancelClick:
		return
	if grid.paint.resizeColumnState != 0:
		grid.paint.resizeColumnState = 0
		return
	cTop = -grid.scrollV + grid.headerHeight
	colLeft = 0
	#重置列
	for i in range(0, len(grid.columns)):
		column = grid.columns[i]
		colRect = FCRect(colLeft, 0, colLeft + grid.columns[i].width, grid.headerHeight)
		column.bounds = colRect
		column.index = i
		colLeft += column.width
	#判断列头
	if grid.headerHeight > 0 and firstPoint.y <= grid.headerHeight:
		cLeft = 0
		for gridColumn in grid.columns:
			if gridColumn.visible:
				if gridColumn.frozen:
					if firstPoint.x >= cLeft and firstPoint.x <= cLeft + gridColumn.width:
						for j in range(0, len(grid.columns)):
							tColumn = grid.columns[j]
							if tColumn == gridColumn:
								if tColumn.allowSort:
									for r in range(0, len(grid.rows)):
										if len(grid.rows[r].cells) > j:
											grid.rows[r].key = grid.rows[r].cells[j].value
									if tColumn.sort == "none" or tColumn.sort == "desc":
										tColumn.sort = "asc"
										grid.rows = sorted(grid.rows, key=attrgetter('key'), reverse=False)
									else:
										tColumn.sort = "desc"
										grid.rows = sorted(grid.rows, key=attrgetter('key'), reverse=True)
								else:
									tColumn.sort = "none"
							else:
								tColumn.sort = "none"
						if grid.onClickGridColumn != None:
							grid.onClickGridColumn(grid, gridColumn, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
						elif grid.paint.onClickGridColumn != None:
							grid.paint.onClickGridColumn(grid, gridColumn, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
						return
				cLeft += gridColumn.width
		cLeft = -grid.scrollH
		for gridColumn in grid.columns:
			if gridColumn.visible:
				if gridColumn.frozen == False:
					if firstPoint.x >= cLeft and firstPoint.x <= cLeft + gridColumn.width:
						for j in range(0, len(grid.columns)):
							tColumn = grid.columns[j]
							if tColumn == gridColumn:
								if tColumn.allowSort:
									for r in range(0, len(grid.rows)):
										if len(grid.rows[r].cells) > j:
											grid.rows[r].key = grid.rows[r].cells[j].value
									if tColumn.sort == "none" or tColumn.sort == "desc":
										tColumn.sort = "asc"
										grid.rows = sorted(grid.rows, key=attrgetter('key'), reverse=False)
									else:
										tColumn.sort = "desc"
										grid.rows = sorted(grid.rows, key=attrgetter('key'), reverse=True)
								else:
									tColumn.sort = "none"
							else:
								tColumn.sort = "none"
						if grid.onClickGridColumn != None:
							grid.onClickGridColumn(grid, gridColumn, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
						elif grid.paint.onClickGridColumn != None:
							grid.paint.onClickGridColumn(grid, gridColumn, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
						return
				cLeft += gridColumn.width
	for i in range(0, len(grid.rows)):
		row = grid.rows[i]
		if row.visible:
			rTop = cTop
			rBottom = cTop + grid.rowHeight
			#判断非冻结列
			if rBottom >= 0 and cTop <= grid.size.cy:
				for j in range(0, len(row.cells)):
					cell = row.cells[j]
					gridColumn = cell.column
					if gridColumn == None:
						gridColumn = grid.columns[j]
					if gridColumn.visible:
						if gridColumn.frozen:
							cellWidth = gridColumn.width
							colSpan = cell.colSpan
							if colSpan > 1:
								for n in range(1,colSpan):
									spanColumn = grid.columns[gridColumn.index + n]
									if spanColumn != None and spanColumn.visible:
										cellWidth += spanColumn.width
							cellHeight = grid.rowHeight
							rowSpan = cell.rowSpan
							if rowSpan > 1:
								for n in range(1,rowSpan):
									spanRow = grid.rows[i + n]
									if spanRow != None and spanRow.visible:
										cellHeight += grid.rowHeight
							cRect = FCRect(gridColumn.bounds.left, rTop, gridColumn.bounds.left + cellWidth, rTop + cellHeight)
							if cRect.right >= 0 and cRect.left < grid.size.cx:
								if firstPoint.x >= cRect.left and firstPoint.x <= cRect.right and firstPoint.y >= cRect.top and firstPoint.y <= cRect.bottom:
									for subRow in grid.rows:
										if subRow == row:
											subRow.selected = True
										else:
											subRow.selected = False
									if grid.onClickGridCell != None:
										grid.onClickGridCell(grid, row, gridColumn, cell, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
									elif grid.paint.onClickGridCell != None:
										grid.paint.onClickGridCell(grid, row, gridColumn, cell, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
									return
			#判断冻结列
			if rBottom >= 0 and cTop <= grid.size.cy:
				for j in range(0, len(row.cells)):
					cell = row.cells[j]
					gridColumn = cell.column
					if gridColumn == None:
						gridColumn = grid.columns[j]
					if gridColumn.visible:
						if gridColumn.frozen == False:
							cellWidth = gridColumn.width
							colSpan = cell.colSpan
							if colSpan > 1:
								for n in range(1,colSpan):
									spanColumn = grid.columns[gridColumn.index + n]
									if spanColumn != None and spanColumn.visible:
										cellWidth += spanColumn.width
							cellHeight = grid.rowHeight
							rowSpan = cell.rowSpan
							if rowSpan > 1:
								for n in range(1,rowSpan):
									spanRow = grid.rows[i + n]
									if spanRow != None and spanRow.visible:
										cellHeight += grid.rowHeight
							cRect = FCRect(gridColumn.bounds.left - grid.scrollH, rTop, gridColumn.bounds.left + cellWidth - grid.scrollH, rTop + cellHeight)
							if cRect.right >= 0 and cRect.left < grid.size.cx:
								if firstPoint.x >= cRect.left and firstPoint.x <= cRect.right and firstPoint.y >= cRect.top and firstPoint.y <= cRect.bottom:
									for subRow in grid.rows:
										if subRow == row:
											subRow.selected = True
										else:
											subRow.selected = False
									if grid.onClickGridCell != None:
										grid.onClickGridCell(grid, row, gridColumn, cell, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
									elif grid.paint.onClickGridCell != None:
										grid.paint.onClickGridCell(grid, row, gridColumn, cell, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
									return
			if cTop > grid.size.cy:
				break
			cTop += grid.rowHeight

#获取内容的宽度
#tree:树
def getTreeContentWidth(tree):
	cWidth = 0
	for column in tree.columns:
		if column.visible:
			cWidth += column.width
	return cWidth

#获取内容的高度
#tree:树
def getTreeContentHeight(tree):
	cHeight = 0
	for row in tree.rows:
		if row.visible:
			cHeight += tree.rowHeight
	return cHeight

#绘制滚动条
#tree:树
#paint:绘图对象
#clipRect:裁剪区域
def drawTreeScrollBar(tree, paint, clipRect):
	tree.hScrollIsVisible = False
	tree.vScrollIsVisible = False
	#判断横向滚动条
	if tree.showHScrollBar:
		contentWidth = getTreeContentWidth(tree)
		if contentWidth > 0 and contentWidth > tree.size.cx:
			sLeft = tree.scrollH / contentWidth * tree.size.cx
			sRight = (tree.scrollH + tree.size.cx) / contentWidth * tree.size.cx
			if sRight - sLeft < tree.scrollSize:
				sRight = sLeft + tree.scrollSize
			if paint.touchMoveView == tree and (tree.hoverScrollHButton or tree.downScrollHButton):
				paint.fillRect(tree.scrollBarHoveredColor, sLeft, tree.size.cy - tree.scrollSize, sRight, tree.size.cy)
			else:
				paint.fillRect(tree.scrollBarColor, sLeft, tree.size.cy - tree.scrollSize, sRight, tree.size.cy)
			tree.hScrollIsVisible = True
	#判断纵向滚动条
	if tree.showVScrollBar:
		contentHeight = getTreeContentHeight(tree)	
		if contentHeight > 0 and contentHeight > tree.size.cy:
			sTop = tree.headerHeight + tree.scrollV / contentHeight * (tree.size.cy - tree.headerHeight - tree.scrollSize)
			sBottom = sTop + ((tree.size.cy - tree.headerHeight)) / contentHeight * (tree.size.cy - tree.headerHeight - tree.scrollSize)
			if sBottom - sTop < tree.scrollSize:
				sBottom = sTop + tree.scrollSize
			if paint.touchMoveView == tree and (tree.hoverScrollVButton or tree.downScrollVButton):
				paint.fillRect(tree.scrollBarHoveredColor, tree.size.cx - tree.scrollSize, sTop, tree.size.cx, sBottom)
			else:
				paint.fillRect(tree.scrollBarColor, tree.size.cx - tree.scrollSize, sTop, tree.size.cx, sBottom)
			tree.vScrollIsVisible = True

#绘制单元格
#tree:树
#row:行
#column:列
#node:节点
#paint:绘图对象
#left:左侧坐标
#top:上方坐标
#right:右侧坐标
#bottom:下方坐标
def drawTreeNode(tree, row, column, node, paint, left, top, right, bottom):
	#绘制背景
	if node.backColor != "none":
		paint.fillRect(node.backColor, left, top, right, bottom)
	if node.value != None:
		tSize = paint.textSize(str(node.value), node.font)
		tLeft = left + 2 + getTotalIndent(node)
		wLeft = tLeft
		cR = tree.checkBoxWidth / 3
		#绘制复选框
		if tree.showCheckBox:
			wLeft += tree.checkBoxWidth
			if node.checked:
				paint.fillRect(node.textColor, tLeft + (tree.checkBoxWidth - cR) / 2, top + (tree.rowHeight - cR) / 2, tLeft + (tree.checkBoxWidth + cR) / 2, top + (tree.rowHeight + cR) / 2)
			else:
				paint.drawRect(node.textColor, 1, 0, tLeft + (tree.checkBoxWidth - cR) / 2, top + (tree.rowHeight - cR) / 2, tLeft + (tree.checkBoxWidth + cR) / 2, top + (tree.rowHeight + cR) / 2)
		#绘制箭头
		if len(node.childNodes) > 0:
			drawPoints = []
			if node.collapsed:
				drawPoints.append(FCPoint(wLeft + (tree.collapsedWidth + cR) / 2, top + tree.rowHeight / 2))
				drawPoints.append(FCPoint(wLeft + (tree.collapsedWidth - cR) / 2, top + (tree.rowHeight - cR) / 2))
				drawPoints.append(FCPoint(wLeft + (tree.collapsedWidth - cR) / 2, top + (tree.rowHeight + cR) / 2))
			else:
				drawPoints.append(FCPoint(wLeft + (tree.collapsedWidth - cR) / 2, top + (tree.rowHeight - cR) / 2))
				drawPoints.append(FCPoint(wLeft + (tree.collapsedWidth + cR) / 2, top + (tree.rowHeight - cR) / 2))
				drawPoints.append(FCPoint(wLeft + tree.collapsedWidth / 2, top + (tree.rowHeight + cR) / 2))
			paint.fillPolygon(node.textColor, drawPoints)
			wLeft += tree.collapsedWidth
		#绘制文字
		if tSize.cx > column.width:
			paint.drawTextAutoEllipsis(str(node.value), node.textColor, node.font, wLeft, top + tree.rowHeight / 2 - tSize.cy / 2, wLeft + column.width, top + tree.rowHeight / 2 - tSize.cy / 2)
		else:
			paint.drawText(str(node.value), node.textColor, node.font, wLeft, top + tree.rowHeight / 2 - tSize.cy / 2)

#更新行的索引
#tree:树
def updateTreeRowIndex(tree):
	for i in range(0,len(tree.rows)):
		tree.rows[i].index = i

#绘制树
#tree:树
#paint:绘图对象
#clipRect:裁剪区域
def drawTree(tree, paint, clipRect):
	cLeft = -tree.scrollH
	cTop = -tree.scrollV + tree.headerHeight
	colLeft = 0
	#重置列头
	for i in range(0,len(tree.columns)):
		if len(tree.columns[i].widthStr) > 0:
			newWidthStr = tree.columns[i].widthStr.replace("%", "")
			tree.columns[i].width = int(float(newWidthStr) * tree.size.cx / 100)
		colRect = FCRect(colLeft, 0, colLeft + tree.columns[i].width, tree.headerHeight)
		tree.columns[i].bounds = colRect
		tree.columns[i].index = i
		colLeft += tree.columns[i].width
	updateTreeRowIndex(tree)
	for i in range(0,len(tree.rows)):
		row = tree.rows[i]
		if row.visible:
			rTop = cTop
			rBottom = cTop + tree.rowHeight
			if rBottom >= 0 and cTop <= tree.size.cy:
				for j in range(0,len(row.cells)):
					node = row.cells[j]
					treeColumn = node.column
					if treeColumn == None:
						treeColumn = tree.columns[j]
					if treeColumn.visible:
						nodeWidth = treeColumn.width
						nodeHeight = tree.rowHeight
						cRect = FCRect(treeColumn.bounds.left - tree.scrollH, rTop, treeColumn.bounds.left + nodeWidth - tree.scrollH, rTop + nodeHeight)
						if cRect.right >= 0 and cRect.left < tree.size.cx:
							if tree.onPaintTreeNode != None:
								tree.onPaintTreeNode(tree, row, treeColumn, node, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
							elif tree.paint.onPaintTreeNode != None:
								tree.paint.onPaintTreeNode(tree, row, treeColumn, node, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
							else:
								drawTreeNode(tree, row, treeColumn, node, paint, cRect.left, cRect.top, cRect.right, cRect.bottom)
			if cTop > tree.size.cy:
				break
			cTop += tree.rowHeight

#获取最后一行的索引 
#node:树节点
def getTreeLastNodeRowIndex(node):
	rowIndex = node.row.index
	for i in range(0,len(node.childNodes)):
		rIndex = getTreeLastNodeRowIndex(node.childNodes[i])
		if rowIndex < rIndex:
			rowIndex = rIndex
	return rowIndex

#添加节点
#tree:树
#node:要添加的节点
#parentNode:父节点
def appendTreeNode(tree, node, parentNode):
	if parentNode == None:
		newRow = FCTreeRow()
		tree.rows.append(newRow)
		node.row = newRow
		newRow.cells.append(node)
		tree.childNodes.append(node)
	else:
		newRow = FCTreeRow()
		if len(parentNode.childNodes) == 0:
			tree.rows.insert(parentNode.row.index + 1, newRow)
		else:
			tree.rows.insert(getTreeLastNodeRowIndex(parentNode) + 1, newRow)
		node.parentNode = parentNode
		node.indent = tree.indent
		node.row = newRow
		newRow.cells.append(node)
		parentNode.childNodes.append(node)
		if parentNode.collapsed:
			newRow.visible = False
	updateTreeRowIndex(tree)

#移除节点
#tree:树
#node:要添加的节点
def removeTreeNode(tree, node):
	if node.parentNode == None:
		nodesSize = len(tree.childNodes)
		for i in range(0,nodesSize):
			if tree.childNodes[i] == node:
				tree.childNodes.pop(i)
				break
	else:
		nodesSize = len(node.parentNode.childNodes)
		for i in range(0,nodesSize):
			if node.parentNode.childNodes[i] == node:
				node.parentNode.childNodes.pop(i)
				break
	tree.rows.pop(node.row.index)
	updateTreeRowIndex(tree)

#展开或折叠节点
#node:节点
#visible:是否可见
def hideOrShowTreeNode(node, visible):
	if len(node.childNodes) > 0:
		for i in range(0,len(node.childNodes)):
			node.childNodes[i].row.visible = visible
			hideOrShowTreeNode(node.childNodes[i], visible)
#展开树的节点
#tree:树
def expendTree(tree):
	if len(tree.childNodes) > 0:
		for i in range(0,len(tree.childNodes)):
			tree.childNodes[i].collapsed = False
			hideOrShowTreeNode(tree.childNodes[i], True)

#折叠树的节点
#tree:树
def collapseTree(tree):
	if len(tree.childNodes) > 0:
		for i in range(0,len(tree.childNodes)):
			tree.childNodes[i].collapsed = True
			hideOrShowTreeNode(tree.childNodes[i], False)

#选中或反选节点
#node:节点
#checked:是否选中
def checkOrUnCheckTreeNode(node, checked):
	node.checked = checked
	if len(node.childNodes) > 0:
		for i in range(0,len(node.childNodes)):
			checkOrUnCheckTreeNode(node.childNodes[i], checked)

#树的鼠标滚轮方法
#tree:树
#delta:滚轮值
def touchWheelTree(tree, delta):
	oldScrollV = tree.scrollV
	if delta > 0:
		oldScrollV -= tree.rowHeight
	elif delta < 0:
		oldScrollV += tree.rowHeight
	contentHeight = getTreeContentHeight(tree)
	if contentHeight < tree.size.cy:
		tree.scrollV = 0
	else:
		if oldScrollV < 0:
			oldScrollV = 0
		elif oldScrollV > contentHeight - tree.size.cy + tree.headerHeight + tree.scrollSize:
			oldScrollV = contentHeight - tree.size.cy + tree.headerHeight + tree.scrollSize
		tree.scrollV = oldScrollV

#树的鼠标移动方法
#tree: 树
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
def touchMoveTree(tree, firstTouch, firstPoint, secondTouch, secondPoint):
	tree.hoverScrollHButton = False
	tree.hoverScrollVButton = False
	mp = firstPoint
	if firstTouch:
		if tree.showHScrollBar or tree.showVScrollBar:
			#判断横向滚动
			if tree.downScrollHButton:
				contentWidth = getTreeContentWidth(tree)
				subX = (mp.x - tree.startPoint.x) / tree.size.cx * contentWidth
				newScrollH = tree.startScrollH + subX
				if newScrollH < 0:
					newScrollH = 0
				elif newScrollH > contentWidth - tree.size.cx:
					newScrollH = contentWidth - tree.size.cx
				tree.scrollH = newScrollH
				tree.paint.cancelClick = True
				return
			#判断纵向滚动
			elif tree.downScrollVButton:
				contentHeight = getTreeContentHeight(tree)
				subY = (mp.y - tree.startPoint.y) / (tree.size.cy - tree.headerHeight - tree.scrollSize) * contentHeight
				newScrollV = tree.startScrollV + subY
				if newScrollV < 0:
					newScrollV = 0
				elif newScrollV > contentHeight - (tree.size.cy - tree.headerHeight - tree.scrollSize):
					newScrollV = contentHeight - (tree.size.cy - tree.headerHeight - tree.scrollSize)
				tree.scrollV = newScrollV
				tree.paint.cancelClick = True
				return
		#判断拖动
		if tree.allowDragScroll:
			contentWidth = getTreeContentWidth(tree)
			if contentWidth > tree.size.cx:
				subX = tree.startPoint.x - mp.x
				newScrollH = tree.startScrollH + subX
				if newScrollH < 0:
					newScrollH = 0
				elif newScrollH > contentWidth - tree.size.cx:
					newScrollH = contentWidth - tree.size.cx
				tree.scrollH = newScrollH
				if abs(subX) > 5:
					tree.paint.cancelClick = True
			contentHeight = getTreeContentHeight(tree)
			if contentHeight > tree.size.cy:
				subY = tree.startPoint.y - mp.y
				newScrollV = tree.startScrollV + subY
				if newScrollV < 0:
					newScrollV = 0
				elif newScrollV > contentHeight - (tree.size.cy - tree.headerHeight - tree.scrollSize):
					newScrollV = contentHeight - (tree.size.cy - tree.headerHeight - tree.scrollSize)
				tree.scrollV = newScrollV
				if abs(subY) > 5:
					tree.paint.cancelClick = True
	else:
		#判断横向滚动
		if tree.showHScrollBar:
			contentWidth = getTreeContentWidth(tree)
			if contentWidth > 0 and contentWidth > tree.size.cx:
				sLeft = tree.scrollH / contentWidth * tree.size.cx
				sRight = (tree.scrollH + tree.size.cx) / contentWidth * tree.size.cx
				if sRight - sLeft < tree.scrollSize:
					sRight = sLeft + tree.scrollSize
				if mp.x >= sLeft and mp.x <= sRight and mp.y >= tree.size.cy - tree.scrollSize and mp.y <= tree.size.cy:
					tree.hoverScrollHButton = True
					return
				else:
					tree.hoverScrollHButton = False
		#判断纵向滚动
		if tree.showVScrollBar:
			contentHeight = getTreeContentHeight(tree)
			if contentHeight > 0 and contentHeight > tree.size.cy:
				sTop = tree.headerHeight + tree.scrollV / contentHeight * (tree.size.cy - tree.headerHeight - tree.scrollSize)
				sBottom = tree.headerHeight + (tree.scrollV + (tree.size.cy - tree.headerHeight - tree.scrollSize)) / contentHeight * (tree.size.cy - tree.headerHeight - tree.scrollSize)
				if sBottom - sTop < tree.scrollSize:
					sBottom = sTop + tree.scrollSize
				if mp.x >= tree.size.cx - tree.scrollSize and mp.x <= tree.size.cx and mp.y >= sTop and mp.y <= sBottom:
					tree.hoverScrollVButton = True
					return
				else:
					tree.hoverScrollVButton = False
					

#树的鼠标按下方法
#tree: 树
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks 点击次数
def touchDownTree(tree, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	mp = firstPoint
	tree.startPoint = mp
	tree.hoverScrollHButton = False
	tree.hoverScrollVButton = False
	tree.downScrollHButton = False
	tree.downScrollVButton = False
	#判断横向滚动
	if tree.showHScrollBar:
		contentWidth = getTreeContentWidth(tree)
		if contentWidth > 0 and contentWidth > tree.size.cx:
			sLeft = tree.scrollH / contentWidth * tree.size.cx
			sRight = (tree.scrollH + tree.size.cx) / contentWidth * tree.size.cx
			if sRight - sLeft < tree.scrollSize:
				sRight = sLeft + tree.scrollSize
			if mp.x >= sLeft and mp.x <= sRight and mp.y >= tree.size.cy - tree.scrollSize and mp.y <= tree.size.cy:
				tree.downScrollHButton = True
				tree.startScrollH = tree.scrollH
				return
	#判断纵向滚动
	if tree.showVScrollBar:
		contentHeight = getTreeContentHeight(tree)
		if contentHeight > 0 and contentHeight > tree.size.cy:
			sTop = tree.headerHeight + tree.scrollV / contentHeight * (tree.size.cy - tree.headerHeight - tree.scrollSize)
			sBottom = tree.headerHeight + (tree.scrollV + (tree.size.cy - tree.headerHeight - tree.scrollSize)) / contentHeight * (tree.size.cy - tree.headerHeight - tree.scrollSize)
			if sBottom - sTop < tree.scrollSize:
				sBottom = sTop + tree.scrollSize
			if mp.x >= tree.size.cx - tree.scrollSize and mp.x <= tree.size.cx and mp.y >= sTop and mp.y <= sBottom:
				tree.downScrollVButton = True
				tree.startScrollV = tree.scrollV
				return
	if tree.allowDragScroll:
		tree.startScrollH = tree.scrollH
		tree.startScrollV = tree.scrollV
	

#获取总的偏移量
#node:树节点
def getTotalIndent(node):
	if node.parentNode != None:
		return node.indent + getTotalIndent(node.parentNode)
	else:
		return node.indent

#树的鼠标抬起方法
#tree: 树
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks:点击次数
def touchUpTree(tree, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	tree.downScrollHButton = False
	tree.downScrollVButton = False
	tree.hoverScrollHButton = False
	tree.hoverScrollVButton = False
	if tree.paint.cancelClick:
		return
	cLeft = -tree.scrollH
	cTop = -tree.scrollV + tree.headerHeight
	for i in range(0,len(tree.rows)):
		row = tree.rows[i]
		if row.visible:
			if firstPoint.y >= cTop and firstPoint.y <= cTop + tree.rowHeight:
				node = row.cells[0]
				tLeft = cLeft + 2 + getTotalIndent(node)
				wLeft = tLeft
				if tree.showCheckBox:
					wLeft += tree.checkBoxWidth
					if firstPoint.x < wLeft:
						if node.checked:
							checkOrUnCheckTreeNode(node, False)
						else:
							checkOrUnCheckTreeNode(node, True)
						if tree.paint:
							invalidateView(tree)
						break
				if len(node.childNodes) > 0:
					wLeft += tree.collapsedWidth
					if firstPoint.x < wLeft:
						if node.collapsed:
							node.collapsed = False
							hideOrShowTreeNode(node, True)
						else:
							node.collapsed = True
							hideOrShowTreeNode(node, False)
						break
				if tree.onClickTreeNode != None:
					tree.onClickTreeNode(tree, node, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
				elif tree.paint.onClickTreeNode != None:
					tree.paint.onClickTreeNode(tree, node, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
			cTop += tree.rowHeight

#计算直线参数 
#mp:坐标 
#x1:横坐标1 
#y1:纵坐标1 
#x2:横坐标2 
#y2:纵坐标2 
#oX:坐标起始X 
#oY:坐标起始Y
def lineXY(chart, x1, y1, x2, y2, oX, oY):
	chart.kChart = 0
	chart.bChart = 0
	if (x1 - oX) != (x2 - oX):
		chart.kChart = ((y2 - oY) - (y1 - oY)) / ((x2 - oX) - (x1 - oX))
		chart.bChart = (y1 - oY) - chart.kChart * (x1 - oX)

#判断是否选中直线 
#mp:坐标 
#x1:横坐标1 
#y1:纵坐标1 
#x2:横坐标2 
#y2:纵坐标2
def selectLine(chart, mp, x1, y1, x2, y2):
    lineXY(chart, x1, y1, x2, y2, 0, 0)
    if chart.kChart != 0 or chart.bChart != 0:
        if mp.y / (mp.x * chart.kChart + chart.bChart) >= 0.9 and mp.y / (mp.x * chart.kChart + chart.bChart) <= 1.1:
            return True
    else:
        if mp.x >= x1 - chart.plotPointSizeChart and mp.x <= x1 + chart.plotPointSizeChart:
            return True
    return False

#判断是否选中射线 
#mp:坐标 
#x1:横坐标1 
#y1:纵坐标1 
#x2:横坐标2 
#y2:纵坐标2
def selectRay(chart, mp, x1, y1, x2, y2):
	lineXY(chart, x1, y1, x2, y2, 0, 0)
	if chart.kChart != 0 or chart.bChart != 0:
		if mp.y / (mp.x * chart.kChart + chart.bChart) >= 0.9 and mp.y / (mp.x * chart.kChart + chart.bChart) <= 1.1:
			if x1 >= x2:
				if mp.x > x1 + chart.plotPointSizeChart:
					return False
			elif x1 < x2:
				if mp.x < x1 - chart.plotPointSizeChart:
					return False
			return True
	else:
		if mp.x >= x1 - chart.plotPointSizeChart and mp.x <= x1 + chart.plotPointSizeChart:
			if y1 >= y2:
				if mp.y <= y1 - chart.plotPointSizeChart:
					return True
			else:
				if mp.y >= y1 - chart.plotPointSizeChart:
					return True
	return False

#判断是否选中线段 
#mp:坐标 
#x1:横坐标1 
#y1:纵坐标1 
#x2:横坐标2 
#y2:纵坐标2
def selectSegment(chart, mp, x1, y1, x2, y2):
	lineXY(chart, x1, y1, x2, y2, 0, 0)
	smallX = x2
	if x1 <= x2:
		smallX = x1
	smallY = y2
	if y1 <= y2:
		smallY = y1
	bigX = x2
	if x1 > x2:
		bigX = x1
	bigY = y2
	if y1 > y2:
		bigY = y1
	if mp.x >= smallX - 2 and mp.x <= bigX + 2 and mp.y >= smallY - 2 and mp.y <= bigY + 2:
		if chart.kChart != 0 or chart.bChart != 0:
			if mp.y / (mp.x * chart.kChart + chart.bChart) >= 0.9 and mp.y / (mp.x * chart.kChart + chart.bChart) <= 1.1:
				return True
		else:
			if mp.x >= x1 - chart.plotPointSizeChart and mp.x <= x1 + chart.plotPointSizeChart:
				return True
	return False

# 根据三点计算圆心 
#x1:横坐标 
#y1:纵坐标1 
#x2:横坐标2 
#y2:纵坐标2 
#x3:横坐标3 
#y3:纵坐标3
def ellipseOR(chart, x1, y1, x2, y2, x3, y3):
	chart.oXChart = ((y3 - y1) * (y2 * y2 - y1 * y1 + x2 * x2 - x1 * x1) + (y2 - y1) * (y1 * y1 - y3 * y3 + x1 * x1 - x3 * x3)) / (2 * (x2 - x1) * (y3 - y1) - 2 * (x3 - x1) * (y2 - y1))
	chart.oYChart = ((x3 - x1) * (x2 * x2 - x1 * x1 + y2 * y2 - y1 * y1) + (x2 - x1) * (x1 * x1 - x3 * x3 + y1 * y1 - y3 * y3)) / (2 * (y2 - y1) * (x3 - x1) - 2 * (y3 - y1) * (x2 - x1))
	chart.rChart = math.sqrt((x1 - chart.oXChart) * (x1 - chart.oXChart) + (y1 - chart.oYChart) * (y1 - chart.oYChart))

#判断点是否在椭圆上
#x:横坐标 
#y:纵坐标 
#oX:坐标起始X 
#oY:坐标起始Y 
#a:椭圆参数a 
#b:椭圆参数b
def ellipseHasPoint(x, y, oX, oY, a, b):
	x -= oX
	y -= oY
	if a == 0 and b == 0 and x == 0 and y == 0:
		return True
	if a == 0:
		if x == 0 and y >= -b and y <= b:
			return False
	if b == 0:
		if y == 0 and x >= -a and x <= a:
			return True
	if a != 0 and b != 0:
		if (x * x) / (a * a) + (y * y) / (b * b) >= 0.8 and (x * x) / (a * a) + (y * y) / (b * b) <= 1.2:
			return True
	return False

#计算线性回归 
#list:集合
def linearRegressionEquation(chart, list):
	result = 0
	sumX = 0
	sumY = 0
	sumUp = 0
	sumDown = 0
	xAvg = 0
	yAvg = 0
	chart.kChart = 0
	chart.bChart = 0
	length = len(list)
	if length > 1:
		for i in range(0, length):
			sumX += i + 1
			sumY += list[i]
		xAvg = sumX / length
		yAvg = sumY / length
		for i in range(0, length):
			sumUp += (i + 1 - xAvg) * (list[i] - yAvg)
			sumDown += (i + 1 - xAvg) * (i + 1 - xAvg)
		chart.kChart = sumUp / sumDown
		chart.bChart = yAvg - chart.kChart * xAvg
	return result

#计算最大值 
#list:集合
def maxValue(list):
	length = len(list)
	maxValue = 0
	for i in range(0, length):
		if i == 0:
			maxValue = list[i]
		else:
			if maxValue < list[i]:
				maxValue = list[i]
	return maxValue

#计算最小值 
#list:集合
def minValue(list):
    length = len(list)
    minValue = 0
    for i in range(0, length):
        if i == 0:
            minValue = list[i]
        else:
            if minValue > list[i]:
                minValue = list[i]
    return minValue

#计算平均值 
#list:集合
def avgValue(list):
	sumValue = 0
	length = len(list)
	if length > 0:
		for i in range(0, length):
			sumValue += list[i]
		return sumValue / length
	return
	
#计算平行四边形参数 
#x1:横坐标1 
#y1:纵坐标1 
#x2:横坐标2 
#y2:纵坐标2 
#x3:横坐标3 
#y3:纵坐标3
def parallelogram(chart, x1, y1, x2, y2, x3, y3):
	chart.x4Chart = x1 + x3 - x2
	chart.y4Chart = y1 + y3 - y2

#计算斐波那契数列 
#index:索引
def fibonacciValue(index):
	if index < 1:
		return 0
	else:
		vList = []
		for i in range(0, index):
			vList.append(0)
		result = 0
		for i in range(0, index):
			if i == 0 or i == 1:
				vList[i] = 1
			else:
				vList[i] = vList[i - 1] + vList[i - 2]
		result = vList[index - 1]
		return result

# 获取百分比线的刻度 
#y1: 纵坐标1 
#y2: 纵坐标2
def getPercentParams(y1, y2):
	y0 = 0
	y25 = 0
	y50 = 0
	y75 = 0
	y100 = 0
	y0 = y1
	if y1 <= y2:
		y25 = y1 + (y2 - y1) / 4.0
		y50 = y1 + (y2 - y1) / 2.0
		y75 = y1 + (y2 - y1) * 3.0 / 4.0
	else:
		y25 = y2 + (y1 - y2) * 3.0 / 4.0
		y50 = y2 + (y1 - y2) / 2.0
		y75 = y2 + (y1 - y2) / 4.0
	y100 = y2
	list = []
	list.append(y0)
	list.append(y25)
	list.append(y50)
	list.append(y75)
	list.append(y100)
	return list

#根据坐标计算矩形
#x1:横坐标1
#y1:纵坐标1
#x2:横坐标2
#y2:纵坐标2
def rectangleXYWH(chart, x1, y1, x2, y2):
	chart.xChart = x2
	if x1 < x2:
		chart.xChart = x1
	chart.yChart = y2
	if y1 < y2:
		chart.yChart = y1
	chart.wChart = abs(x1 - x2)
	chart.hChart = abs(y1 - y2)
	if chart.wChart <= 0:
		chart.wChart = 4
	if chart.hChart <= 0:
		chart.hChart = 4


#根据位置计算索引
#chart:图表
#mp:坐标
def getChartIndex(chart, mp):
	if chart.data != None and len(chart.data) == 0:
		return -1
	if mp.x <= 0:
		return 0
	intX = int(mp.x - chart.leftVScaleWidth - chart.hScalePixel - chart.offsetX)
	if intX < 0:
		intX = 0
	index = int(chart.firstVisibleIndex + intX / chart.hScalePixel)
	if intX % chart.hScalePixel != 0:
		index = index + 1
	if index < 0:
		index = 0
	elif chart.data and index > len(chart.data) - 1:
		index = len(chart.data) - 1
	return index

#获取最大显示记录条数
#chart:图表
#hScalePixel:间隔
#pureH:横向距离
def getChartMaxVisibleCount(chart, hScalePixel, pureH):
    count = int((pureH - hScalePixel) / hScalePixel)
    if count < 0:
        count = 0
    return count

#获取图表层的高度
#chart:图表
def getCandleDivHeight(chart):
	height = chart.size.cy - chart.hScaleHeight
	if height > 0:
		return height * chart.candleDivPercent
	else:
		return 0

#获取成交量层的高度
#chart:图表
def getVolDivHeight(chart):
	height = chart.size.cy - chart.hScaleHeight
	if height > 0:
		return height * chart.volDivPercent
	else:
		return 0

#获取指标层的高度
#chart:图表
def getIndDivHeight(chart):
	height = chart.size.cy - chart.hScaleHeight
	if height > 0:
		return height * chart.indDivPercent
	else:
		return 0

#获取指标层2的高度
#chart:图表
def getIndDivHeight2(chart):
	height = chart.size.cy - chart.hScaleHeight
	if height > 0:
		return height * chart.indDivPercent2
	else:
		return 0

#获取横向工作区
#chart:图表
def getChartWorkAreaWidth(chart):
    return chart.size.cx - chart.leftVScaleWidth - chart.rightVScaleWidth - chart.rightSpace - chart.offsetX

#根据索引获取横坐标
#chart:图表
#index:索引
def getChartX(chart, index):
    return chart.leftVScaleWidth + (index - chart.firstVisibleIndex) * chart.hScalePixel + chart.hScalePixel / 2 + chart.offsetX

#根据日期获取索引
#chart:图表
#date:日期
def getChartIndexByDate(chart, date):
	index = -1
	for i in range(0, len(chart.data)):
		if chart.data[i].date == date:
			index = i
			break
	return index

#根据索引获取日期
#chart:图表
#index:索引
def getChartDateByIndex(chart, index):
    date = ""
    if index >= 0 and index < len(chart.data):
        date = chart.data[index].date
    return date

#检查最后可见索引
#chart:图表
def checkChartLastVisibleIndex(chart):
    dataCount = len(chart.data)
    workingAreaWidth = getChartWorkAreaWidth(chart)
    maxVisibleRecord = getChartMaxVisibleCount(chart, chart.hScalePixel, workingAreaWidth)
    if chart.firstVisibleIndex < 0:
        chart.firstVisibleIndex = 0
    if chart.lastVisibleIndex >= chart.firstVisibleIndex + maxVisibleRecord - 1 or chart.lastVisibleIndex < dataCount - 1:
        chart.lastVisibleIndex = chart.firstVisibleIndex + maxVisibleRecord - 1
    if chart.lastVisibleIndex > dataCount - 1:
        chart.lastVisibleIndex = dataCount - 1
    if len(chart.data) > 0 and chart.lastVisibleIndex != -1:
        chart.lastVisibleKey = chart.data[chart.lastVisibleIndex].date
        if chart.lastVisibleIndex == len(chart.data) - 1:
            chart.lastRecordIsVisible = True
        else:
            chart.lastRecordIsVisible = False
    else:
        chart.lastVisibleKey = 0
        chart.lastRecordIsVisible = True

#自动设置首先可见和最后可见的记录号
#chart:图表
def resetChartVisibleRecord(chart):
    rowsCount = len(chart.data)
    workingAreaWidth = getChartWorkAreaWidth(chart)
    if chart.autoFillHScale:
        if workingAreaWidth > 0 and rowsCount > 0:
            chart.hScalePixel = workingAreaWidth / rowsCount
            chart.firstVisibleIndex = 0
            chart.lastVisibleIndex = rowsCount - 1
    else:
        maxVisibleRecord = getChartMaxVisibleCount(chart, chart.hScalePixel, workingAreaWidth)
        if rowsCount == 0:
            chart.firstVisibleIndex = -1
            chart.lastVisibleIndex = -1
        else:
            if rowsCount < maxVisibleRecord:
                chart.lastVisibleIndex = rowsCount - 1
                chart.firstVisibleIndex = 0
            else:
                if chart.firstVisibleIndex != -1 and chart.lastVisibleIndex != -1 and chart.lastRecordIsVisible == False:
                    index = getChartIndexByDate(chart, chart.lastVisibleKey)
                    if index != -1:
                        chart.lastVisibleIndex = index
                    chart.firstVisibleIndex = chart.lastVisibleIndex - maxVisibleRecord + 1
                    if chart.firstVisibleIndex < 0:
                        chart.firstVisibleIndex = 0
                        chart.lastVisibleIndex = chart.firstVisibleIndex + maxVisibleRecord
                        checkChartLastVisibleIndex(chart)
                else:
                    chart.lastVisibleIndex = rowsCount - 1
                    chart.firstVisibleIndex = chart.lastVisibleIndex - maxVisibleRecord + 1
                    if chart.firstVisibleIndex > chart.lastVisibleIndex:
                        chart.firstVisibleIndex = chart.lastVisibleIndex

#设置可见索引
#chart:图表
#firstVisibleIndex:起始索引
#lastVisibleIndex:结束索引
def setChartVisibleIndex(chart, firstVisibleIndex, lastVisibleIndex):
    xScalePixel = getChartWorkAreaWidth(chart) / (lastVisibleIndex - firstVisibleIndex + 1)
    if xScalePixel < 1000000:
        chart.firstVisibleIndex = firstVisibleIndex
        chart.lastVisibleIndex = lastVisibleIndex
        if lastVisibleIndex != len(chart.data) - 1:
            chart.lastRecordIsVisible = False
        else:
            chart.lastRecordIsVisible = True
        chart.hScalePixel = xScalePixel
        checkChartLastVisibleIndex(chart)

#计算数值在层中的位置
#chart:图表
#divIndex:所在层
#chart:数值
def getChartY(chart, divIndex, value):
	if divIndex == 0:
		if chart.candleMax > chart.candleMin:
			cValue = value
			cMax = chart.candleMax
			cMin = chart.candleMin
			if chart.vScaleType != "standard":
				if cValue > 0:
					cValue = math.log10(cValue)
				elif cValue < 0:
					cValue = -math.log10(abs(cValue))
				if cMax > 0:
					cMax = math.log10(cMax)
				elif cMax < 0:
					cMax = -math.log10(abs(cMax))
				if cMin > 0:
					cMin = math.log10(cMin)
				elif cMin < 0:
					cMin = -math.log10(abs(cMin))
			rate = (cValue - cMin) / (cMax - cMin)
			divHeight = getCandleDivHeight(chart)
			return divHeight - chart.candlePaddingBottom - (divHeight - chart.candlePaddingTop - chart.candlePaddingBottom) * rate
		else:
			return 0
	elif divIndex == 1:
		if chart.volMax > chart.volMin:
			rate = (value - chart.volMin) / (chart.volMax - chart.volMin)
			candleHeight = getCandleDivHeight(chart)
			volHeight = getVolDivHeight(chart)
			return candleHeight + volHeight - chart.volPaddingBottom - (volHeight - chart.volPaddingTop - chart.volPaddingBottom) * rate
		else:
			return 0
	elif divIndex == 2:
		if chart.indMax > chart.indMin:
			rate = (value - chart.indMin) / (chart.indMax - chart.indMin)
			candleHeight = getCandleDivHeight(chart)
			volHeight = getVolDivHeight(chart)
			indHeight = getIndDivHeight(chart)
			return candleHeight + volHeight + indHeight - chart.indPaddingBottom - (indHeight - chart.indPaddingTop - chart.indPaddingBottom) * rate
		else:	
			return 0
	elif divIndex == 3:
		if chart.indMax2 > chart.indMin2:
			rate = (value - chart.indMin2) / (chart.indMax2 - chart.indMin2)
			candleHeight = getCandleDivHeight(chart)
			volHeight = getVolDivHeight(chart)
			indHeight = getIndDivHeight(chart)
			indHeight2 = getIndDivHeight2(chart)
			return candleHeight + volHeight + indHeight + indHeight2- chart.indPaddingBottom2 - (indHeight2 - chart.indPaddingTop2 - chart.indPaddingBottom2) * rate
		else:	
			return 0
	return 0

#计算数值在层中右轴的位置
#chart:图表
#divIndex:所在层
#chart:数值
def getChartYInRight(chart, divIndex, value):
	if divIndex == 0:
		if chart.candleMaxRight > chart.candleMinRight:
			cValue = value
			cMax = chart.candleMaxRight
			cMin = chart.candleMinRight
			if chart.vScaleType != "standard":
				if cValue > 0:
					cValue = math.log10(cValue)
				elif cValue < 0:
					cValue = -math.log10(abs(cValue))
				if cMax > 0:
					cMax = math.log10(cMax)
				elif cMax < 0:
					cMax = -math.log10(abs(cMax))
				if cMin > 0:
					cMin = math.log10(cMin)
				elif cMin < 0:
					cMin = -math.log10(abs(cMin))
			rate = (cValue - cMin) / (cMax - cMin)
			divHeight = getCandleDivHeight(chart)
			return divHeight - chart.candlePaddingBottom - (divHeight - chart.candlePaddingTop - chart.candlePaddingBottom) * rate
		else:
			return 0
	elif divIndex == 1:
		if chart.volMaxRight > chart.volMinRight:
			rate = (value - chart.volMinRight) / (chart.volMaxRight - chart.volMinRight)
			candleHeight = getCandleDivHeight(chart)
			volHeight = getVolDivHeight(chart)
			return candleHeight + volHeight - chart.volPaddingBottom - (volHeight - chart.volPaddingTop - chart.volPaddingBottom) * rate
		else:
			return 0
	elif divIndex == 2:
		if chart.indMaxRight > chart.indMinRight:
			rate = (value - chart.indMinRight) / (chart.indMaxRight - chart.indMinRight)
			candleHeight = getCandleDivHeight(chart)
			volHeight = getVolDivHeight(chart)
			indHeight = getIndDivHeight(chart)
			return candleHeight + volHeight + indHeight - chart.indPaddingBottom - (indHeight - chart.indPaddingTop - chart.indPaddingBottom) * rate
		else:	
			return 0
	elif divIndex == 3:
		if chart.indMax2Right > chart.indMin2Right:
			rate = (value - chart.indMin2Right) / (chart.indMax2Right - chart.indMin2Right)
			candleHeight = getCandleDivHeight(chart)
			volHeight = getVolDivHeight(chart)
			indHeight = getIndDivHeight(chart)
			indHeight2 = getIndDivHeight2(chart)
			return candleHeight + volHeight + indHeight + indHeight2- chart.indPaddingBottom2 - (indHeight2 - chart.indPaddingTop2 - chart.indPaddingBottom2) * rate
		else:	
			return 0
	return 0


#根据坐标获取对应的值
#chart:图表
#point:坐标
def getChartValue(chart, point):
	candleHeight = getCandleDivHeight(chart)
	volHeight = getVolDivHeight(chart)
	indHeight = getIndDivHeight(chart)
	indHeight2 = getIndDivHeight2(chart)
	if point.y <= candleHeight:
		if candleHeight - chart.candlePaddingTop - chart.candlePaddingBottom > 0:
			rate = (candleHeight - chart.candlePaddingBottom - point.y) / (candleHeight - chart.candlePaddingTop - chart.candlePaddingBottom)
			cMin = chart.candleMin
			cMax = chart.candleMax
			if chart.vScaleType != "standard":
				if cMax > 0:
					cMax = math.log10(cMax)
				elif cMax < 0:
					cMax = -math.log10(abs(cMax))
				if cMin > 0:
					cMin = math.log10(cMin)
				elif cMin < 0:
					cMin = -math.log10(abs(cMin))
			result = cMin + (cMax - cMin) * rate
			if chart.vScaleType != "standard":
				return pow(10, result)
			else:
				return result
	elif point.y > candleHeight and point.y <= candleHeight + volHeight:
		if volHeight - chart.volPaddingTop - chart.volPaddingBottom > 0:
			rate = (volHeight - chart.volPaddingBottom - (point.y - candleHeight)) / (volHeight - chart.volPaddingTop - chart.volPaddingBottom)
			return chart.volMin + (chart.volMax - chart.volMin) * rate
	elif point.y > candleHeight + volHeight and point.y <= candleHeight + volHeight + indHeight:
		if indHeight - chart.indPaddingTop - chart.indPaddingBottom > 0:
			rate = (indHeight - chart.indPaddingBottom - (point.y - candleHeight - volHeight)) / (indHeight - chart.indPaddingTop - chart.indPaddingBottom)
			return chart.indMin + (chart.indMax - chart.indMin) * rate
	elif point.y > candleHeight + volHeight + indHeight and point.y <= candleHeight + volHeight + indHeight + indHeight2:
		if indHeight2 - chart.indPaddingTop2 - chart.indPaddingBottom2 > 0:
			rate = (indHeight2 - chart.indPaddingBottom2 - (point.y - candleHeight - volHeight - indHeight)) / (indHeight2 - chart.indPaddingTop2 - chart.indPaddingBottom2)
			return chart.indMin2 + (chart.indMax2 - chart.indMin2) * rate
	return 0

#根据坐标获取图表层对应的值
#chart:图表
#point:坐标
def getCandleDivValue(chart, point):
	candleHeight = getCandleDivHeight(chart)
	rate = 0
	if candleHeight - chart.candlePaddingTop - chart.candlePaddingBottom > 0:
		rate = (candleHeight - chart.candlePaddingBottom - point.y) / (candleHeight - chart.candlePaddingTop - chart.candlePaddingBottom)
	cMin = chart.candleMin
	cMax = chart.candleMax
	if chart.vScaleType != "standard":
		if cMax > 0:
			cMax = math.log10(cMax)
		elif cMax < 0:
			cMax = -math.log10(abs(cMax))
		if cMin > 0:
			cMin = math.log10(cMin)
		elif cMin < 0:
			cMin = -math.log10(abs(cMin))
	result = cMin + (cMax - cMin) * rate
	if chart.vScaleType != "standard":
		return pow(10, result)
	else:
		return result

#清除缓存数据方法
#chart:图表
def clearDataArr(chart):
	chart.closearr = []
	chart.allema12 = []
	chart.allema26 = []
	chart.alldifarr = []
	chart.alldeaarr = []
	chart.allmacdarr = []
	chart.boll_mid = []
	chart.boll_up = []
	chart.boll_down = []
	chart.bias1 = []
	chart.bias2 = []
	chart.bias3 = []
	chart.dma1 = []
	chart.dma2 = []
	chart.kdj_k = []
	chart.kdj_d = []
	chart.kdj_j = []
	chart.bbi = []
	chart.roc = []
	chart.roc_ma = []
	chart.rsi1 = []
	chart.rsi2 = []
	chart.rsi3 = []
	chart.wr1 = []
	chart.wr2 = []
	chart.trix = []
	chart.trix_ma = []
	chart.cci = []

#获取数据
#chart:图表
def calcChartIndicator(chart):
	clearDataArr(chart)
	closeArr = []
	highArr = []
	lowArr = []
	if chart.data != None and len(chart.data) > 0:
		for i in range(0,len(chart.data)):
			chart.closearr.append(chart.data[i].close)
			closeArr.append(chart.data[i].close)
			highArr.append(chart.data[i].high)
			lowArr.append(chart.data[i].low)
	if chart.mainIndicator == "MA":
		chart.ma5 = MA(closeArr, 5)
		chart.ma10 = MA(closeArr, 10)
		chart.ma20 = MA(closeArr, 20)
		chart.ma30 = MA(closeArr, 30)
		chart.ma120 = MA(closeArr, 120)
		chart.ma250 = MA(closeArr, 250)
	elif chart.mainIndicator == "BOLL":
		getBollData(closeArr, 20, chart.boll_up, chart.boll_mid, chart.boll_down)
	if chart.showIndicator == "MACD":
		chart.allema12.append(chart.closearr[0])
		chart.allema26.append(chart.closearr[0])
		chart.alldeaarr.append(0)
		for i in range(1,len(chart.closearr)):
			chart.allema12.append(getEMA(12, chart.closearr[i], chart.allema12[i - 1]))
			chart.allema26.append(getEMA(26, chart.closearr[i], chart.allema26[i - 1]))
		chart.alldifarr = getDIF(chart.allema12, chart.allema26)
		for i in range(1,len(chart.alldifarr)):
			chart.alldeaarr.append(chart.alldeaarr[i - 1] * 8 / 10 + chart.alldifarr[i] * 2 / 10)
		chart.allmacdarr = getMACD(chart.alldifarr, chart.alldeaarr)
	elif chart.showIndicator == "BIAS":
		getBIASData(chart.closearr, 6, 12, 24, chart.bias1, chart.bias2, chart.bias3)
	elif chart.showIndicator == "TRIX":
		getTRIXData(chart.closearr, 10, 50, chart.trix, chart.trix_ma)
	elif chart.showIndicator == "CCI":
		getCCIData(closeArr, highArr, lowArr, 14, chart.cci)
	elif chart.showIndicator == "BBI":
		getBBIData(closeArr, 3, 6, 12, 24, chart.bbi)
	elif chart.showIndicator == "ROC":
		getRocData(closeArr, 12, 6, chart.roc, chart.roc_ma)
	elif chart.showIndicator == "WR":
		getWRData(closeArr, highArr, lowArr, 5, 10, chart.wr1, chart.wr2)
	elif chart.showIndicator == "DMA":
		getDMAData(closeArr, 10, 50, chart.dma1, chart.dma2)
	elif chart.showIndicator == "RSI":
		getRSIData(closeArr, 6, 12, 24, chart.rsi1, chart.rsi2, chart.rsi3)
	elif chart.showIndicator == "KDJ":
		getKDJData(chart, highArr, lowArr, closeArr, 9, 3, 3, chart.kdj_k, chart.kdj_d, chart.kdj_j)
	if chart.onCalculateChartMaxMin != None:
		chart.onCalculateChartMaxMin(chart)
	elif chart.paint.onCalculateChartMaxMin != None:
		chart.paint.onCalculateChartMaxMin(chart)
	else:
		calculateChartMaxMin(chart)

#计算最大最小值
#chart:图表
def calculateChartMaxMin(chart):
	chart.candleMax = 0
	chart.candleMin = 0
	chart.volMax = 0
	chart.volMin = 0
	chart.indMin = 0
	chart.indMin = 0
	isTrend = False
	if chart.cycle == "trend":
		isTrend = True
	firstOpen = chart.firstOpen
	load1 = False
	load2 = False
	load3 = False
	load4 = False
	if chart.data != None and len(chart.data) > 0:
		lastValidIndex = chart.lastVisibleIndex
		if chart.lastValidIndex != -1:
			lastValidIndex = chart.lastValidIndex
		for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
			if i == chart.firstVisibleIndex:
				if isTrend:
					chart.candleMax = chart.data[i].close
					chart.candleMin = chart.data[i].close
					if firstOpen == 0:
						firstOpen = chart.data[i].close
				else:
					chart.candleMax = chart.data[i].high
					chart.candleMin = chart.data[i].low
				load1 = True
				load2 = True
				chart.volMax = chart.data[i].volume
				if chart.showIndicator == "MACD":
					chart.indMax = chart.alldifarr[i]
					chart.indMin = chart.alldifarr[i]
					load3 = True
				elif chart.showIndicator == "KDJ":
					chart.indMax = chart.kdj_k[i]
					chart.indMin = chart.kdj_k[i]
					load3 = True
				elif chart.showIndicator == "RSI":
					chart.indMax = chart.rsi1[i]
					chart.indMin = chart.rsi1[i]
					load3 = True
				elif chart.showIndicator == "BIAS":
					chart.indMax = chart.bias1[i]
					chart.indMin = chart.bias1[i]
					load3 = True
				elif chart.showIndicator == "ROC":
					chart.indMax = chart.roc[i]
					chart.indMin = chart.roc[i]
					load3 = True
				elif chart.showIndicator == "WR":
					chart.indMax = chart.wr1[i]
					chart.indMin = chart.wr1[i]
					load3 = True
				elif chart.showIndicator == "CCI":
					chart.indMax = chart.cci[i]
					chart.indMin = chart.cci[i]
					load3 = True
				elif chart.showIndicator == "BBI":
					chart.indMax = chart.bbi[i]
					chart.indMin = chart.bbi[i]
					load3 = True
				elif chart.showIndicator == "TRIX":
					chart.indMax = chart.trix[i]
					chart.indMin = chart.trix[i]
					load3 = True
				elif chart.showIndicator == "DMA":
					chart.indMax = chart.dma1[i]
					chart.indMin = chart.dma1[i]
					load3 = True
			else:
				if isTrend:
					if chart.candleMax < chart.data[i].close:
						chart.candleMax = chart.data[i].close
					if chart.candleMin > chart.data[i].close:
						chart.candleMin = chart.data[i].close
				else:
					if chart.candleMax < chart.data[i].high:
						chart.candleMax = chart.data[i].high
					if chart.candleMin > chart.data[i].low:
						chart.candleMin = chart.data[i].low
				if chart.volMax < chart.data[i].volume:
					chart.volMax = chart.data[i].volume
				if chart.showIndicator == "MACD":
					if chart.indMax < chart.alldifarr[i]:
						chart.indMax = chart.alldifarr[i]
					if chart.indMax < chart.alldeaarr[i]:
						chart.indMax = chart.alldeaarr[i]
					if chart.indMax < chart.allmacdarr[i]:
						chart.indMax = chart.allmacdarr[i]
					if chart.indMin > chart.alldifarr[i]:
						chart.indMin = chart.alldifarr[i]
					if chart.indMin > chart.alldeaarr[i]:
						chart.indMin = chart.alldeaarr[i]
					if chart.indMin > chart.allmacdarr[i]:
						chart.indMin = chart.allmacdarr[i]
				elif chart.showIndicator == "KDJ":
					if chart.indMax < chart.kdj_k[i]:
						chart.indMax = chart.kdj_k[i]
					if chart.indMax < chart.kdj_d[i]:
						chart.indMax = chart.kdj_d[i]
					if chart.indMax < chart.kdj_j[i]:
						chart.indMax = chart.kdj_j[i]
					if chart.indMin > chart.kdj_k[i]:
						chart.indMin = chart.kdj_k[i]
					if chart.indMin > chart.kdj_d[i]:
						chart.indMin = chart.kdj_d[i]
					if chart.indMin > chart.kdj_j[i]:
						chart.indMin = chart.kdj_j[i]
				elif chart.showIndicator == "RSI":
					if chart.indMax < chart.rsi1[i]:
						chart.indMax = chart.rsi1[i]
					if chart.indMax < chart.rsi2[i]:
						chart.indMax = chart.rsi2[i]
					if chart.indMax < chart.rsi3[i]:
						chart.indMax = chart.rsi3[i]
					if chart.indMin > chart.rsi1[i]:
						chart.indMin = chart.rsi1[i]
					if chart.indMin > chart.rsi2[i]:
						chart.indMin = chart.rsi2[i]
					if chart.indMin > chart.rsi3[i]:
						chart.indMin = chart.rsi3[i]
				elif chart.showIndicator == "BIAS":
					if chart.indMax < chart.bias1[i]:
						chart.indMax = chart.bias1[i]
					if chart.indMax < chart.bias2[i]:
						chart.indMax = chart.bias2[i]
					if chart.indMax < chart.bias3[i]:
						chart.indMax = chart.bias3[i]
					if chart.indMin > chart.bias1[i]:
						chart.indMin = chart.bias1[i]
					if chart.indMin > chart.bias2[i]:
						chart.indMin = chart.bias2[i]
					if chart.indMin > chart.bias3[i]:
						chart.indMin = chart.bias3[i]
				elif chart.showIndicator == "ROC":
					if chart.indMax < chart.roc[i]:
						chart.indMax = chart.roc[i]
					if chart.indMax < chart.roc_ma[i]:
						chart.indMax = chart.roc_ma[i]
					if chart.indMin > chart.roc[i]:
						chart.indMin = chart.roc[i]
					if chart.indMin > chart.roc_ma[i]:
						chart.indMin = chart.roc_ma[i]
				elif chart.showIndicator == "WR":
					if chart.indMax < chart.wr1[i]:
						chart.indMax = chart.wr1[i]
					if chart.indMax < chart.wr2[i]:
						chart.indMax = chart.wr2[i]
					if chart.indMin > chart.wr1[i]:
						chart.indMin = chart.wr1[i]
					if chart.indMin > chart.wr2[i]:
						chart.indMin = chart.wr2[i]
				elif chart.showIndicator == "CCI":
					if chart.indMax < chart.cci[i]:
						chart.indMax = chart.cci[i]
					if chart.indMin > chart.cci[i]:
						chart.indMin = chart.cci[i]
				elif chart.showIndicator == "BBI":
					if chart.indMax < chart.bbi[i]:
						chart.indMax = chart.bbi[i]
					if chart.indMin > chart.bbi[i]:
						chart.indMin = chart.bbi[i]
				elif chart.showIndicator == "TRIX":
					if chart.indMax < chart.trix[i]:
						chart.indMax = chart.trix[i]
					if chart.indMax < chart.trix_ma[i]:
						chart.indMax = chart.trix_ma[i]
					if chart.indMin > chart.trix[i]:
						chart.indMin = chart.trix[i]
					if chart.indMin > chart.trix_ma[i]:
						chart.indMin = chart.trix_ma[i]
				elif chart.showIndicator == "DMA":
					if chart.indMax < chart.dma1[i]:
						chart.indMax = chart.dma1[i]
					if chart.indMax < chart.dma2[i]:
						chart.indMax = chart.dma2[i]
					if chart.indMin > chart.dma1[i]:
						chart.indMin = chart.dma1[i]
					if chart.indMin > chart.dma2[i]:
						chart.indMin = chart.dma2[i]
	if len(chart.shapes) > 0:
		lastValidIndex = chart.lastVisibleIndex
		if chart.lastValidIndex != -1:
			lastValidIndex = chart.lastValidIndex
		for s in range(0, len(chart.shapes)):
			shape = chart.shapes[s]
			if len(shape.datas) > 0:
				for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
					if shape.divIndex == 0:
						if load1 == False and i == chart.firstVisibleIndex:
							if shape.leftOrRight:
								chart.candleMax = shape.datas[i]
								chart.candleMin = shape.datas[i]
							else:
								chart.candleMaxRight = shape.datas[i]
								chart.candleMinRight = shape.datas[i]
							load1 = True
						else:
							if shape.leftOrRight:
								if shape.datas[i] > chart.candleMax:
									chart.candleMax = shape.datas[i]
								if shape.datas[i] < chart.candleMin:
									chart.candleMin = shape.datas[i]
							else:
								if shape.datas[i] > chart.candleMaxRight:
									chart.candleMaxRight = shape.datas[i]
								if shape.datas[i] < chart.candleMinRight:
									chart.candleMinRight = shape.datas[i]
					elif shape.divIndex == 1:
						if load2 == False and i == chart.firstVisibleIndex:
							if shape.leftOrRight:
								chart.volMax = shape.datas[i]
								chart.volMin = shape.datas[i]
							else:
								chart.volMaxRight = shape.datas[i]
								chart.volMinRight = shape.datas[i]
							load2 = True
						else:
							if shape.leftOrRight:
								if shape.datas[i] > chart.volMax:
									chart.volMax = shape.datas[i]
								if shape.datas[i] < chart.volMin:
									chart.volMin = shape.datas[i]
							else:
								if shape.datas[i] > chart.volMaxRight:
									chart.volMaxRight = shape.datas[i]
								if shape.datas[i] < chart.volMinRight:
									chart.volMinRight = shape.datas[i]
					elif shape.divIndex == 2:
						if load3 == False and i == chart.firstVisibleIndex:
							if shape.leftOrRight:
								chart.indMax = shape.datas[i]
								chart.indMin = shape.datas[i]
							else:
								chart.indMaxRight = shape.datas[i]
								chart.indMinRight = shape.datas[i]
							load3 = True
						else:
							if shape.leftOrRight:
								if shape.datas[i] > chart.indMax:
									chart.indMax = shape.datas[i]
								if shape.datas[i] < chart.indMin:
									chart.indMin = shape.datas[i]
							else:
								if shape.datas[i] > chart.indMaxRight:
									chart.indMaxRight = shape.datas[i]
								if shape.datas[i] < chart.indMinRight:
									chart.indMinRight = shape.datas[i]
					elif shape.divIndex == 3:
						if load4 == False and i == chart.firstVisibleIndex:
							if shape.leftOrRight:
								chart.indMax2 = shape.datas[i]
								chart.indMin2 = shape.datas[i]
							else:
								chart.indMax2Right = shape.datas[i]
								chart.indMin2Right = shape.datas[i]
							load4 = True
						else:
							if shape.leftOrRight:
								if shape.datas[i] > chart.indMax2:
									chart.indMax2 = shape.datas[i]
								if shape.datas[i] < chart.indMin2:
									chart.indMin2 = shape.datas[i]
							else:
								if shape.datas[i] > chart.indMax2Right:
									chart.indMax2Right = shape.datas[i]
								if shape.datas[i] < chart.indMin2Right:
									chart.indMin2Right = shape.datas[i]
			if len(shape.datas2) > 0:
				for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
					if shape.divIndex == 0:
						if shape.leftOrRight:
							if shape.datas2[i] > chart.candleMax:
								chart.candleMax = shape.datas2[i]
							if shape.datas2[i] < chart.candleMin:
								chart.candleMin = shape.datas2[i]
						else:
							if shape.datas2[i] > chart.candleMaxRight:
								chart.candleMaxRight = shape.datas2[i]
							if shape.datas2[i] < chart.candleMinRight:
								chart.candleMinRight = shape.datas2[i]
					elif shape.divIndex == 1:
						if shape.leftOrRight:
							if shape.datas2[i] > chart.volMax:
								chart.volMax = shape.datas2[i]
							if shape.datas2[i] < chart.volMin:
								chart.volMin = shape.datas2[i]
						else:
							if shape.datas2[i] > chart.volMaxRight:
								chart.volMaxRight = shape.datas2[i]
							if shape.datas2[i] < chart.volMinRight:
								chart.volMinRight = shape.datas2[i]
					elif shape.divIndex == 2:
						if shape.leftOrRight:
							if shape.datas2[i] > chart.indMax:
								chart.indMax = shape.datas2[i]
							if shape.datas2[i] < chart.indMin:
								chart.indMin = shape.datas2[i]
						else:
							if shape.datas2[i] > chart.indMaxRight:
								chart.indMaxRight = shape.datas2[i]
							if shape.datas2[i] < chart.indMinRight:
								chart.indMinRight = shape.datas2[i]
					elif shape.divIndex == 3:
						if shape.leftOrRight:
							if shape.datas2[i] > chart.indMax2:
								chart.indMax2 = shape.datas2[i]
							if shape.datas2[i] < chart.indMin2:
								chart.indMin2 = shape.datas2[i]
						else:
							if shape.datas2[i] > chart.indMax2Right:
								chart.indMax2Right = shape.datas2[i]
							if shape.datas2[i] < chart.indMin2Right:
								chart.indMin2Right = shape.datas2[i]
					
	if isTrend:
		subMax = max(abs(chart.candleMax - firstOpen), abs(chart.candleMin - firstOpen))
		chart.candleMax = firstOpen + subMax
		chart.candleMin = firstOpen - subMax
	else:
		if chart.candleMax == 0 and chart.candleMin == 0:
			chart.candleMax = 1
			chart.candleMin = -1
		if chart.volMax == 0 and chart.volMin == 0:
			chart.volMax = 1
			chart.volMin = -1
		if chart.indMax == 0 and chart.indMin == 0:
			chart.indMax = 1
			chart.indMin = -1
		if chart.indMax2 == 0 and chart.indMin2 == 0:
			chart.indMax2 = 1
			chart.indMin2 = -1
		if chart.candleMaxRight == 0 and chart.candleMinRight == 0:
			chart.candleMaxRight = 1
			chart.candleMinRight = -1
		if chart.volMaxRight == 0 and chart.volMinRight == 0:
			chart.volMaxRight = 1
			chart.volMinRight = -1
		if chart.indMaxRight == 0 and chart.indMinRight == 0:
			chart.indMaxRight = 1
			chart.indMinRight = -1
		if chart.indMax2Right == 0 and chart.indMin2Right == 0:
			chart.indMax2Right = 1
			chart.indMin2Right = -1

#缩小
#chart:图表
def zoomOutChart(chart):
	if chart.autoFillHScale == False:
		hScalePixel = chart.hScalePixel
		oldX = getChartX(chart, chart.crossStopIndex)
		if chart.showCrossLine and chart.targetOldX == 0:
			chart.targetOldX = oldX
		pureH = getChartWorkAreaWidth(chart)
		oriMax = -1
		maxValue = -1
		deal = 0
		dataCount = len(chart.data)
		findex = chart.firstVisibleIndex
		lindex = chart.lastVisibleIndex
		if hScalePixel < pureH:
			oriMax = getChartMaxVisibleCount(chart, hScalePixel, pureH)
			if dataCount < oriMax:
				deal = 1
			if hScalePixel > 3:
				hScalePixel += 1
			else:
				if hScalePixel == 1:
					hScalePixel = 2
				else:
					hScalePixel = hScalePixel * 1.5
					if hScalePixel > 3:
						hScalePixel = int(hScalePixel)
			maxValue = getChartMaxVisibleCount(chart, hScalePixel, pureH)
			if dataCount >= maxValue:
				if deal == 1:
					lindex = dataCount - 1
				findex = lindex - maxValue + 1
				if findex < 0:
					findex = 0
		chart.hScalePixel = hScalePixel
		if chart.showCrossLine:
			sX = chart.targetOldX
			findex = chart.crossStopIndex
			while sX >= chart.leftVScaleWidth + chart.hScalePixel / 2:
				findex = findex - 1
				chart.offsetX = sX - chart.leftVScaleWidth - chart.hScalePixel / 2
				sX = sX - chart.hScalePixel
			findex = findex + 1
		chart.firstVisibleIndex = findex
		chart.lastVisibleIndex = lindex
		checkChartLastVisibleIndex(chart)
		if chart.onCalculateChartMaxMin != None:
			chart.onCalculateChartMaxMin(chart)
		elif chart.paint.onCalculateChartMaxMin != None:
			chart.paint.onCalculateChartMaxMin(chart)
		else:
			calculateChartMaxMin(chart)

#放大
#chart:图表
def zoomInChart(chart):
	if chart.autoFillHScale == False:
		hScalePixel = chart.hScalePixel
		oldX = getChartX(chart, chart.crossStopIndex)
		if chart.showCrossLine and chart.targetOldX2 == 0:
			chart.targetOldX2 = oldX
		pureH = getChartWorkAreaWidth(chart)
		maxValue = -1
		dataCount = len(chart.data)
		maxCount = getChartMaxVisibleCount(chart, hScalePixel, pureH)
		if maxCount > dataCount and hScalePixel < 1:
			return
		findex = chart.firstVisibleIndex
		lindex = chart.lastVisibleIndex
		if hScalePixel > 3:
			hScalePixel -= 1
		else:
			hScalePixel = hScalePixel * 2 / 3
			if hScalePixel > 3:
				hScalePixel = int(hScalePixel)
		maxValue = getChartMaxVisibleCount(chart, hScalePixel, pureH)
		if maxValue >= dataCount:
			if hScalePixel < 1:
				hScalePixel = pureH / maxValue
			findex = 0
			lindex = dataCount - 1
		else:
			findex = lindex - maxValue + 1
			if findex < 0:
				findex = 0
		chart.hScalePixel = hScalePixel
		if chart.showCrossLine:
			sX = chart.targetOldX2
			findex = chart.crossStopIndex
			while sX >= chart.leftVScaleWidth + chart.hScalePixel / 2:
				findex = findex - 1
				chart.offsetX = sX - chart.leftVScaleWidth - chart.hScalePixel / 2
				sX = sX - chart.hScalePixel
			findex = findex + 1
		chart.firstVisibleIndex = findex
		chart.lastVisibleIndex = lindex
		checkChartLastVisibleIndex(chart)
		if chart.onCalculateChartMaxMin != None:
			chart.onCalculateChartMaxMin(chart)
		elif chart.paint.onCalculateChartMaxMin != None:
			chart.paint.onCalculateChartMaxMin(chart)
		else:
			calculateChartMaxMin(chart)

#计算坐标轴
#min:最小值
#max:最大值
#yLen:长度
#maxSpan:最大间隔
#minSpan:最小间隔
#defCount:数量
def chartGridScale(chart, minValue, maxValue, yLen, maxSpan, minSpan, defCount):
	if defCount > 0 and maxSpan > 0 and minSpan > 0:
		sub = maxValue - minValue
		nMinCount = int(math.ceil(yLen / maxSpan))
		nMaxCount = int(math.floor(yLen / minSpan))
		nCount = defCount
		logStep = sub / nCount
		start = False
		divisor = 0
		i = 15
		nTemp = 0
		chart.gridStep = 0
		chart.gridDigit = 0
		nCount = max(nMinCount, nCount)
		nCount = min(nMaxCount, nCount)
		nCount = max(nCount, 1)
		while i >= -6:
			divisor = math.pow(10.0, i)
			if divisor < 1:
				chart.gridDigit = chart.gridDigit + 1
			nTemp = int(math.floor(logStep / divisor))
			if start:
				if nTemp < 4:
					if chart.gridDigit > 0:
						chart.gridDigit = chart.gridDigit - 1
				elif nTemp >= 4 and nTemp <= 6:
					nTemp = 5
					chart.gridStep = chart.gridStep + nTemp * divisor
				else:
					chart.gridStep = chart.gridStep + 10 * divisor
					if chart.gridDigit > 0:
						chart.gridDigit = chart.gridDigit - 1
				break
			elif nTemp > 0:
				chart.gridStep = nTemp * divisor + chart.gridStep
				logStep = logStep - chart.gridStep
				start = True
			i = i - 1
		return 1
	return 0

#计算线性回归上下限
#chart:图表
#plot:画线
#a:直线k
#b:直线b
def getLRBandRange(chart, plot, a, b):
	bIndex = getChartIndexByDate(chart, plot.key1)
	eIndex = getChartIndexByDate(chart, plot.key2)
	tempBIndex = min(bIndex, eIndex)
	tempEIndex = max(bIndex, eIndex)
	bIndex = tempBIndex
	eIndex = tempEIndex
	upList = []
	downList = []
	for i in range(bIndex,eIndex + 1):
		high = chart.data[i].high
		low = chart.data[i].low
		midValue = (i - bIndex + 1) * a + b
		upList.append(high - midValue)
		downList.append(midValue - low)
	chart.upSubValue = maxValue(upList)
	chart.downSubValue = maxValue(downList)

#获取图表的区域
#chart: 图表
#plot: 画线
def getCandleRange(chart, plot):
	bIndex = getChartIndexByDate(chart, plot.key1)
	eIndex = getChartIndexByDate(chart, plot.key2)
	tempBIndex = min(bIndex, eIndex)
	tempEIndex = max(bIndex, eIndex)
	bIndex = tempBIndex
	eIndex = tempEIndex
	highList = []
	lowList = []
	for i in range(bIndex,eIndex + 1):
		highList.append(chart.data[i].high)
		lowList.append(chart.data[i].low)
	chart.nHighChart = maxValue(highList)
	chart.nLowChart = minValue(lowList)

#判断是否选中线条
#chart:图表
#mp:坐标
#divIndex:层索引
#datas:数据
#curIndex:当前索引
def selectLines(chart, mp, divIndex, datas, curIndex):
	if len(datas) > 0:
		topY = getChartY(chart, divIndex, datas[curIndex])
		if chart.hScalePixel <= 1:
			if mp.y >= topY - 8 and mp.y <= topY + 8:
				return True
		else:
			index = curIndex
			scaleX = getChartX(chart, index)
			judgeTop = 0
			judgeScaleX = scaleX
			if mp.x >= scaleX:
				leftIndex = curIndex + 1
				if curIndex < chart.lastVisibleIndex:
					rightValue = datas[leftIndex]
					judgeTop = getChartY(chart, divIndex, rightValue)
				else:
					judgeTop = topY
			else:
				judgeScaleX = scaleX - chart.hScalePixel
				rightIndex = curIndex - 1
				if curIndex > 0:
					leftValue = datas[rightIndex]
					judgeTop = getChartY(chart, divIndex, leftValue)
				else:
					judgeTop = topY
			lineWidth = 4
			judgeX = 0
			judgeY = 0
			judgeW = 0
			judgeH = 0
			if judgeTop >= topY:
				judgeX = judgeScaleX
				judgeY = topY - 2 - lineWidth
				judgeW = chart.hScalePixel
				judgeH = judgeTop - topY + 4 + lineWidth
				if judgeH < 4:
					judgeH = 4
			else:
				judgeX = judgeScaleX
				judgeY = judgeTop - 2 - lineWidth / 2
				judgeW = chart.hScalePixel
				judgeH = topY - judgeTop + 4 + lineWidth
				if judgeH < 4:
					judgeH = 4
			if mp.x >= judgeX and mp.x <= judgeX + judgeW and mp.y >= judgeY and mp.y <= judgeY + judgeH:
				return True
	return False

#判断是否在右轴选中线条
#chart:图表
#mp:坐标
#divIndex:层索引
#datas:数据
#curIndex:当前索引
def selectLinesInRight(chart, mp, divIndex, datas, curIndex):
	if len(datas) > 0:
		topY = getChartYInRight(chart, divIndex, datas[curIndex])
		if chart.hScalePixel <= 1:
			if mp.y >= topY - 8 and mp.y <= topY + 8:
				return True
		else:
			index = curIndex
			scaleX = getChartX(chart, index)
			judgeTop = 0
			judgeScaleX = scaleX
			if mp.x >= scaleX:
				leftIndex = curIndex + 1
				if curIndex < chart.lastVisibleIndex:
					rightValue = datas[leftIndex]
					judgeTop = getChartYInRight(chart, divIndex, rightValue)
				else:
					judgeTop = topY
			else:
				judgeScaleX = scaleX - chart.hScalePixel
				rightIndex = curIndex - 1
				if curIndex > 0:
					leftValue = datas[rightIndex]
					judgeTop = getChartYInRight(chart, divIndex, leftValue)
				else:
					judgeTop = topY
			lineWidth = 4
			judgeX = 0
			judgeY = 0
			judgeW = 0
			judgeH = 0
			if judgeTop >= topY:
				judgeX = judgeScaleX
				judgeY = topY - 2 - lineWidth
				judgeW = chart.hScalePixel
				judgeH = judgeTop - topY + 4 + lineWidth
				if judgeH < 4:
					judgeH = 4
			else:
				judgeX = judgeScaleX
				judgeY = judgeTop - 2 - lineWidth / 2
				judgeW = chart.hScalePixel
				judgeH = topY - judgeTop + 4 + lineWidth
				if judgeH < 4:
					judgeH = 4
			if mp.x >= judgeX and mp.x <= judgeX + judgeW and mp.y >= judgeY and mp.y <= judgeY + judgeH:
				return True
	return False

#判断是否选中图形
#chart:图表
#mp:坐标
def selectShape(chart, mp):
	if chart.data != None and len(chart.data) > 0:
		chart.selectShape = ""
		chart.selectShapeEx = ""
		candleHeight = getCandleDivHeight(chart)
		volHeight = getVolDivHeight(chart)
		indHeight = getIndDivHeight(chart)
		index = getChartIndex(chart, mp)
		if mp.y >= candleHeight + volHeight and mp.y <= candleHeight + volHeight + indHeight:
			if chart.showIndicator == "MACD":
				macdY = getChartY(chart, 2, chart.allmacdarr[index])
				zeroY = getChartY(chart, 2, 0)
				if selectLines(chart, mp, 2, chart.allmacdarr, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "MACD"
				if selectLines(chart, mp, 2, chart.alldifarr, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "DIF"
				elif selectLines(chart, mp, 2, chart.alldeaarr, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "DEA"
			elif chart.showIndicator == "KDJ":
				if selectLines(chart, mp, 2, chart.kdj_k, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "K"
				elif selectLines(chart, mp, 2, chart.kdj_d, index):	
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "D"
				elif selectLines(chart, mp, 2, chart.kdj_j, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "J"
			elif chart.showIndicator == "RSI":
				if selectLines(chart, mp, 2, chart.rsi1, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "6"
				elif selectLines(chart, mp, 2, chart.rsi2, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "12"
				elif selectLines(chart, mp, 2, chart.rsi3, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "24"
			elif chart.showIndicator == "BIAS":
				if selectLines(chart, mp, 2, chart.bias1, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "1"
				elif selectLines(chart, mp, 2, chart.bias2, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "2"
				elif selectLines(chart, mp, 2, chart.bias3, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "3"
			elif chart.showIndicator == "ROC":
				if selectLines(chart, mp, 2, chart.roc, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "ROC"
				elif selectLines(chart, mp, 2, chart.roc_ma, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "ROCMA"
			elif chart.showIndicator == "WR":
				if selectLines(chart, mp, 2, chart.wr1, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "1"
				elif selectLines(chart, mp, 2, chart.wr2, index):
					chart.selectShape = "WR"
					chart.selectShapeEx = "2"
			elif chart.showIndicator == "CCI":
				if selectLines(chart, mp, 2, chart.cci, index):
					chart.selectShape = chart.showIndicator
			elif chart.showIndicator == "BBI":
				if selectLines(chart, mp, 2, chart.bbi, index):
					chart.selectShape = chart.showIndicator
			elif chart.showIndicator == "TRIX":
				if selectLines(chart, mp, 2, chart.trix, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "TRIX"
				elif selectLines(chart, mp, 2, chart.trix_ma, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "TRIXMA"
			elif chart.showIndicator == "DMA":
				if selectLines(chart, mp, 2, chart.dma1, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "DIF"
				elif selectLines(chart, mp, 2, chart.dma2, index):
					chart.selectShape = chart.showIndicator
					chart.selectShapeEx = "DIFMA"
		elif mp.y >= candleHeight and mp.y <= candleHeight + volHeight:
			volY = getChartY(chart, 1, chart.data[index].volume)
			zeroY = getChartY(chart, 1, 0)
			if mp.y >= min(volY, zeroY) and mp.y <= max(volY, zeroY):
				chart.selectShape = "VOL"
		elif mp.y >= 0 and mp.y <= candleHeight:
			isTrend = False
			if chart.cycle == "trend":
				isTrend = True
			if isTrend == False:
				if chart.mainIndicator == "BOLL":
					if selectLines(chart, mp, 0, chart.boll_mid, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "MID"
					elif selectLines(chart, mp, 0, chart.boll_up, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "UP"
					elif selectLines(chart, mp, 0, chart.boll_down, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "DOWN"
				elif chart.mainIndicator == "MA":
					if selectLines(chart, mp, 0, chart.ma5, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "5"
					elif selectLines(chart, mp, 0, chart.ma10, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "10"
					elif selectLines(chart, mp, 0, chart.ma20, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "20"
					elif selectLines(chart, mp, 0, chart.ma30, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "30"
					elif selectLines(chart, mp, 0, chart.ma120, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "120"
					elif selectLines(chart, mp, 0, chart.ma250, index):
						chart.selectShape = chart.mainIndicator
						chart.selectShapeEx = "250"
			if chart.selectShape == "":
				highY = getChartY(chart, 0, chart.data[index].high)
				lowY = getChartY(chart, 0, chart.data[index].low)
				if isTrend:
					if selectLines(chart, mp, 0, chart.closearr, index):
						chart.selectShape = "CANDLE"
				else:
					if mp.y >= min(lowY, highY) and mp.y <= max(lowY, highY):
						chart.selectShape = "CANDLE"
		if len(chart.shapes) > 0:
			for i in range(0, len(chart.shapes)):
				shape = chart.shapes[i]
				if shape.leftOrRight:
					if selectLines(chart, mp, shape.divIndex, shape.datas, index):
						chart.selectShape = shape.shapeName
						break
				else:
					if selectLinesInRight(chart, mp, shape.divIndex, shape.datas, index):
						chart.selectShape = shape.shapeName
						break


#绘制线条
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
#divIndex:图层
#datas:数据
#color:颜色
#selected:是否选中
def drawChartLines(chart, paint, clipRect, divIndex, datas, color, selected):
	maxVisibleRecord = getChartMaxVisibleCount(chart, chart.hScalePixel, getChartWorkAreaWidth(chart))
	lastValidIndex = chart.lastVisibleIndex
	if chart.lastValidIndex != -1:
		lastValidIndex = chart.lastValidIndex
	drawPoints = []
	for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
		x = getChartX(chart, i)
		value = datas[i]
		y = getChartY(chart, divIndex, value)
		drawPoints.append(FCPoint(x, y))
		if selected:
			kPInterval = int(maxVisibleRecord / 30)
			if kPInterval < 2:
				kPInterval = 3
			if i % kPInterval == 0:
				paint.fillRect(color, x - 3, y - 3, x + 3, y + 3)
	paint.drawPolyline(color, chart.lineWidthChart, 0, drawPoints)

#绘制线条到右轴
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
#divIndex:图层
#datas:数据
#color:颜色
#selected:是否选中
def drawChartLinesInRight(chart, paint, clipRect, divIndex, datas, color, selected):
	maxVisibleRecord = getChartMaxVisibleCount(chart, chart.hScalePixel, getChartWorkAreaWidth(chart))
	lastValidIndex = chart.lastVisibleIndex
	if chart.lastValidIndex != -1:
		lastValidIndex = chart.lastValidIndex
	drawPoints = []
	for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
		x = getChartX(chart, i)
		value = datas[i]
		y = getChartYInRight(chart, divIndex, value)
		drawPoints.append(FCPoint(x, y))
		if selected:
			kPInterval = int(maxVisibleRecord / 30)
			if kPInterval < 2:
				kPInterval = 3
			if i % kPInterval == 0:
				paint.fillRect(color, x - 3, y - 3, x + 3, y + 3)
	paint.drawPolyline(color, chart.lineWidthChart, 0, drawPoints)

#数值转字符串，可以设置保留位数
#value 数值
#digit 小数位数
def toFixed(value, digit):
	if digit > 0:
		return ("{:." + str(digit) + "f}").format(value)
	else:
		return str(int(value))


#计算EMA
#n:周期
#value:当前数据
#lastEMA:上期数据
def getEMA(n, value, lastEMA):
	return(value * 2 + lastEMA * (n - 1)) / (n + 1)

#计算MACD
#dif:DIF数据
#dea:DEA数据
def getMACD(dif, dea):
	result = []
	for i in range(0,len(dif)):
		result.append((dif[i] - dea[i]) * 2)
	return result

#计算DIF
#close12:12日数据
#close26:26日数据
def getDIF(close12, close26):
	result = []
	for i in range(0,len(close12)):
		result.append(close12[i] - close26[i])
	return result

#REF函数
#ticks:数据
#days:日数
def REF(ticks, days):
	refArr = []
	length = len(ticks)
	for i in range(0,length):
		ref = 0
		if i >= days:
			ref = ticks[i - days]
		else:
			ref = ticks[0]
		refArr.append(ref)
	return refArr

#计算最大值
#ticks 最高价数组
#days
def HHV(ticks, days):
	hhv = []
	maxValue = ticks[0]
	for i in range(0,len(ticks)):
		if i >= days:
			maxValue = ticks[i]
			j = i
			while j > i - days:
				if maxValue < ticks[j]:
					maxValue = ticks[j]
				j = j - 1
			hhv.append(maxValue)
		else:
			if maxValue < ticks[i]:
				maxValue = ticks[i]
			hhv.append(maxValue)
	return hhv

#计算最小值
#ticks 最低价数组
#days
def LLV(ticks, days):
	llv = []
	minValue = ticks[0]
	for i in range(0,len(ticks)):
		if i >= days:
			minValue = ticks[i]
			j = i
			while j > i - days:
				if minValue > ticks[j]:
					minValue = ticks[j]
				j = j - 1
			llv.append(minValue)
		else:
			if minValue > ticks[i]:
				minValue = ticks[i]
			llv.append(minValue)
	return llv

#MA数据计算
#ticks 收盘价数组
#days 天数
def MA(ticks, days):
	maSum = 0
	mas = []
	last = 0
	for i in range(0,len(ticks)):
		ma = 0
		if i >= days:
			last = ticks[i - days]
			maSum = maSum + ticks[i] - last
			ma = maSum / days
		else:
			maSum += ticks[i]
			ma = maSum / (i + 1)
		mas.append(ma)
	return mas

#计算ROC数据
#ticks 收盘价数组
def getRocData(ticks, n, m, roc, maroc):
	for i in range(0,len(ticks)):
		currRoc = 0
		if i >= n:
			currRoc = 100 * (ticks[i] - ticks[i - n]) / ticks[i - n]
			roc.append(currRoc)
		else:
			currRoc = 100 * (ticks[i] - ticks[0]) / ticks[0]
			roc.append(currRoc)
	marocMA = MA(roc, m)
	for i in range(0, len(marocMA)):
		maroc.append(marocMA[i])

#计算rsi指标,分别返回以6日，12日，24日为参考基期的RSI值
def getRSIData(ticks, n1, n2, n3, rsi1, rsi2, rsi3):
	lastClosePx = ticks[0]
	lastSm1 = 0
	lastSa1 = 0
	lastSm2 = 0
	lastSa2 = 0
	lastSm3 = 0
	lastSa3 = 0
	for i in range(0, len(ticks)):
		c = ticks[i]
		m = max(c - lastClosePx, 0)
		a = abs(c - lastClosePx)
		if i == 0:
			lastSm1 = 0
			lastSa1 = 0
			rsi1.append(0)
		else:
			lastSm1 = (m + (n1 - 1) * lastSm1) / n1
			lastSa1 = (a + (n1 - 1) * lastSa1)/ n1
			if lastSa1 != 0:
				rsi1.append(lastSm1 / lastSa1 * 100)
			else:
				rsi1.append(0)

		if i == 0:
			lastSm2 = 0
			lastSa2 = 0
			rsi2.append(0)
		else:
			lastSm2 = (m + (n2 - 1) * lastSm2) / n2
			lastSa2 = (a + (n2 - 1) * lastSa2)/ n2
			if lastSa2 != 0:
				rsi2.append(lastSm2 / lastSa2 * 100)
			else:
				rsi2.append(0)

		if i == 0:
			lastSm3 = 0
			lastSa3 = 0
			rsi3.append(0)
		else:
			lastSm3 = (m + (n3 - 1) * lastSm3) / n3
			lastSa3 = (a + (n3 - 1) * lastSa3)/ n3
			if lastSa3 != 0:
				rsi3.append(lastSm3 / lastSa3 * 100)
			else:
				rsi3.append(0.0)
		lastClosePx =  c

#获取方差数据
def standardDeviationSum(listValue, avg_value, param):
	target_value = listValue[len(listValue) - 1]
	sumValue = (target_value - avg_value) * (target_value - avg_value)
	for i in range(0, len(listValue) - 1):
		ileft = listValue[i]
		sumValue = sumValue + (ileft - avg_value) * (ileft - avg_value)
	return sumValue

#计算boll指标,ma的周期为20日
def getBollData(ticks, maDays, ups, mas, lows):
	tickBegin = maDays - 1
	maSum  = 0
	p = 0
	for i in range(0, len(ticks)):
		c = ticks[i]
		ma = 0
		md = 0
		bstart = 0
		mdSum = 0
		maSum = maSum + c
		if i >= tickBegin:
			maSum = maSum - p
			ma = maSum / maDays
			bstart = i - tickBegin
			p = ticks[bstart]
			mas.append(ma)
			bstart = i - tickBegin
			p = ticks[bstart]
			values = []
			for j in range(bstart, bstart + maDays):
				values.append(ticks[j])
			mdSum = standardDeviationSum(values, ma, 2)
			md = math.sqrt(mdSum / maDays)
			ups.append(ma + 2 * md)
			lows.append(ma - 2 * md)
		else:
			ma = maSum / (i + 1)
			mas.append(ma)
			values = []
			for j in range(0, i + 1):
				values.append(ticks[j])
			mdSum = standardDeviationSum(values, ma, 2)
			md = math.sqrt(mdSum / (i + 1))
			ups.append(ma + 2 * md)
			lows.append(ma - 2 * md)

#获取最大最小值区间
#ticks:数据
def getMaxHighAndMinLow(chart, highArr, lowArr):
	for i in range(0, len(lowArr)):
		high = highArr[i]
		low = lowArr[i]
		if high > chart.nMaxHigh:
			chart.nMaxHigh = high
		if low < chart.nMaxLow:
			chart.nMaxLow = low

#计算kdj指标,rsv的周期为9日
def getKDJData(chart, highArr, lowArr, closeArr, n, m1, m2, ks, ds, js):
	rsvs = []
	lastK = 0
	lastD = 0
	curK = 0
	curD = 0
	for i in range(0, len(highArr)):
		highList = []
		lowList = []
		startIndex = i - n
		if startIndex < 0:
			startIndex = 0
		for j in range(startIndex, (i + 1)):
			highList.append(highArr[j])
			lowList.append(lowArr[j])
		chart.nMaxHigh = 0
		chart.nMaxLow = 0
		close = closeArr[i]
		getMaxHighAndMinLow(chart, highList, lowList)
		if chart.nMaxHigh == chart.nMaxLow:
			rsvs.append(0)
		else:
			rsvs.append((close - chart.nMaxLow) / (chart.nMaxHigh - chart.nMaxLow) * 100)
		if i == 0:
			lastK = rsvs[i]
			lastD = rsvs[i]
		curK = (m1 - 1) / m1 * lastK + 1.0 / m1 * rsvs[i]
		ks.append(curK)
		lastK = curK

		curD = (m2 - 1) / m2 * lastD + 1.0 / m2 * curK
		ds.append(curD)
		lastD = curD

		js.append(3.0 * curK - 2.0 * curD)

#获取BIAS的数据
#ticks 收盘价数组
def getBIASData(ticks, n1, n2, n3, bias1Arr, bias2Arr, bias3Arr):
	ma1 = MA(ticks, n1)
	ma2 = MA(ticks, n2)
	ma3 = MA(ticks, n3)
	for i in range(0,len(ticks)):
		b1 = (ticks[i] - ma1[i]) / ma1[i] * 100
		b2 = (ticks[i] - ma2[i]) / ma2[i] * 100
		b3 = (ticks[i] - ma3[i]) / ma3[i] * 100
		bias1Arr.append(b1)
		bias2Arr.append(b2)
		bias3Arr.append(b3)

#计算DMA（平均差）
#ticks 收盘价数组
def getDMAData(ticks, n1, n2, difArr, difmaArr):
	ma10 = MA(ticks, n1)
	ma50 = MA(ticks, n2)
	for i in range(0,len(ticks)):
		dif = ma10[i] - ma50[i]
		difArr.append(dif)
	difma = MA(difArr, n1)
	for i in range(0,len(difma)):
		difmaArr.append(difma[i])

#计算BBI(多空指标)
#ticks
def getBBIData(ticks, n1, n2, n3, n4, bbiArr):
	ma3 = MA(ticks, n1)
	ma6 = MA(ticks, n2)
	ma12 = MA(ticks, n3)
	ma24 = MA(ticks, n4)
	for i in range(0,len(ticks)):
		bbi = (ma3[i] + ma6[i] + ma12[i] + ma24[i]) / 4
		bbiArr.append(bbi)

#计算WR(威廉指标)
#ticks 含最高价,最低价, 收盘价的二维数组
#days
def getWRData(closeArr, highArr, lowArr, n1, n2, wr1Arr, wr2Arr):
	for i in range(0,len(closeArr)):
		highArr.append(highArr[i])
		lowArr.append(lowArr[i])
		closeArr.append(closeArr[i])
	highArr1 = HHV(highArr, n1)
	highArr2 = HHV(highArr, n2)
	lowArr1 = LLV(lowArr, n1)
	lowArr2 = LLV(lowArr, n2)
	for i in range(0,len(closeArr)):
		high1 = highArr1[i]
		low1 = lowArr1[i]
		high2 = highArr2[i]
		low2 = lowArr2[i]
		close = closeArr[i]
		wr1 = 100 * (high1 - close) / (high1 - low1)
		wr2 = 100 * (high2 - close) / (high2 - low2)
		wr1Arr.append(wr1)
		wr2Arr.append(wr2)

#CCI(顺势指标)计算  CCI（N日）=（TP－MA）÷MD÷0.015
#ticks 带最高价，最低价，收盘价的二维数组
def getCCIData(closeArr, highArr, lowArr, n, cciArr):
	tpArr = []
	for i in range(0,len(closeArr)):
		tpArr.append((closeArr[i] + highArr[i] + lowArr[i]) / 3)
	maClose = MA(closeArr, n)

	mdArr = []
	for i in range(0,len(closeArr)):
		mdArr.append(maClose[i] - closeArr[i])

	maMD = MA(mdArr, n)
	for i in range(0,len(closeArr)):
		cci = 0
		if maMD[i] > 0:
			cci = (tpArr[i] - maClose[i]) / (maMD[i] * 0.015)
		cciArr.append(cci)
	return cciArr

#获取TRIX的数据
#ticks:数据
def getTRIXData(ticks, n, m, trixArr, matrixArr):
	mtrArr = []

	emaArr1 = []
	emaArr1.append(ticks[0])
	for i in range(1,len(ticks)):
		emaArr1.append(getEMA(n, ticks[i], emaArr1[i - 1]))

	emaArr2 = []
	emaArr2.append(emaArr1[0])
	for i in range(1,len(ticks)):
		emaArr2.append(getEMA(n, emaArr1[i], emaArr2[i - 1]))

	mtrArr.append(emaArr2[0])
	for i in range(1,len(ticks)):
		mtrArr.append(getEMA(n, emaArr2[i], mtrArr[i - 1]))

	ref = REF(mtrArr, 1)
	for i in range(0,len(ticks)):
		trix = 100 * (mtrArr[i] - ref[i]) / ref[i]
		trixArr.append(trix)
	matrixMa = MA(trixArr, m)
	for i in range(0, len(matrixMa)):
		matrixArr.append(matrixMa[i])

#绘制画线工具
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
def drawChartPlot(chart, paint, clipRect):
	if len(chart.plots) > 0:
		divHeight = getCandleDivHeight(chart)
		paint.setClip(chart.leftVScaleWidth, 0, chart.size.cx, divHeight)
		for i in range(0,len(chart.plots)):
			plot = chart.plots[i]
			index1 = 0
			index2 = 0
			index3 = 0
			mpx1 = 0
			mpy1 = 0
			mpx2 = 0
			mpy2 = 0
			mpx3 = 0
			mpy3 = 0
			if plot.plotType == "LRLine" or plot.plotType == "LRChannel" or plot.plotType == "LRBand":
				listValue = []
				index1 = getChartIndexByDate(chart, plot.key1)
				index2 = getChartIndexByDate(chart, plot.key2)
				minIndex = min(index1, index2)
				maxIndex = max(index1, index2)
				for j in range(minIndex,maxIndex + 1):
					listValue.append(chart.data[j].close)
				linearRegressionEquation(chart, listValue)
				plot.value1 = chart.bChart
				plot.value2 = chart.kChart * (maxIndex - minIndex + 1) + chart.bChart
			elif plot.plotType == "BoxLine" or plot.plotType == "TironeLevels" or plot.plotType == "QuadrantLines":
				getCandleRange(chart, plot)
				nHigh = chart.nHighChart
				nLow = chart.nLowChart
				index1 = getChartIndexByDate(chart, plot.key1)
				index2 = getChartIndexByDate(chart, plot.key2)
				plot.key1 = getChartDateByIndex(chart, min(index1, index2))
				plot.key2 = getChartDateByIndex(chart, max(index1, index2))
				plot.value1 = nHigh
				plot.value2 = nLow
			if plot.key1 != None:
				index1 = getChartIndexByDate(chart, plot.key1)
				mpx1 = getChartX(chart, index1)
				mpy1 = getChartY(chart, 0, plot.value1)
				if chart.sPlot == plot:
					paint.fillEllipse(plot.pointColor, mpx1 - chart.plotPointSizeChart, mpy1 - chart.plotPointSizeChart, mpx1 + chart.plotPointSizeChart, mpy1 + chart.plotPointSizeChart)
			if plot.key2 != None:
				index2 = getChartIndexByDate(chart, plot.key2)
				mpx2 = getChartX(chart, index2)
				mpy2 = getChartY(chart, 0, plot.value2)
				if chart.sPlot == plot:
					paint.fillEllipse(plot.pointColor, mpx2 - chart.plotPointSizeChart, mpy2 - chart.plotPointSizeChart, mpx2 + chart.plotPointSizeChart, mpy2 + chart.plotPointSizeChart)
			if plot.key3 != None:
				index3 = getChartIndexByDate(chart, plot.key3)
				mpx3 = getChartX(chart, index3)
				mpy3 = getChartY(chart, 0, plot.value3)
				if chart.sPlot == plot:
					paint.fillEllipse(plot.pointColor, mpx3 - chart.plotPointSizeChart, mpy3 - chart.plotPointSizeChart, mpx3 + chart.plotPointSizeChart, mpy3 + chart.plotPointSizeChart)
			if plot.plotType == "Line":
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				if mpx2 == mpx1:
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, 0, mpx1, divHeight)
				else:
					newX1 = chart.leftVScaleWidth
					newY1 = newX1 * chart.kChart + chart.bChart
					newX2 = chart.size.cx - chart.rightVScaleWidth
					newY2 = newX2 * chart.kChart + chart.bChart
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, newX1, newY1, newX2, newY2)
			elif plot.plotType == "ArrowSegment":
				ARROW_Size = 24
				slopy = 0
				cosy = 0
				siny = 0
				slopy = math.atan2(mpy1 - mpy2, mpx1 - mpx2)
				cosy = math.cos(slopy)
				siny = math.sin(slopy)
				ptPoint = FCPoint(0,0)
				ptPoint.x = mpx2
				ptPoint.y = mpy2
				pts = []
				pts.append(FCPoint(0, 0))
				pts.append(FCPoint(0, 0))
				pts.append(FCPoint(0, 0))
				pts[0] = ptPoint
				pts[1].x = ptPoint.x + (ARROW_Size * cosy - (ARROW_Size / 2.0 * siny) + 0.5)
				pts[1].y = ptPoint.y + (ARROW_Size * siny + (ARROW_Size / 2.0 * cosy) + 0.5)
				pts[2].x = ptPoint.x + (ARROW_Size * cosy + ARROW_Size / 2.0 * siny + 0.5)
				pts[2].y = ptPoint.y - (ARROW_Size / 2.0 * cosy - ARROW_Size * siny + 0.5)
				ARROW_Size = 20
				ptPoint2 = FCPoint(0,0)
				ptPoint2.x = mpx2
				ptPoint2.y = mpy2
				pts2 = []
				pts2.append(FCPoint(0, 0))
				pts2.append(FCPoint(0, 0))
				pts2.append(FCPoint(0, 0))
				pts2[0] = ptPoint2
				pts2[1].x = ptPoint2.x + (ARROW_Size * cosy - (ARROW_Size / 2.0 * siny) + 0.5)
				pts2[1].y = ptPoint2.y + (ARROW_Size * siny + (ARROW_Size / 2.0 * cosy) + 0.5)
				pts2[2].x = ptPoint2.x + (ARROW_Size * cosy + ARROW_Size / 2.0 * siny + 0.5)
				pts2[2].y = ptPoint2.y - (ARROW_Size / 2.0 * cosy - ARROW_Size * siny + 0.5)
				lineXY(chart, pts2[1].x, pts2[1].y, pts2[2].x, pts2[2].y, 0, 0)
				newX1 = 0
				newY1 = 0
				newX2 = 0
				newY2 = 0

				if pts2[1].x > pts2[2].x:
					newX1 = pts2[2].x + (pts2[1].x - pts2[2].x) / 3
					newX2 = pts2[2].x + (pts2[1].x - pts2[2].x) * 2 / 3
				else:
					newX1 = pts2[1].x + (pts2[2].x - pts2[1].x) / 3
					newX2 = pts2[1].x + (pts2[2].x - pts2[1].x) * 2 / 3
				if chart.kChart == 0 and chart.bChart == 0:
					if pts2[1].y > pts2[2].y:
						newY1 = pts2[2].y + (pts2[1].y - pts2[2].y) / 3
						newY2 = pts2[2].y + (pts2[1].y - pts2[2].y) * 2 / 3
					else:
						newY1 = pts2[1].y + (pts2[2].y - pts2[1].y) / 3
						newY2 = pts2[1].y + (pts2[2].y - pts2[1].y) * 2 / 3
				else:
					newY1 = (chart.kChart * newX1) + chart.bChart
					newY2 = (chart.kChart * newX2) + chart.bChart
				pts2[1].x = newX1
				pts2[1].y = newY1
				pts2[2].x = newX2
				pts2[2].y = newY2
				drawPoints = []
				drawPoints.append(FCPoint(0, 0))
				drawPoints.append(FCPoint(0, 0))
				drawPoints.append(FCPoint(0, 0))
				drawPoints.append(FCPoint(0, 0))
				drawPoints.append(FCPoint(0, 0))
				drawPoints.append(FCPoint(0, 0))
				drawPoints[0].x = ptPoint.x
				drawPoints[0].y = ptPoint.y
				drawPoints[1].x = pts[1].x
				drawPoints[1].y = pts[1].y
				if mpy1 >= mpy2:
					drawPoints[2].x = pts2[1].x
					drawPoints[2].y = pts2[1].y
				else:
					drawPoints[2].x = pts2[2].x
					drawPoints[2].y = pts2[2].y
				drawPoints[3].x = mpx1
				drawPoints[3].y = mpy1
				if mpy1 >= mpy2:
					drawPoints[4].x = pts2[2].x
					drawPoints[4].y = pts2[2].y
				else:
					drawPoints[4].x = pts2[1].x
					drawPoints[4].y = pts2[1].y
				drawPoints[5].x = pts[2].x
				drawPoints[5].y = pts[2].y
				paint.fillPolygon(plot.lineColor, drawPoints)
			elif plot.plotType == "AngleLine":
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				if mpx2 == mpx1:
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, 0, mpx1, divHeight)
				else:
					newX1 = chart.leftVScaleWidth
					newY1 = newX1 * chart.kChart + chart.bChart
					newX2 = chart.size.cx - chart.rightVScaleWidth
					newY2 = newX2 * chart.kChart + chart.bChart
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, newX1, newY1, newX2, newY2)
				lineXY(chart, mpx1, mpy1, mpx3, mpy3, 0, 0)
				if mpx3 == mpx1:
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, 0, mpx1, divHeight)
				else:
					newX1 = chart.leftVScaleWidth
					newY1 = newX1 * chart.kChart + chart.bChart
					newX2 = chart.size.cx - chart.rightVScaleWidth
					newY2 = newX2 * chart.kChart + chart.bChart
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, newX1, newY1, newX2, newY2)
			elif plot.plotType == "Parallel":
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				if mpx2 == mpx1:
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, 0, mpx1, divHeight)
				else:
					newX1 = chart.leftVScaleWidth
					newY1 = newX1 * chart.kChart + chart.bChart
					newX2 = chart.size.cx - chart.rightVScaleWidth
					newY2 = newX2 * chart.kChart + chart.bChart
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, newX1, newY1, newX2, newY2)
					newB = mpy3 - chart.kChart * mpx3
				if mpx2 == mpx1:
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx3, 0, mpx3, divHeight)
				else:
					newX1 = chart.leftVScaleWidth
					newY1 = newX1 * chart.kChart + newB
					newX2 = chart.size.cx - chart.rightVScaleWidth
					newY2 = newX2 * chart.kChart + newB
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, newX1, newY1, newX2, newY2)
			elif plot.plotType == "Percent":
				listValue = getPercentParams(mpy1, mpy2)
				texts = []
				texts.append("0%")
				texts.append("25%")
				texts.append("50%")
				texts.append("75%")
				texts.append("100%")
				for j in range(0,len(listValue)):
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, chart.leftVScaleWidth, listValue[j], chart.size.cx - chart.rightVScaleWidth, listValue[j])
					tSize = paint.textSize(texts[j], chart.font)
					paint.drawText(texts[j], chart.textColor, chart.font, chart.leftVScaleWidth + 5, listValue[j] - tSize.cy - 2)
			elif plot.plotType == "FiboTimezone":
				fValue = 1
				aIndex = index1
				pos = 1
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, 0, mpx1, divHeight)
				tSize = paint.textSize("1", chart.font)
				paint.drawText("1", chart.textColor, chart.font, mpx1, divHeight - tSize.cy)
				while aIndex + fValue <= chart.lastVisibleIndex:
					fValue = fibonacciValue(pos)
					newIndex = aIndex + fValue
					newX = getChartX(chart, newIndex)
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, newX, 0, newX, divHeight)
					tSize = paint.textSize(str(fValue), chart.font)
					paint.drawText(str(fValue), chart.textColor, chart.font, newX, divHeight - tSize.cy)
					pos = pos + 1
			elif plot.plotType == "SpeedResist":
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
				if mpx1 != mpx2 and mpy1 != mpy2:
					firstP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) / 3)
					secondP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 2 / 3)
					startP = FCPoint(mpx1, mpy1)
					fK = 0
					fB = 0
					sK = 0
					sB = 0
					lineXY(chart, startP.x, startP.y, firstP.x, firstP.y, 0, 0)
					fK = chart.kChart
					fB = chart.bChart
					lineXY(chart, startP.x, startP.y, secondP.x, secondP.y, 0, 0)
					sK = chart.kChart
					sB = chart.bChart
					newYF = 0
					newYS = 0
					newX = 0
					if mpx2 > mpx1:
						newYF = fK * (chart.size.cx - chart.rightVScaleWidth) + fB
						newYS = sK * (chart.size.cx - chart.rightVScaleWidth) + sB
						newX = (chart.size.cx - chart.rightVScaleWidth)
					else:
						newYF = fB
						newYS = sB
					newX = chart.leftVScaleWidth
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, startP.x, startP.y, newX, newYF)
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, startP.x, startP.y, newX, newYS)
			elif plot.plotType == "FiboFanline":
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
				if mpx1 != mpx2 and mpy1 != mpy2:
					firstP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 0.382)
					secondP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 0.5)
					thirdP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 0.618)
					startP = FCPoint(mpx1, mpy1)
					listP = []
					listP.append(firstP)
					listP.append(secondP)
					listP.append(thirdP)
					listSize = len(listP)
					for j in range(0,listSize):
						lineXY(chart, startP.x, startP.y, listP[j].x, listP[j].y, 0, 0)
						newX = 0
						newY = 0
						if mpx2 > mpx1:
							newY = chart.kChart * (chart.size.cx - chart.rightVScaleWidth) + chart.bChart
							newX = (chart.size.cx - chart.rightVScaleWidth)
						else:
							newY = chart.bChart
							newX = chart.leftVScaleWidth
						paint.drawLine(plot.lineColor, plot.lineWidth, 0, startP.x, startP.y, newX, newY)
			elif plot.plotType == "LRLine":
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "LRBand":
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
				getLRBandRange(chart, plot, chart.kChart, chart.bChart)
				mpy1 = getChartY(chart, 0, plot.value1 + chart.upSubValue)
				mpy2 = getChartY(chart, 0, plot.value2 + chart.upSubValue)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
				mpy1 = getChartY(chart, 0, plot.value1 - chart.downSubValue)
				mpy2 = getChartY(chart, 0, plot.value2 - chart.downSubValue)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "LRChannel":
				getLRBandRange(chart, plot, chart.kChart, chart.bChart)
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				rightX = chart.size.cx - chart.rightVScaleWidth
				rightY = rightX * chart.kChart + chart.bChart
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, rightX, rightY)
				mpy1 = getChartY(chart, 0, plot.value1 + chart.upSubValue)
				mpy2 = getChartY(chart, 0, plot.value2 + chart.upSubValue)
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				rightY = rightX * chart.kChart + chart.bChart
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, rightX, rightY)
				mpy1 = getChartY(chart, 0, plot.value1 - chart.downSubValue)
				mpy2 = getChartY(chart, 0, plot.value2 - chart.downSubValue)
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				rightY = rightX * chart.kChart + chart.bChart
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, rightX, rightY)
			elif plot.plotType == "Segment":
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "Ray":
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				if chart.kChart != 0 or chart.bChart != 0:
					leftX = chart.leftVScaleWidth
					leftY = leftX * chart.kChart + chart.bChart
					rightX = chart.size.cx - chart.rightVScaleWidth
					rightY = rightX * chart.kChart + chart.bChart
					if mpx1 >= mpx2:
						paint.drawLine(plot.lineColor, plot.lineWidth, 0, leftX, leftY, mpx1, mpy1)
					else:
						paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, rightX, rightY)
				else:
					if mpy1 >= mpy2:
						paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx1, 0)
					else:
						paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx1, divHeight)
			elif plot.plotType == "Triangle":
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx2, mpy2, mpx3, mpy3)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx3, mpy3)
			elif plot.plotType == "SymmetricTriangle":
				if mpx2 != mpx1:
					a = (mpy2 - mpy1) / (mpx2 - mpx1)
					b = mpy1 - a * mpx1
					c = -a
					d = mpy3 - c * mpx3
					leftX = chart.leftVScaleWidth
					leftY = leftX * a + b
					rightX = chart.size.cx - chart.rightVScaleWidth
					rightY = rightX * a + b
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, leftX, leftY, rightX, rightY)
					leftY = leftX * c + d
					rightY = rightX * c + d
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, leftX, leftY, rightX, rightY)
				else:
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, 0, mpx1, divHeight)
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx3, 0, mpx3, divHeight)
			elif plot.plotType == "Rect":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				paint.drawRect(plot.lineColor, plot.lineWidth, 0, sX1, sY1, sX2, sY2)
			elif plot.plotType == "Cycle":
				r = math.sqrt(abs((mpx2 - mpx1) * (mpx2 - mpx1) + (mpy2 - mpy1) * (mpy2 - mpy1)))
				paint.drawEllipse(plot.lineColor, plot.lineWidth, 0, mpx1 - r, mpy1 - r, mpx1 + r, mpy1 + r)
			elif plot.plotType == "CircumCycle":
				ellipseOR(chart, mpx1, mpy1, mpx2, mpy2, mpx3, mpy3)
				paint.drawEllipse(plot.lineColor, plot.lineWidth, 0, chart.oXChart - chart.rChart, chart.oYChart - chart.rChart, chart.oXChart + chart.rChart, chart.oYChart + chart.rChart)
			elif plot.plotType == "Ellipse":
				x1 = 0
				y1 = 0
				x2 = 0
				y2 = 0
				if mpx1 <= mpx2:
					x1 = mpx2
					y1 = mpy2
					x2 = mpx1
					y2 = mpy1
				else:
					x1 = mpx1
					y1 = mpy1
					x2 = mpx2
					y2 = mpy2	
				x = x1 - (x1 - x2)
				y = 0
				width = (x1 - x2) * 2
				height = 0
				if y1 >= y2:
					height = (y1 - y2) * 2
				else:
					height = (y2 - y1) * 2
				y = y2 - height / 2
				paint.drawEllipse(plot.lineColor, plot.lineWidth, 0, x, y, x + width, y + height)
			elif plot.plotType == "ParalleGram":
				parallelogram(chart, mpx1, mpy1, mpx2, mpy2, mpx3, mpy3)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx1, mpy1, mpx2, mpy2)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx2, mpy2, mpx3, mpy3)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, mpx3, mpy3, chart.x4Chart, chart.y4Chart)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, chart.x4Chart, chart.y4Chart, mpx1, mpy1)
			elif plot.plotType == "BoxLine":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				paint.drawRect(plot.lineColor, plot.lineWidth, 0, sX1, sY1, sX2, sY2)
				bSize = paint.textSize("COUNT:" + str(abs(index2 - index1) + 1), chart.font)
				paint.drawText("COUNT:" + str(abs(index2 - index1) + 1), chart.textColor, chart.font, sX1 + 2, sY1 + 2)
				closeList = []
				for j in range(index1,index2 + 1):
					closeList.append(chart.data[j].close)
				avgClose = avgValue(closeList)
				closeY = getChartY(chart, 0, avgClose)
				paint.drawLine(plot.lineColor, plot.lineWidth, 1, sX1, closeY, sX2, closeY)
				drawAvg = "AVG:" + toFixed(avgClose, chart.candleDigit)
				tSize = paint.textSize(drawAvg, chart.font)
				paint.drawText(drawAvg, chart.textColor, chart.font, sX1 + 2, closeY - tSize.cy - 2)
			elif plot.plotType == "TironeLevels":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, sX1, sY1, sX2, sY1)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, sX1, sY2, sX2, sY2)
				paint.drawLine(plot.lineColor, plot.lineWidth, [5, 5], sX1 + (sX2 - sX1) / 2, sY1, sX1 + (sX2 - sX1) / 2, sY2)
				t1 = chart.nHighChart
				t2 = chart.nHighChart - (chart.nHighChart - chart.nLowChart) / 3
				t3 = chart.nHighChart - (chart.nHighChart - chart.nLowChart) / 2
				t4 = chart.nHighChart - 2 * (chart.nHighChart - chart.nLowChart) / 3
				t5 = chart.nLowChart
				tList = []
				tList.append(t2)
				tList.append(t3)
				tList.append(t4)
				for j in range(0,len(tList)):
					y = getChartY(chart, 0, tList[j])
					paint.drawLine(plot.lineColor, plot.lineWidth, [5,5], chart.leftVScaleWidth, y, chart.size.cx - chart.rightVScaleWidth, y)
					strText = toFixed(tList[j], chart.candleDigit)
					tSize = paint.textSize(strText, chart.font)
					paint.drawText(strText, chart.textColor, chart.font, chart.leftVScaleWidth + 2, y - tSize.cy - 2)
			elif plot.plotType == "QuadrantLines":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, sX1, sY1, sX2, sY1)
				paint.drawLine(plot.lineColor, plot.lineWidth, 0, sX1, sY2, sX2, sY2)
				t1 = chart.nHighChart
				t2 = chart.nHighChart - (chart.nHighChart - chart.nLowChart) / 4
				t3 = chart.nHighChart - (chart.nHighChart - chart.nLowChart) / 2
				t4 = chart.nHighChart - 3 * (chart.nHighChart - chart.nLowChart) / 4
				t5 = chart.nLowChart
				tList = []
				tList.append(t2)
				tList.append(t3)
				tList.append(t4)
				for j in range(0,len(tList)):
					y = getChartY(chart, 0, tList[j])
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, sX1, y, sX2, y)
			elif plot.plotType == "GoldenRatio":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				ranges = []
				ranges.append(0)
				ranges.append(0.236)
				ranges.append(0.382)
				ranges.append(0.5)
				ranges.append(0.618)
				ranges.append(0.809)
				ranges.append(1)
				ranges.append(1.382)
				ranges.append(1.618)
				ranges.append(2)
				ranges.append(2.382)
				ranges.append(2.618)
				minValue = min(plot.value1, plot.value2)
				maxValue = max(plot.value1, plot.value2)
				for j in range(0,len(ranges)):
					newY = sY2 + (sY1 - sY2) * (1 - ranges[j])
					if sY1 <= sY2:
						newY = sY1 + (sY2 - sY1) * ranges[j]
					paint.drawLine(plot.lineColor, plot.lineWidth, 0, chart.leftVScaleWidth, newY, chart.size.cx - chart.rightVScaleWidth, newY)
					newPoint = FCPoint(0, newY)
					value = getCandleDivValue(chart, newPoint)
					strText = toFixed(value, chart.candleDigit)
					tSize = paint.textSize(strText, chart.font)
					paint.drawText(strText, chart.textColor, chart.font, chart.leftVScaleWidth + 2, newY - tSize.cy - 2)
		paint.setClip(0, 0, chart.size.cx, chart.size.cy)

#选中直线
#chart: 图表
#mp:坐标
def selectPlot(chart, mp):
	sPlot = None
	chart.startMovePlot = False
	chart.selectPlotPoint = -1
	for i in range(0, len(chart.plots)):
		plot = chart.plots[i]
		index1 = 0
		index2 = 0
		index3 = 0
		mpx1 = 0
		mpy1 = 0
		mpx2 = 0
		mpy2 = 0
		mpx3 = 0
		mpy3 = 0
		if plot.key1 != None:
			index1 = getChartIndexByDate(chart, plot.key1)
			mpx1 = getChartX(chart, index1)
			mpy1 = getChartY(chart, 0, plot.value1)
			if mp.x >= mpx1 - chart.plotPointSizeChart and mp.x <= mpx1 + chart.plotPointSizeChart and mp.y >= mpy1 - chart.plotPointSizeChart and mp.y <= mpy1 + chart.plotPointSizeChart:
				sPlot = plot
				chart.selectPlotPoint = 0
				break
		if plot.key2 != None:
			index2 = getChartIndexByDate(chart, plot.key2)
			mpx2 = getChartX(chart, index2)
			mpy2 = getChartY(chart, 0, plot.value2)
			if mp.x >= mpx2 - chart.plotPointSizeChart and mp.x <= mpx2 + chart.plotPointSizeChart and mp.y >= mpy2 - chart.plotPointSizeChart and mp.y <= mpy2 + chart.plotPointSizeChart:
				sPlot = plot
				chart.selectPlotPoint = 1
				break
		if plot.key3 != None:
			index3 = getChartIndexByDate(chart, plot.key3)
			mpx3 = getChartX(chart, index3)
			mpy3 = getChartY(chart, 0, plot.value3)
			if mp.x >= mpx3 - chart.plotPointSizeChart and mp.x <= mpx3 + chart.plotPointSizeChart and mp.y >= mpy3 - chart.plotPointSizeChart and mp.y <= mpy3 + chart.plotPointSizeChart:
				sPlot = plot
				chart.selectPlotPoint = 2
				break

		if chart.selectPlotPoint == -1:
			if plot.plotType == "Line":
				chart.startMovePlot = selectLine(chart, mp, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "ArrowSegment":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "AngleLine":
				chart.startMovePlot = selectLine(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectLine(chart, mp, mpx1, mpy1, mpx3, mpy3)
			elif plot.plotType == "Parallel":
				chart.startMovePlot = selectLine(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
					newB = mpy3 - chart.kChart * mpx3
					if mpx2 == mpx1:
						if mp.x >= mpx3 - chart.plotPointSizeChart and mp.x <= mpx3 + chart.plotPointSizeChart:
							chart.startMovePlot = True
					else:
						newX1 = chart.leftVScaleWidth
						newY1 = newX1 * chart.kChart + newB
						newX2 = chart.size.cx - chart.rightVScaleWidth
						newY2 = newX2 * chart.kChart + newB
						chart.startMovePlot = selectLine(chart, mp, newX1, newY1, newX2, newY2)
			elif plot.plotType == "LRLine":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "Segment":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "Ray":
				chart.startMovePlot = selectRay(chart, mp, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "Triangle":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, mpx2, mpy2, mpx3, mpy3)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx3, mpy3)
			elif plot.plotType == "SymmetricTriangle":
				if mpx2 != mpx1:
					a = (mpy2 - mpy1) / (mpx2 - mpx1)
					b = mpy1 - a * mpx1
					c = -a
					d = mpy3 - c * mpx3
					leftX = chart.leftVScaleWidth
					leftY = leftX * a + b
					rightX = chart.size.cx - chart.rightVScaleWidth
					rightY = rightX * a + b
					chart.startMovePlot = selectSegment(chart, mp, leftX, leftY, rightX, rightY)
					if chart.startMovePlot == False:
						leftY = leftX * c + d
						rightY = rightX * c + d
						chart.startMovePlot = selectSegment(chart, mp, leftX, leftY, rightX, rightY)
				else:
					divHeight = getCandleDivHeight(chart)
					chart.startMovePlot = selectSegment(chart, mp, mpx1, 0, mpx1, divHeight)
					if chart.startMovePlot == False:		
						chart.startMovePlot = selectSegment(chart, mp, mpx3, 0, mpx3, divHeight)
			elif plot.plotType == "Rect":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				chart.startMovePlot = selectSegment(chart, mp, sX1, sY1, sX2, sY1)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX2, sY1, sX2, sY2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX1, sY2, sX2, sY2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX1, sY1, sX1, sY2)
			elif plot.plotType == "BoxLine":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				chart.startMovePlot = selectSegment(chart, mp, sX1, sY1, sX2, sY1)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX2, sY1, sX2, sY2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX1, sY2, sX2, sY2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX1, sY1, sX1, sY2)
			elif plot.plotType == "TironeLevels":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				chart.startMovePlot = selectSegment(chart, mp, sX1, sY1, sX2, sY1)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX1, sY2, sX2, sY2)
			elif plot.plotType == "QuadrantLines":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				chart.startMovePlot = selectSegment(chart, mp, sX1, sY1, sX2, sY1)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, sX1, sY2, sX2, sY2)
			elif plot.plotType == "GoldenRatio":
				sX1 = min(mpx1, mpx2)
				sY1 = min(mpy1, mpy2)
				sX2 = max(mpx1, mpx2)
				sY2 = max(mpy1, mpy2)
				ranges = []
				ranges.append(0)
				ranges.append(0.236)
				ranges.append(0.382)
				ranges.append(0.5)
				ranges.append(0.618)
				ranges.append(0.809)
				ranges.append(1)
				ranges.append(1.382)
				ranges.append(1.618)
				ranges.append(2)
				ranges.append(2.382)
				ranges.append(2.618)
				minValue = min(plot.value1, plot.value2)
				maxValue = max(plot.value1, plot.value2)
				for j in range(0,len(ranges)):
					newY = sY2 + (sY1 - sY2) * (1 - ranges[j])
					if sY1 <= sY2:
						newY = sY1 + (sY2 - sY1) * ranges[j]
					chart.startMovePlot = selectSegment(chart, mp, chart.leftVScaleWidth, newY, chart.size.cx - chart.rightVScaleWidth, newY)
					if chart.startMovePlot:
						break
			elif plot.plotType == "Cycle":
				r = math.sqrt(abs((mpx2 - mpx1) * (mpx2 - mpx1) + (mpy2 - mpy1) * (mpy2 - mpy1)))
				roundValue = (mp.x - mpx1) * (mp.x - mpx1) + (mp.y - mpy1) * (mp.y - mpy1)
				if roundValue / (r * r) >= 0.9 and roundValue / (r * r) <= 1.1:
					chart.startMovePlot = True
			elif plot.plotType == "CircumCycle":
				ellipseOR(chart, mpx1, mpy1, mpx2, mpy2, mpx3, mpy3)
				roundValue = (mp.x - chart.oXChart) * (mp.x - chart.oXChart) + (mp.y - chart.oYChart) * (mp.y - chart.oYChart)
				if roundValue / (chart.rChart * chart.rChart) >= 0.9 and roundValue / (chart.rChart * chart.rChart) <= 1.1:
					chart.startMovePlot = True
			elif plot.plotType == "Ellipse":
				x1 = 0
				y1 = 0
				x2 = 0
				y2 = 0
				if mpx1 <= mpx2:
					x1 = mpx2
					y1 = mpy2
					x2 = mpx1
					y2 = mpy1
				else:
					x1 = mpx1
					y1 = mpy1
					x2 = mpx2
					y2 = mpy2
				x = x1 - (x1 - x2)
				y = 0
				width = (x1 - x2) * 2
				height = 0
				if y1 >= y2:
					height = (y1 - y2) * 2
				else:
					height = (y2 - y1) * 2
				y = y2 - height / 2
				a = width / 2
				b = height / 2
				chart.startMovePlot = ellipseHasPoint(mp.x, mp.y, x + (width / 2), y + (height / 2), a, b)
			elif plot.plotType == "LRBand":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					listValue = []
					minIndex = min(index1, index2)
					maxIndex = max(index1, index2)
					for j in range(minIndex,maxIndex + 1):
						listValue.append(chart.data[j].close)
					linearRegressionEquation(chart, listValue)
					getLRBandRange(chart, plot, chart.kChart, chart.bChart)
					mpy1 = getChartY(chart, 0, plot.value1 + chart.upSubValue)
					mpy2 = getChartY(chart, 0, plot.value2 + chart.upSubValue)
					chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
					if chart.startMovePlot == False:
						mpy1 = getChartY(chart, 0, plot.value1 - chart.downSubValue)
						mpy2 = getChartY(chart, 0, plot.value2 - chart.downSubValue)
						chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
			elif plot.plotType == "LRChannel":
				lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
				rightX = chart.size.cx - chart.rightVScaleWidth
				rightY = rightX * chart.kChart + chart.bChart
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, rightX, rightY)
				if chart.startMovePlot == False:
					listValue = []
					minIndex = min(index1, index2)
					maxIndex = max(index1, index2)
					for j in range(minIndex,maxIndex + 1):
						listValue.append(chart.data[j].close)
					linearRegressionEquation(chart, listValue)
					getLRBandRange(chart, plot, chart.kChart, chart.bChart)
					mpy1 = getChartY(chart, 0, plot.value1 + chart.upSubValue)
					mpy2 = getChartY(chart, 0, plot.value2 + chart.upSubValue)
					lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
					rightY = rightX * chart.kChart + chart.bChart
					chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, rightX, rightY)
					if chart.startMovePlot == False:
						mpy1 = getChartY(chart, 0, plot.value1 - chart.downSubValue)
						mpy2 = getChartY(chart, 0, plot.value2 - chart.downSubValue)
						lineXY(chart, mpx1, mpy1, mpx2, mpy2, 0, 0)
						rightY = rightX * chart.kChart + chart.bChart
						chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, rightX, rightY)
			elif plot.plotType == "ParalleGram":
				parallelogram(chart, mpx1, mpy1, mpx2, mpy2, mpx3, mpy3)
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					chart.startMovePlot = selectSegment(chart, mp, mpx2, mpy2, mpx3, mpy3)
					if chart.startMovePlot == False:
						chart.startMovePlot = selectSegment(chart, mp, mpx3, mpy3, chart.x4Chart, chart.y4Chart)
						if chart.startMovePlot == False:
							chart.startMovePlot = selectSegment(chart, mp, chart.x4Chart, chart.y4Chart, mpx1, mpy1)
			elif plot.plotType == "SpeedResist":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					if mpx1 != mpx2 and mpy1 != mpy2:
						firstP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) / 3)
						secondP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 2 / 3)
						startP = FCPoint(mpx1, mpy1)
						fK = 0
						fB = 0
						sK = 0
						sB = 0
						lineXY(chart, startP.x, startP.y, firstP.x, firstP.y, 0, 0)
						fK = chart.kChart
						fB = chart.bChart
						lineXY(chart, startP.x, startP.y, secondP.x, secondP.y, 0, 0)
						sK = chart.kChart
						sB = chart.bChart
						newYF = 0
						newYS = 0
						newX = 0
						if mpx2 > mpx1:
							newYF = fK * (chart.size.cx - chart.rightVScaleWidth) + fB
							newYS = sK * (chart.size.cx - chart.rightVScaleWidth) + sB
							newX = (chart.size.cx - chart.rightVScaleWidth)
						else:
							newYF = fB
							newYS = sB
							newX = chart.leftVScaleWidth
						chart.startMovePlot = selectSegment(chart, mp, startP.x, startP.y, newX, newYF)
						if chart.startMovePlot == False:
							chart.startMovePlot = selectSegment(chart, mp, startP.x, startP.y, newX, newYS)
			elif plot.plotType == "FiboFanline":
				chart.startMovePlot = selectSegment(chart, mp, mpx1, mpy1, mpx2, mpy2)
				if chart.startMovePlot == False:
					if mpx1 != mpx2 and mpy1 != mpy2:
						firstP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 0.382)
						secondP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 0.5)
						thirdP = FCPoint(mpx2, mpy2 - (mpy2 - mpy1) * 0.618)
						startP = FCPoint(mpx1, mpy1)
						listP = []
						listP.append(firstP)
						listP.append(secondP)
						listP.append(thirdP)
						listSize = len(listP)
						for j in range(0,listSize):
							lineXY(chart, startP.x, startP.y, listP[j].x, listP[j].y, 0, 0)
							newX = 0
							newY = 0
							if mpx2 > mpx1:
								newY = chart.kChart * (chart.size.cx - chart.rightVScaleWidth) + chart.bChart
								newX = (chart.size.cx - chart.rightVScaleWidth)
							else:
								newY = chart.bChart
								newX = chart.leftVScaleWidth
							chart.startMovePlot = selectSegment(chart, mp, startP.x, startP.y, newX, newY)
							if chart.startMovePlot:
								break
			elif plot.plotType == "FiboTimezone":
				fValue = 1
				aIndex = index1
				pos = 1
				divHeight = getCandleDivHeight(chart)
				chart.startMovePlot = selectSegment(chart, mp, mpx1, 0, mpx1, divHeight)
				if chart.startMovePlot == False:
					while aIndex + fValue <= chart.lastVisibleIndex:
						fValue = fibonacciValue(pos)
						newIndex = aIndex + fValue
						newX = getChartX(chart, newIndex)
						chart.startMovePlot = selectSegment(chart, mp, newX, 0, newX, divHeight)
						if chart.startMovePlot:
							break
						pos = pos + 1
			elif plot.plotType == "Percent":
				listValue = getPercentParams(mpy1, mpy2)
				for j in range(0, len(listValue)):
					chart.startMovePlot = selectSegment(chart, mp, chart.leftVScaleWidth, listValue[j], chart.size.cx - chart.rightVScaleWidth, listValue[j])
					if chart.startMovePlot:
						break
			if chart.startMovePlot:
				sPlot = plot
				plot.startKey1 = plot.key1
				plot.startValue1 = plot.value1
				plot.startKey2 = plot.key2
				plot.startValue2 = plot.value2
				plot.startKey3 = plot.key3
				plot.startValue3 = plot.value3
				break
	return sPlot

#添加画线
#chart: 图表
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
def addPlotDefault(chart, firstTouch, firstPoint, secondTouch, secondPoint):
	mp = firstPoint
	if mp.y < getCandleDivHeight(chart):
		touchIndex = getChartIndex(chart, mp)
		if touchIndex >= chart.firstVisibleIndex and touchIndex <= chart.lastVisibleIndex:
			if chart.addingPlot == "FiboTimezone":
				fIndex = touchIndex
				fDate = getChartDateByIndex(chart, fIndex)
				y = getCandleDivValue(chart, mp)
				newPlot = FCPlot()
				if chart.paint.defaultUIStyle == "light":
					newPlot.lineColor = "rgb(0,0,0)"
					newPlot.pointColor = "rgba(0,0,0,125)"
				elif chart.paint.defaultUIStyle == "dark":
					newPlot.lineColor = "rgb(255,255,255)"
					newPlot.pointColor = "rgba(255,255,255,125)"
				newPlot.key1 = fDate
				newPlot.value1 = y
				newPlot.plotType = chart.addingPlot
				chart.plots.append(newPlot)
				chart.sPlot = selectPlot(chart, mp)
			elif chart.addingPlot == "Triangle" or chart.addingPlot == "CircumCycle" or chart.addingPlot == "ParalleGram" or chart.addingPlot == "AngleLine" or chart.addingPlot == "Parallel" or chart.addingPlot == "SymmetricTriangle":
				eIndex = touchIndex
				bIndex = eIndex - 5
				if bIndex >= 0:
					fDate = getChartDateByIndex(chart, bIndex)
					sDate = getChartDateByIndex(chart, eIndex)
					y = getCandleDivValue(chart, mp)
					newPlot = FCPlot()
					if chart.paint.defaultUIStyle == "light":
						newPlot.lineColor = "rgb(0,0,0)"
						newPlot.pointColor = "rgba(0,0,0,125)"
					elif chart.paint.defaultUIStyle == "dark":
						newPlot.lineColor = "rgb(255,255,255)"
						newPlot.pointColor = "rgba(255,255,255,125)"
					newPlot.key1 = fDate
					newPlot.value1 = y
					newPlot.key2 = sDate
					newPlot.value2 = y
					newPlot.key3 = sDate
					newPlot.value3 = chart.candleMin + (chart.candleMax - chart.candleMin) / 2
					newPlot.plotType = chart.addingPlot
					chart.plots.append(newPlot)
					chart.sPlot = selectPlot(chart, mp)
			else:
				eIndex = touchIndex
				bIndex = eIndex - 5
				if bIndex >= 0:
					fDate = getChartDateByIndex(chart, bIndex)
					sDate = getChartDateByIndex(chart, eIndex)
					y = getCandleDivValue(chart, mp)
					newPlot = FCPlot()
					if chart.paint.defaultUIStyle == "light":
						newPlot.lineColor = "rgb(0,0,0)"
						newPlot.pointColor = "rgba(0,0,0,125)"
					elif chart.paint.defaultUIStyle == "dark":
						newPlot.lineColor = "rgb(255,255,255)"
						newPlot.pointColor = "rgba(255,255,255,125)"
					newPlot.key1 = fDate
					newPlot.value1 = y
					newPlot.key2 = sDate
					newPlot.value2 = y
					newPlot.plotType = chart.addingPlot
					chart.plots.append(newPlot)
					chart.sPlot = selectPlot(chart, mp)

#图表的鼠标按下方法
#chart: 图表
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
def touchDownChart(chart, firstTouch, firstPoint, secondTouch, secondPoint):
	mp = firstPoint
	chart.targetOldX = 0
	chart.targetOldX2 = 0
	chart.selectShape = ""
	chart.selectShapeEx = ""
	chart.touchDownPointChart = mp
	if chart.data != None and len(chart.data) > 0:
		chart.sPlot = selectPlot(chart, mp)
		if chart.sPlot == None:
			selectShape(chart, mp)
	if chart.paint.isDoubleClick:
		if chart.showCrossLine:
			chart.showCrossLine = False
		else:
			chart.showCrossLine = True

#左滚
#chart:图表
#step:步长
def scrollLeftChart(chart, step):
	chart.targetOldX = 0
	chart.targetOldX2 = 0
	if chart.showCrossLine:
		chart.crossStopIndex = chart.crossStopIndex - step
		if chart.crossStopIndex >= chart.firstVisibleIndex:
			step = 0
		elif chart.crossStopIndex < 0:
			chart.crossStopIndex = 0
	if step > 0:
		subIndex = chart.lastVisibleIndex - chart.firstVisibleIndex
		fIndex = chart.firstVisibleIndex - step
		if fIndex < 0:
			fIndex = 0
		eIndex = fIndex + subIndex
		chart.firstVisibleIndex = fIndex
		chart.lastVisibleIndex = eIndex
	checkChartLastVisibleIndex(chart)
	if chart.onCalculateChartMaxMin != None:
		chart.onCalculateChartMaxMin(chart)
	elif chart.paint.onCalculateChartMaxMin != None:
		chart.paint.onCalculateChartMaxMin(chart)
	else:
		calculateChartMaxMin(chart)

#右滚
#chart:图表
#step:步长
def scrollRightChart(chart, step):
	chart.targetOldX = 0
	chart.targetOldX2 = 0
	dataCount = len(chart.data)
	if chart.showCrossLine:
		chart.crossStopIndex = chart.crossStopIndex + step
		if chart.crossStopIndex <= chart.lastVisibleIndex:
			step = 0
		elif chart.crossStopIndex > dataCount - 1:
			chart.crossStopIndex = dataCount - 1
	if step > 0:
		subIndex = chart.lastVisibleIndex - chart.firstVisibleIndex
		eIndex = chart.lastVisibleIndex + step
		if eIndex > dataCount - 1:
			eIndex = dataCount - 1
		fIndex = eIndex - subIndex
		chart.firstVisibleIndex = fIndex
		chart.lastVisibleIndex = eIndex
	checkChartLastVisibleIndex(chart)
	if chart.onCalculateChartMaxMin != None:
		chart.onCalculateChartMaxMin(chart)
	elif chart.paint.onCalculateChartMaxMin != None:
		chart.paint.onCalculateChartMaxMin(chart)
	else:
		calculateChartMaxMin(chart)

#图标的键盘按下事件
#chart:图表
#key:按键
def keyDownChart(chart, key):
	if key == 38:
		zoomOutChart(chart)
	elif key == 40:
		zoomInChart(chart)
	elif key == 37:
		scrollLeftChart(chart, 1)
	elif key == 39:
		scrollRightChart(chart, 1)

#图表的鼠标移动方法
#chart: 图表
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
def touchMoveChart(chart, firstTouch, firstPoint, secondTouch, secondPoint):
	if chart.data == None or len(chart.data) == 0:
		return
	mp = firstPoint
	chart.targetOldX = 0
	chart.targetOldX2 = 0
	chart.crossStopIndex = getChartIndex(chart, mp)
	chart.touchPosition = mp
	if firstTouch and chart.sPlot != None:
		newIndex = getChartIndex(chart, mp)
		if newIndex >= 0 and newIndex < len(chart.data):
			newDate = getChartDateByIndex(chart, newIndex)
			newValue = getCandleDivValue(chart, mp)
			if chart.selectPlotPoint == 0:
				chart.sPlot.key1 = newDate
				chart.sPlot.value1 = newValue
			elif chart.selectPlotPoint == 1:
				chart.sPlot.key2 = newDate
				chart.sPlot.value2 = newValue
			elif chart.selectPlotPoint == 2:
				chart.sPlot.key3 = newDate
				chart.sPlot.value3 = newValue
			elif chart.startMovePlot:
				bValue = getCandleDivValue(chart, chart.touchDownPointChart)
				bIndex = getChartIndex(chart, chart.touchDownPointChart)
				if chart.sPlot.key1 != None:
					chart.sPlot.value1 = chart.sPlot.startValue1 + (newValue - bValue)
					startIndex1 = getChartIndexByDate(chart, chart.sPlot.startKey1)
					newIndex1 = startIndex1 + (newIndex - bIndex)
					if newIndex1 < 0:
						newIndex1 = 0
					elif newIndex1 > len(chart.data) - 1:
						newIndex1 = len(chart.data) - 1
					chart.sPlot.key1 = getChartDateByIndex(chart, newIndex1)
				if chart.sPlot.key2 != None:
					chart.sPlot.value2 = chart.sPlot.startValue2 + (newValue - bValue)
					startIndex2 = getChartIndexByDate(chart, chart.sPlot.startKey2)
					newIndex2 = startIndex2 + (newIndex - bIndex)
					if newIndex2 < 0:
						newIndex2 = 0
					elif newIndex2 > len(chart.data) - 1:
						newIndex2 = len(chart.data) - 1
					chart.sPlot.key2 = getChartDateByIndex(chart, newIndex2)
				if chart.sPlot.key3 != None:
					chart.sPlot.value3 = chart.sPlot.startValue3 + (newValue - bValue)
					startIndex3 = getChartIndexByDate(chart, chart.sPlot.startKey3)
					newIndex3 = startIndex3 + (newIndex - bIndex)
					if newIndex3 < 0:
						newIndex3 = 0
					elif newIndex3 > len(chart.data) - 1:
						newIndex3 = len(chart.data) - 1
					chart.sPlot.key3 = getChartDateByIndex(chart, newIndex3)
		return
	if firstTouch and secondTouch:
		if firstPoint.x > secondPoint.x:
			chart.firstTouchPointCache = secondPoint
			chart.secondTouchPointCache = firstPoint
		else:
			chart.firstTouchPointCache = firstPoint
			chart.secondTouchPointCache = secondPoint
		if chart.firstTouchIndexCache == -1 or chart.secondTouchIndexCache == -1:
			chart.firstTouchIndexCache = getChartIndex(chart, chart.firstTouchPointCache)
			chart.secondTouchIndexCache = getChartIndex(chart, chart.secondTouchPointCache)
			chart.firstIndexCache = chart.firstVisibleIndex
			chart.lastIndexCache = chart.lastVisibleIndex
	elif firstTouch:
		chart.secondTouchIndexCache = -1
		if chart.firstTouchIndexCache == -1:
			chart.firstTouchPointCache = firstPoint
			chart.firstTouchIndexCache = getChartIndex(chart, chart.firstTouchPointCache)
			chart.firstIndexCache = chart.firstVisibleIndex
			chart.lastIndexCache = chart.lastVisibleIndex
			chart.firstPaddingTop = chart.candlePaddingTop
			chart.firstPaddingBottom = chart.candlePaddingBottom

	if firstTouch and secondTouch:
		if chart.firstTouchIndexCache != -1 and chart.secondTouchIndexCache != -1:
			fPoint = firstPoint
			sPoint = secondPoint
			if firstPoint.x > secondPoint.x:
				fPoint = secondPoint
				sPoint = firstPoint
			subX = abs(sPoint.x - fPoint.x)
			subIndex = abs(chart.secondTouchIndexCache - chart.firstTouchIndexCache)
			if subX > 0 and subIndex > 0:
				newScalePixel = subX / subIndex
				if newScalePixel >= 3:
					intScalePixel = int(newScalePixel)
					newScalePixel = intScalePixel
				if newScalePixel != chart.hScalePixel:
					newFirstIndex = chart.firstTouchIndexCache
					thisX = fPoint.x
					thisX -= newScalePixel
					while thisX > chart.leftVScaleWidth + newScalePixel:
						newFirstIndex = newFirstIndex - 1
						if newFirstIndex < 0:
							newFirstIndex = 0
							break
						thisX -= newScalePixel
					thisX = sPoint.x
					newSecondIndex = chart.secondTouchIndexCache
					thisX += newScalePixel
					while thisX < chart.size.cx - chart.rightVScaleWidth - newScalePixel:
						newSecondIndex = newSecondIndex + 1
						if newSecondIndex > len(chart.data) - 1:
							newSecondIndex = len(chart.data) - 1
							break
						thisX += newScalePixel
					setChartVisibleIndex(chart, newFirstIndex, newSecondIndex)
					maxVisibleRecord = getChartMaxVisibleCount(chart, chart.hScalePixel, getChartWorkAreaWidth(chart))
					while (maxVisibleRecord < chart.lastVisibleIndex - chart.firstVisibleIndex + 1) and (chart.lastVisibleIndex > chart.firstVisibleIndex):
						chart.lastVisibleIndex = chart.lastVisibleIndex - 1
					checkChartLastVisibleIndex(chart)
					resetChartVisibleRecord(chart)
					if chart.onCalculateChartMaxMin != None:
						chart.onCalculateChartMaxMin(chart)
					elif chart.paint.onCalculateChartMaxMin != None:
						chart.paint.onCalculateChartMaxMin(chart)
					else:
						calculateChartMaxMin(chart)
	elif firstTouch:
		if chart.autoFillHScale == False:
			subIndex = int((chart.firstTouchPointCache.x - firstPoint.x) / chart.hScalePixel)
			if chart.allowDragChartDiv:
				chart.candlePaddingTop = chart.firstPaddingTop - int(chart.firstTouchPointCache.y - firstPoint.y)
				chart.candlePaddingBottom = chart.firstPaddingBottom + int(chart.firstTouchPointCache.y - firstPoint.y)
			fIndex = chart.firstIndexCache + subIndex
			lIndex = chart.lastIndexCache + subIndex    
			if fIndex > len(chart.data) - 1:
				fIndex = len(chart.data) - 1
				lIndex = len(chart.data) - 1
			chart.firstVisibleIndex = fIndex
			chart.lastVisibleIndex = lIndex
			checkChartLastVisibleIndex(chart)
			if chart.onCalculateChartMaxMin != None:
				chart.onCalculateChartMaxMin(chart)
			elif chart.paint.onCalculateChartMaxMin != None:
				chart.paint.onCalculateChartMaxMin(chart)
			else:
				calculateChartMaxMin(chart)

#绘制刻度
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
def drawChartScale(chart, paint, clipRect):
	if chart.leftVScaleWidth > 0:
		paint.fillRect(chart.scaleColor, chart.leftVScaleWidth, 0, chart.leftVScaleWidth + chart.lineWidthChart, chart.size.cy - chart.hScaleHeight)
	if chart.rightVScaleWidth > 0:
		paint.fillRect(chart.scaleColor, chart.size.cx - chart.rightVScaleWidth, 0, chart.size.cx - chart.rightVScaleWidth + chart.lineWidthChart, chart.size.cy - chart.hScaleHeight)
	if chart.hScaleHeight > 0:
		paint.fillRect(chart.scaleColor, 0, chart.size.cy - chart.hScaleHeight, chart.size.cx, chart.size.cy - chart.hScaleHeight + chart.lineWidthChart)
	candleDivHeight = getCandleDivHeight(chart)
	volDivHeight = getVolDivHeight(chart)
	indDivHeight = getIndDivHeight(chart)
	indDivHeight2 = getIndDivHeight2(chart)
	if volDivHeight > 0:
		paint.fillRect(chart.scaleColor, chart.leftVScaleWidth, candleDivHeight, chart.size.cx - chart.rightVScaleWidth, candleDivHeight + chart.lineWidthChart)
	if indDivHeight > 0:
		paint.fillRect(chart.scaleColor, chart.leftVScaleWidth, candleDivHeight + volDivHeight, chart.size.cx - chart.rightVScaleWidth, candleDivHeight + volDivHeight + chart.lineWidthChart)
	if indDivHeight2 > 0:
		paint.fillRect(chart.scaleColor, chart.leftVScaleWidth, candleDivHeight + volDivHeight + indDivHeight, chart.size.cx - chart.rightVScaleWidth, candleDivHeight + volDivHeight + indDivHeight + chart.lineWidthChart)
	if chart.data != None and len(chart.data) > 0:
		topPoint = FCPoint(0, 20)
		bottomPoint = FCPoint(0, candleDivHeight - 10)
		candleMax = getChartValue(chart, topPoint)
		candleMin = getChartValue(chart, bottomPoint)
		ret = chartGridScale(chart, candleMin, candleMax,  (candleDivHeight - chart.candlePaddingTop - chart.candlePaddingBottom) / 2, chart.vScaleDistance, chart.vScaleDistance / 2, int((candleDivHeight - chart.candlePaddingTop - chart.candlePaddingBottom) / chart.vScaleDistance))
		if chart.gridStep > 0 and ret > 0:
			drawValues = []
			isTrend = False
			if chart.cycle == "trend":
				isTrend = True
			firstOpen = chart.firstOpen
			if isTrend:
				if firstOpen == 0:
					firstOpen = chart.data[chart.firstVisibleIndex].close
				subValue = candleMax - candleMin
				count = int((candleDivHeight - chart.candlePaddingTop - chart.candlePaddingBottom) / chart.vScaleDistance)
				if count > 0:
					subValue /= count
				start = firstOpen
				while start < candleMax:
					start += subValue
					if start <= candleMax:
						drawValues.append(start)
				start = firstOpen
				while start > candleMin:
					start -= subValue
					if start >= candleMin:
						drawValues.append(start)
			else:
				start = 0
				if candleMin >= 0:
					while start + chart.gridStep < candleMin:
						start += chart.gridStep
				else:
					while start - chart.gridStep > candleMin:
						start -= chart.gridStep

				while start <= candleMax:
					if start > candleMin:
						drawValues.append(start)
					start += chart.gridStep
			drawValues.append(firstOpen)
			for i in range(0,len(drawValues)):
				start = drawValues[i]
				hAxisY = getChartY(chart, 0, start)
				if hAxisY < 1 or hAxisY > candleDivHeight:
					continue
				paint.fillRect(chart.gridColor, chart.leftVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth, int(hAxisY) + chart.lineWidthChart)
				paint.fillRect(chart.scaleColor, chart.leftVScaleWidth - 8, int(hAxisY), chart.leftVScaleWidth, int(hAxisY) + chart.lineWidthChart)
				paint.fillRect(chart.scaleColor, chart.size.cx - chart.rightVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth + 8, int(hAxisY) + chart.lineWidthChart)
				drawText = toFixed(start, chart.candleDigit)
				tSize = paint.textSize(drawText, chart.font)
				if isTrend:
					diffRange = ((start - firstOpen) / firstOpen * 100)
					diffRangeStr = toFixed(diffRange, 2) + "%"
					if diffRange >= 0:
						paint.drawText(diffRangeStr, chart.upColor, chart.font, chart.size.cx - chart.rightVScaleWidth + 10, int(hAxisY) - tSize.cy / 2)
					else:
						paint.drawText(diffRangeStr, chart.downColor, chart.font, chart.size.cx - chart.rightVScaleWidth + 10, int(hAxisY) - tSize.cy / 2)
				else:
					paint.drawText(drawText, chart.textColor, chart.font, chart.size.cx - chart.rightVScaleWidth + 10, int(hAxisY) - tSize.cy / 2)
				paint.drawText(drawText, chart.textColor, chart.font, chart.leftVScaleWidth - tSize.cx - 10, int(hAxisY) - tSize.cy / 2)			
		topPoint = FCPoint(0, candleDivHeight + 10)
		bottomPoint = FCPoint(0, candleDivHeight + volDivHeight - 10)
		volMax = getChartValue(chart, topPoint)
		volMin = getChartValue(chart, bottomPoint)
		ret = chartGridScale(chart, volMin, volMax,  (volDivHeight - chart.volPaddingTop - chart.volPaddingBottom) / 2, chart.vScaleDistance, chart.vScaleDistance / 2, int((volDivHeight - chart.volPaddingTop - chart.volPaddingBottom) / chart.vScaleDistance))
		if chart.gridStep > 0 and ret > 0:
			start = 0
			if volMin >= 0:
				while start + chart.gridStep < volMin:
					start += chart.gridStep
			else:
				while start - chart.gridStep > volMin:
					start -= chart.gridStep
			while start <= volMax:
				if start > volMin:
					hAxisY = getChartY(chart, 1, start)
					if hAxisY < candleDivHeight or hAxisY > candleDivHeight + volDivHeight:
						start += chart.gridStep
						continue
					paint.fillRect(chart.gridColor, chart.leftVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth, int(hAxisY) + chart.lineWidthChart)
					paint.fillRect(chart.scaleColor, chart.leftVScaleWidth - 8, int(hAxisY), chart.leftVScaleWidth, int(hAxisY) + chart.lineWidthChart)
					paint.fillRect(chart.scaleColor, chart.size.cx - chart.rightVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth + 8, int(hAxisY) + chart.lineWidthChart)
					drawText = toFixed((start/chart.magnitude), chart.volDigit)
					tSize = paint.textSize(drawText, chart.font)
					paint.drawText(drawText, chart.textColor, chart.font, chart.size.cx - chart.rightVScaleWidth + 10, int(hAxisY) - tSize.cy / 2)
					paint.drawText(drawText, chart.textColor, chart.font, chart.leftVScaleWidth - tSize.cx - 10, int(hAxisY) - tSize.cy / 2)
				start += chart.gridStep
		if indDivHeight > 0:
			topPoint = FCPoint(0, candleDivHeight + volDivHeight + 10)
			bottomPoint = FCPoint(0, candleDivHeight + volDivHeight + indDivHeight - 10)
			indMax = getChartValue(chart, topPoint)
			indMin = getChartValue(chart, bottomPoint)
			ret = chartGridScale(chart, indMin, indMax, (indDivHeight - chart.indPaddingTop - chart.indPaddingBottom) / 2, chart.vScaleDistance, chart.vScaleDistance / 2, int((indDivHeight - chart.indPaddingTop - chart.indPaddingBottom) / chart.vScaleDistance))
			if chart.gridStep > 0 and ret > 0:
				start = 0
				if indMin >= 0:
					while start + chart.gridStep < indMin:
						start += chart.gridStep
				else:
					while start - chart.gridStep > indMin:
						start -= chart.gridStep
				while start <= indMax:
					if start > indMin:
						hAxisY = getChartY(chart, 2, start)
						if hAxisY < candleDivHeight + volDivHeight or hAxisY > candleDivHeight + volDivHeight + indDivHeight:
							start += chart.gridStep
							continue
						paint.fillRect(chart.gridColor, chart.leftVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth, int(hAxisY) + chart.lineWidthChart)
						paint.fillRect(chart.scaleColor, chart.leftVScaleWidth - 8, int(hAxisY), chart.leftVScaleWidth, int(hAxisY) + chart.lineWidthChart)
						paint.fillRect(chart.scaleColor, chart.size.cx - chart.rightVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth + 8, int(hAxisY) + chart.lineWidthChart)
						drawText = toFixed(start, chart.indDigit)
						tSize = paint.textSize(drawText, chart.font)
						paint.drawText(drawText, chart.textColor, chart.font, chart.size.cx - chart.rightVScaleWidth + 10, int(hAxisY) - tSize.cy / 2)
						paint.drawText(drawText, chart.textColor, chart.font, chart.leftVScaleWidth - tSize.cx - 10, int(hAxisY) - tSize.cy / 2)
					start += chart.gridStep
		if indDivHeight2 > 0:
			topPoint = FCPoint(0, candleDivHeight + volDivHeight + indDivHeight + 10)
			bottomPoint = FCPoint(0, candleDivHeight + volDivHeight + indDivHeight + indDivHeight2 - 10)
			indMax2 = getChartValue(chart, topPoint)
			indMin2 = getChartValue(chart, bottomPoint)
			ret = chartGridScale(chart, indMin2, indMax2, (indDivHeight2 - chart.indPaddingTop2 - chart.indPaddingBottom2) / 2, chart.vScaleDistance, chart.vScaleDistance / 2, int((indDivHeight2 - chart.indPaddingTop2 - chart.indPaddingBottom2) / chart.vScaleDistance))
			if chart.gridStep > 0 and ret > 0:
				start = 0
				if indMin2 >= 0:
					while start + chart.gridStep < indMin2:
						start += chart.gridStep
				else:
					while start - chart.gridStep > indMin2:
						start -= chart.gridStep 
				while start <= indMax2:
					if start > indMin2:
						hAxisY = getChartY(chart, 3, start)
						if hAxisY < candleDivHeight + volDivHeight + indDivHeight or hAxisY > candleDivHeight + volDivHeight + indDivHeight + indDivHeight2:
							start += chart.gridStep
							continue
						paint.fillRect(chart.gridColor, chart.leftVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth, int(hAxisY) + chart.lineWidthChart)
						paint.fillRect(chart.scaleColor, chart.leftVScaleWidth - 8, int(hAxisY), chart.leftVScaleWidth, int(hAxisY) + chart.lineWidthChart)
						paint.fillRect(chart.scaleColor, chart.size.cx - chart.rightVScaleWidth, int(hAxisY), chart.size.cx - chart.rightVScaleWidth + 8, int(hAxisY) + chart.lineWidthChart)
						drawText = toFixed(start, chart.indDigit)
						tSize = paint.textSize(drawText, chart.font)
						paint.drawText(drawText, chart.textColor, chart.font, chart.size.cx - chart.rightVScaleWidth + 10, int(hAxisY) - tSize.cy / 2)
						paint.drawText(drawText, chart.textColor, chart.font, chart.leftVScaleWidth - tSize.cx - 10, int(hAxisY) - tSize.cy / 2)
					start += chart.gridStep
		if chart.onPaintChartHScale != None:
			chart.onPaintChartHScale(chart, paint, clipRect)
		elif paint.onPaintChartHScale != None:
			paint.onPaintChartHScale(chart, paint, clipRect)
		else:
			if chart.data != None and len(chart.data) > 0 and chart.hScaleHeight > 0:
				dLeft = chart.leftVScaleWidth + 10
				i = chart.firstVisibleIndex
				while i <= chart.lastVisibleIndex:
					xText = ""
					if len(chart.hScaleFormat) > 0:
						timeArray = time.localtime(chart.data[i].date)
						xText = time.strftime(chart.hScaleFormat, timeArray)
					else:
						if chart.cycle == "day":
							timeArray = time.localtime(chart.data[i].date)
							xText = time.strftime("%Y-%m-%d", timeArray)
						elif chart.cycle == "minute":
							timeArray = time.localtime(chart.data[i].date)
							xText = time.strftime("%Y-%m-%d %H:%M", timeArray)
						elif chart.cycle == "trend":
							timeArray = time.localtime(chart.data[i].date)
							xText = time.strftime("%H:%M", timeArray)
						elif chart.cycle == "second":
							timeArray = time.localtime(chart.data[i].date)
							xText = time.strftime("%H:%M:%S", timeArray)
						elif chart.cycle == "tick":
							xText = str(i + 1)
					tSize = paint.textSize(xText, chart.font)
					x = getChartX(chart, i)
					dx = x - tSize.cx / 2
					if dx > dLeft and dx < chart.size.cx - chart.rightVScaleWidth - 10:
						paint.drawLine(chart.scaleColor, chart.lineWidthChart, 0, x, chart.size.cy - chart.hScaleHeight, x, chart.size.cy - chart.hScaleHeight + 8)
						paint.drawText(xText, chart.textColor, chart.font, dx, chart.size.cy - chart.hScaleHeight + 8  - tSize.cy / 2 + 7)
						i = i + int((tSize.cx + chart.hScaleTextDistance) / chart.hScalePixel) + 1
					else:
						i = i + 1

#绘制十字线
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
def drawChartCrossLine(chart, paint, clipRect):
	if chart.data == None or len(chart.data) == 0:
		return
	candleDivHeight = getCandleDivHeight(chart)
	volDivHeight = getVolDivHeight(chart)
	indDivHeight = getIndDivHeight(chart)
	indDivHeight2 = getIndDivHeight2(chart)
	crossLineIndex = chart.crossStopIndex
	if crossLineIndex == -1 or chart.showCrossLine == False:
		if chart.lastValidIndex != -1:
			crossStopIndex = hart.lastValidIndex
		else:
			crossLineIndex = chart.lastVisibleIndex
	if crossLineIndex == -1:
		return
	if volDivHeight > 0:
		drawTitles = []
		drawColors = []
		if len(chart.data) > 0:
			drawTitles.append("VOL " + toFixed(chart.data[crossLineIndex].volume / chart.magnitude, chart.volDigit))
			drawColors.append(chart.textColor)
		else:
			drawTitles.append("VOL")
			drawColors.append(chart.textColor)
		if len(chart.shapes) > 0:
			for i in range(0, len(chart.shapes)):
				shape = chart.shapes[i]
				if shape.divIndex == 1:
					if len(shape.title) > 0:
						if shape.shapeType == "bar"  and shape.style == "2color":
							drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.volDigit))
							drawColors.append(shape.color2)
						else:
							if shape.shapeType != "text":
								drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.volDigit))
								drawColors.append(shape.color)
								if len(shape.datas2) > 0:
									drawTitles.append(shape.title2 + " " + toFixed(shape.datas2[crossLineIndex], chart.volDigit))
									drawColors.append(shape.color2)
						
					
		iLeft = chart.leftVScaleWidth + 5
		for i in range(0,len(drawTitles)):
			tSize = paint.textSize(drawTitles[i], chart.font)
			paint.drawText(drawTitles[i], drawColors[i], chart.font, iLeft, candleDivHeight + 5)
			iLeft += tSize.cx + 5
	if chart.cycle == "trend":
		drawTitles = []
		drawColors = []
		if len(chart.text) > 0:
			drawTitles.append(chart.text)
			drawColors.append(chart.textColor)
		if len(chart.data) > 0:
			drawTitles.append("CLOSE" + toFixed(chart.data[crossLineIndex].close, chart.candleDigit))
			drawColors.append(chart.textColor)
		else:
			drawTitles.append("CLOSE")
			drawColors.append(chart.textColor)
		iLeft = chart.leftVScaleWidth + 5
		if len(chart.shapes) > 0:
			for i in range(0, len(chart.shapes)):
				shape = chart.shapes[i]
				if shape.divIndex == 0:
					if len(shape.title) > 0:
						if shape.shapeType == "bar"  and shape.style == "2color":
							drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.candleDigit))
							drawColors.append(shape.color2)
						else:
							if shape.shapeType != "text":
								drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.candleDigit))
								drawColors.append(shape.color)
								if len(shape.datas2) > 0:
									drawTitles.append(shape.title2 + " " + toFixed(shape.datas2[crossLineIndex], chart.candleDigit))
									drawColors.append(shape.color2)
		for i in range(0,len(drawTitles)):
			tSize = paint.textSize(drawTitles[i], chart.font)
			paint.drawText(drawTitles[i], drawColors[i], chart.font, iLeft, 5)
			iLeft += tSize.cx + 5
	else:
		drawTitles = []
		drawColors = []
		if len(chart.text) > 0:
			drawTitles.append(chart.text)
			drawColors.append(chart.textColor)
		if chart.mainIndicator == "MA":
			if len(chart.ma5) > 0:
				drawTitles.append("MA5 " + toFixed(chart.ma5[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MA5")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.ma10) > 0:
				drawTitles.append("MA10 " + toFixed(chart.ma10[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MA10")
			drawColors.append(chart.indicatorColors[1])
			if len(chart.ma20) > 0:
				drawTitles.append("MA20 " + toFixed(chart.ma20[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MA20")
			drawColors.append(chart.indicatorColors[2])
			if len(chart.ma30) > 0:
				drawTitles.append("MA30 " + toFixed(chart.ma30[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MA30")
			drawColors.append(chart.indicatorColors[5])
			if len(chart.ma120) > 0:
				drawTitles.append("MA120 " + toFixed(chart.ma120[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MA120")
			drawColors.append(chart.indicatorColors[4])
			if len(chart.ma250) > 0:
				drawTitles.append("MA250 " + toFixed(chart.ma250[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MA250")
			drawColors.append(chart.indicatorColors[3])
		elif chart.mainIndicator == "BOLL":
			if len(chart.boll_mid) > 0:
				drawTitles.append("MID " + toFixed(chart.boll_mid[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("MID")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.boll_up) > 0:
				drawTitles.append("UP " + toFixed(chart.boll_up[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("UP")
			drawColors.append(chart.indicatorColors[1])
			if len(chart.boll_down) > 0:
				drawTitles.append("LOW " + toFixed(chart.boll_down[crossLineIndex], chart.candleDigit))
			else:
				drawTitles.append("LOW")
			drawColors.append(chart.indicatorColors[2])
		if len(chart.shapes) > 0:
			for i in range(0, len(chart.shapes)):
				shape = chart.shapes[i]
				if shape.divIndex == 0:
					if len(shape.title) > 0:
						if shape.shapeType == "bar" and shape.style == "2color":
							drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.candleDigit))
							drawColors.append(shape.color2)
						else:
							if shape.shapeType != "text":
								drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.candleDigit))
								drawColors.append(shape.color)
								if len(shape.datas2) > 0:
									drawTitles.append(shape.title2 + " " + toFixed(shape.datas2[crossLineIndex], chart.candleDigit))
									drawColors.append(shape.color2)
		iLeft = chart.leftVScaleWidth + 5
		for i in range(0, len(drawTitles)):
			tSize = paint.textSize(drawTitles[i], chart.font)
			paint.drawText(drawTitles[i], drawColors[i], chart.font, iLeft, 5)
			iLeft += tSize.cx + 5
	if indDivHeight > 0:
		drawTitles = []
		drawColors = []
		if chart.showIndicator == "MACD":
			if len(chart.alldifarr) > 0:
				drawTitles.append("DIF " + toFixed(chart.alldifarr[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("DIF")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.alldeaarr) > 0:
				drawTitles.append("DEA " + toFixed(chart.alldeaarr[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("DEA")
			drawColors.append(chart.indicatorColors[1])
			if len(chart.allmacdarr) > 0:
				drawTitles.append("MACD " + toFixed(chart.allmacdarr[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("MACD")
			drawColors.append(chart.indicatorColors[4])
		elif chart.showIndicator == "KDJ":
			if len(chart.kdj_k) > 0:
				drawTitles.append("K " + toFixed(chart.kdj_k[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("K")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.kdj_d) > 0:
				drawTitles.append("D " + toFixed(chart.kdj_d[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("D")
			drawColors.append(chart.indicatorColors[1])
			if len(chart.kdj_j) > 0:
				drawTitles.append("J " + toFixed(chart.kdj_j[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("J")
			drawColors.append(chart.indicatorColors[2])
		elif chart.showIndicator == "RSI":
			if len(chart.rsi1) > 0:
				drawTitles.append("RSI6 " + toFixed(chart.rsi1[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("RSI6")
			drawColors.append(chart.indicatorColors[5])
			if len(chart.rsi2) > 0:
				drawTitles.append("RSI12 " + toFixed(chart.rsi2[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("RSI12")
			drawColors.append(chart.indicatorColors[1])
			if len(chart.rsi3) > 0:
				drawTitles.append("RSI24 " + toFixed(chart.rsi3[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("RSI24")
			drawColors.append(chart.indicatorColors[2])
		elif chart.showIndicator == "BIAS":
			if len(chart.bias1) > 0:
				drawTitles.append("BIAS6 " + toFixed(chart.bias1[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("BIAS6")
			drawColors.append(chart.indicatorColors[5])
			if len(chart.bias2) > 0:
				drawTitles.append("BIAS12 " + toFixed(chart.bias2[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("BIAS12")
			drawColors.append(chart.indicatorColors[1])
			if len(chart.bias3) > 0:
				drawTitles.append("BIAS24 " + toFixed(chart.bias3[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("BIAS24")
			drawColors.append(chart.indicatorColors[2])
		elif chart.showIndicator == "ROC":
			if len(chart.roc) > 0:
				drawTitles.append("ROC " + toFixed(chart.roc[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("ROC")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.roc_ma) > 0:
				drawTitles.append("ROCMA " + toFixed(chart.roc_ma[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("ROCMA")
			drawColors.append(chart.indicatorColors[1])       
		elif chart.showIndicator == "WR":
			if len(chart.wr1) > 0:
				drawTitles.append("WR5 " + toFixed(chart.wr1[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("WR5")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.wr2) > 0:
				drawTitles.append("WR10 " + toFixed(chart.wr2[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("WR10")
			drawColors.append(chart.indicatorColors[1])
		elif chart.showIndicator == "CCI":
			if len(chart.cci) > 0:
				drawTitles.append("CCI " + toFixed(chart.cci[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("CCI")
			drawColors.append(chart.indicatorColors[0])
		elif chart.showIndicator == "BBI":
			if len(chart.bbi) > 0:
				drawTitles.append("BBI " + toFixed(chart.bbi[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("BBI")
			drawColors.append(chart.indicatorColors[0])
		elif chart.showIndicator == "TRIX":
			if len(chart.trix) > 0:
				drawTitles.append("TRIX " + toFixed(chart.trix[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("TRIX")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.trix_ma) > 0:
				drawTitles.append("TRIXMA " + toFixed(chart.trix_ma[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("TRIXMA")
			drawColors.append(chart.indicatorColors[1])
		elif chart.showIndicator == "DMA":
			if len(chart.dma1) > 0:
				drawTitles.append("MA10 " + toFixed(chart.dma1[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("MA10")
			drawColors.append(chart.indicatorColors[0])
			if len(chart.dma2) > 0:
				drawTitles.append("MA50 " + toFixed(chart.dma2[crossLineIndex], chart.indDigit))
			else:
				drawTitles.append("MA50")
			drawColors.append(chart.indicatorColors[1])
		if len(chart.shapes) > 0:
			for i in range(0, len(chart.shapes)):
				shape = chart.shapes[i]
				if shape.divIndex == 2:
					if len(shape.title) > 0:
						if shape.shapeType == "bar"  and shape.style == "2color":
							drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.indDigit))
							drawColors.append(shape.color2)
						else:
							if shape.shapeType != "text":
								drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.indDigit))
								drawColors.append(shape.color)
								if len(shape.datas2) > 0:
									drawTitles.append(shape.title2 + " " + toFixed(shape.datas2[crossLineIndex], chart.indDigit))
									drawColors.append(shape.color2)
		iLeft = chart.leftVScaleWidth + 5
		for i in range(0,len(drawTitles)):
			tSize = paint.textSize(drawTitles[i], chart.font)
			paint.drawText(drawTitles[i], drawColors[i], chart.font, iLeft, candleDivHeight + volDivHeight + 5)
			iLeft += tSize.cx + 5
	if indDivHeight2 > 0:
		drawTitles = []
		drawColors = []
		if len(chart.shapes) > 0:
			for i in range(0, len(chart.shapes)):
				shape = chart.shapes[i]
				if shape.divIndex == 3:
					if len(shape.title) > 0:
						if shape.shapeType == "bar"  and shape.style == "2color":
							drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.indDigit2))
							drawColors.append(shape.color2)
						else:
							if shape.shapeType != "text":
								drawTitles.append(shape.title + " " + toFixed(shape.datas[crossLineIndex], chart.indDigit2))
								drawColors.append(shape.color)
								if len(shape.datas2) > 0:
									drawTitles.append(shape.title2 + " " + toFixed(shape.datas2[crossLineIndex], chart.indDigit2))
									drawColors.append(shape.color2)
			if len(drawTitles) > 0:
				iLeft = chart.leftVScaleWidth + 5
				for i in range(0,len(drawTitles)):
					tSize = paint.textSize(drawTitles[i], chart.font)
					paint.drawText(drawTitles[i], drawColors[i], chart.font, iLeft, candleDivHeight + volDivHeight + indDivHeight + 5)
					iLeft += tSize.cx + 5
	if chart.showCrossLine:
		rightText = ""
		if chart.touchPosition.y < candleDivHeight:
			rightText = toFixed(getChartValue(chart, chart.touchPosition), chart.candleDigit)	
		elif chart.touchPosition.y > candleDivHeight and chart.touchPosition.y < candleDivHeight + volDivHeight:
			rightText = toFixed(getChartValue(chart, chart.touchPosition) / chart.magnitude, chart.volDigit)
		elif chart.touchPosition.y > candleDivHeight + volDivHeight and chart.touchPosition.y < candleDivHeight + volDivHeight + indDivHeight:
			rightText = toFixed(getChartValue(chart, chart.touchPosition), chart.indDigit)
		elif chart.touchPosition.y > candleDivHeight + volDivHeight + indDivHeight and chart.touchPosition.y < candleDivHeight + volDivHeight + indDivHeight + indDivHeight2:
			rightText = toFixed(getChartValue(chart, chart.touchPosition), chart.indDigit2)
		drawY = chart.touchPosition.y
		if drawY > chart.size.cy - chart.hScaleHeight:
			drawY = chart.size.cy - chart.hScaleHeight
		tSize = paint.textSize(rightText, chart.font)
		if chart.leftVScaleWidth > 0:
			paint.fillRect(chart.crossTipColor, chart.leftVScaleWidth - tSize.cx, drawY - tSize.cy / 2 - 4, chart.leftVScaleWidth, drawY + tSize.cy / 2 + 3)
			paint.drawText(rightText, chart.textColor, chart.font, chart.leftVScaleWidth - tSize.cx, drawY - tSize.cy / 2)
		if chart.rightVScaleWidth > 0:
			paint.fillRect(chart.crossTipColor, chart.size.cx - chart.rightVScaleWidth, drawY - tSize.cy / 2 - 4, chart.size.cx - chart.rightVScaleWidth + tSize.cx, drawY + tSize.cy / 2 + 3)
			paint.drawText(rightText, chart.textColor, chart.font, chart.size.cx - chart.rightVScaleWidth, drawY - tSize.cy / 2)
		drawX = getChartX(chart, chart.crossStopIndex)
		if chart.targetOldX == 0 and chart.targetOldX2 == 0:
			drawX = chart.touchPosition.x
		if drawX < chart.leftVScaleWidth:
			drawX = chart.leftVScaleWidth
		if drawX > chart.size.cx - chart.rightVScaleWidth:
			drawX = chart.size.cx - chart.rightVScaleWidth
		if chart.sPlot == None and chart.selectShape == "":
			paint.fillRect(chart.crossLineColor, chart.leftVScaleWidth, drawY, chart.size.cx - chart.rightVScaleWidth, drawY + chart.lineWidthChart)
			paint.fillRect(chart.crossLineColor, drawX, 0, drawX + chart.lineWidthChart, chart.size.cy - chart.hScaleHeight)
		if chart.crossStopIndex != -1:
			xText = ""
			if chart.cycle == "day":
				timeArray = time.localtime(chart.data[chart.crossStopIndex].date)
				xText = time.strftime("%Y-%m-%d", timeArray)
			elif chart.cycle == "minute":
				timeArray = time.localtime(chart.data[chart.crossStopIndex].date)
				xText = time.strftime("%Y-%m-%d %H:%M", timeArray)
			elif chart.cycle == "trend":
				timeArray = time.localtime(chart.data[chart.crossStopIndex].date)
				xText = time.strftime("%H:%M", timeArray)
			elif chart.cycle == "second":
				timeArray = time.localtime(chart.data[chart.crossStopIndex].date)
				xText = time.strftime("%H:%M:%S", timeArray)
			elif chart.cycle == "tick":
				xText = str(chart.crossStopIndex + 1)
			if len(chart.hScaleFormat) > 0:
				timeArray = time.localtime(chart.data[chart.crossStopIndex].date)
				xText = time.strftime(chart.hScaleFormat, timeArray)
			xSize = paint.textSize(xText, chart.font)
			paint.fillRect(chart.crossTipColor, drawX - xSize.cx / 2 - 2, candleDivHeight + volDivHeight + indDivHeight, drawX + xSize.cx / 2 + 2, candleDivHeight + volDivHeight + indDivHeight + xSize.cy + 6)
			paint.drawText(xText, chart.textColor, chart.font, drawX - xSize.cx / 2, candleDivHeight + volDivHeight + indDivHeight + 3)

#绘制图表
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
def drawChartStock(chart, paint, clipRect):
	if chart.data != None and len(chart.data) > 0:
		candleHeight = getCandleDivHeight(chart)
		volHeight = getVolDivHeight(chart)
		indHeight = getIndDivHeight(chart)
		isTrend = False
		if chart.cycle == "trend":
			isTrend = True
		cWidth = int(chart.hScalePixel - 3) / 2
		if cWidth < 0:
			cWidth = 0
		lastValidIndex = chart.lastVisibleIndex
		if chart.lastValidIndex != -1:
			lastValidIndex = chart.lastValidIndex
		maxVisibleRecord = getChartMaxVisibleCount(chart, chart.hScalePixel, getChartWorkAreaWidth(chart))
		divHeight = getCandleDivHeight(chart)
		paint.setClip(chart.leftVScaleWidth, 0, chart.size.cx, divHeight)
		if isTrend:
			drawPoints = []
			for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
				x = getChartX(chart, i)
				close = chart.data[i].close
				closeY = getChartY(chart, 0, close)
				drawPoints.append(FCPoint(x, closeY))
			paint.drawPolyline(chart.indicatorColors[7], chart.lineWidthChart, 0, drawPoints)
		hasMinTag = False
		hasMaxTag = False
		for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
			x = getChartX(chart, i)
			openValue = chart.data[i].open
			close = chart.data[i].close
			high = chart.data[i].high
			low = chart.data[i].low
			openY = getChartY(chart, 0, openValue)
			closeY = getChartY(chart, 0, close)
			highY = getChartY(chart, 0, high)
			lowY = getChartY(chart, 0, low)
			if close >= openValue:
				if isTrend == False:
					paint.fillRect(chart.upColor, x, highY, x + chart.lineWidthChart, lowY)
					if cWidth > 0:
						if close == openValue:
							paint.fillRect(chart.upColor, x - cWidth, closeY, x + cWidth, closeY + chart.lineWidthChart)
						else:
							if chart.candleStyle == "rect2":
								paint.fillRect(chart.backColor, x - cWidth, closeY, x + cWidth + 1, openY)
								paint.drawRect(chart.upColor, 1, 0, x - cWidth, closeY, x + cWidth + 1, openY)
							else:
								paint.fillRect(chart.upColor, x - cWidth, closeY, x + cWidth + 1, openY)
			else:
				if isTrend == False:
					paint.fillRect(chart.downColor, x, highY, x + chart.lineWidthChart, lowY)
					if cWidth > 0:
						paint.fillRect(chart.downColor, x - cWidth, openY, x + cWidth + 1, closeY)
			if chart.selectShape == "CANDLE":
				kPInterval = int(maxVisibleRecord / 30)
				if kPInterval < 2:
					kPInterval = 3
				if i % kPInterval == 0:
					if isTrend == False:
						paint.fillRect(chart.indicatorColors[0], x - 3, closeY - 3, x + 3, closeY + 3)
			if isTrend == False:
				if hasMaxTag == False:
					if high == chart.candleMax:
						tag = toFixed(high, chart.candleDigit)
						tSize = paint.textSize(tag, chart.font)
						paint.drawText(tag, chart.textColor, chart.font, x - tSize.cx / 2, highY - tSize.cy - 2)
						hasMaxTag = True
				if hasMinTag == False:
					if low == chart.candleMin:
						tag = toFixed(low, chart.candleDigit)
						tSize = paint.textSize(tag, chart.font)
						paint.drawText(tag, chart.textColor, chart.font, x - tSize.cx / 2, lowY + 2)
						hasMinTag = True
		paint.setClip(0, 0, chart.size.cx, chart.size.cy)
		for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
			x = getChartX(chart, i)
			openValue = chart.data[i].open
			close = chart.data[i].close
			openY = getChartY(chart, 0, openValue)
			closeY = getChartY(chart, 0, close)
			volY = 0
			zeroY = 0
			if volHeight > 0:
				volume = chart.data[i].volume
				volY = getChartY(chart, 1, volume)
				zeroY = getChartY(chart, 1, 0) 
			if close >= openValue:
				if isTrend:
					if volHeight > 0:
						paint.fillRect(chart.indicatorColors[6], x, volY, x + chart.lineWidthChart, zeroY)
				else:
					if cWidth > 0:
						if volHeight > 0:
							if chart.barStyle == "rect2":
								paint.fillRect(chart.backColor, x - cWidth, volY, x + cWidth + 1, zeroY)
								paint.drawRect(chart.upColor, 1, 0, x - cWidth, volY, x + cWidth + 1, zeroY)
							else:
								paint.fillRect(chart.upColor, x - cWidth, volY, x + cWidth + 1, zeroY)
					else:
						if volHeight > 0:
							paint.drawLine(chart.upColor, chart.lineWidthChart, 0, x - cWidth, volY, x + cWidth, zeroY)
			else:
				if isTrend:
					if volHeight > 0:
						paint.fillRect(chart.indicatorColors[6], x, volY, x + chart.lineWidthChart, zeroY)
				else:
					if cWidth > 0:
						if volHeight > 0:
							paint.fillRect(chart.downColor, x - cWidth, volY, x + cWidth + 1, zeroY)
					else:
						if volHeight > 0:
							paint.drawLine(chart.downColor, chart.lineWidthChart, 0, x - cWidth, volY, x + cWidth, zeroY)
			if chart.selectShape == "VOL":
				kPInterval = int(maxVisibleRecord / 30)
				if kPInterval < 2:
					kPInterval = 3
				if i % kPInterval == 0:
					paint.fillRect(chart.indicatorColors[0], x - 3, volY - 3, x + 3, volY + 3)
		if isTrend == False:
			divHeight = getCandleDivHeight(chart)
			paint.setClip(chart.leftVScaleWidth, 0, chart.size.cx, divHeight)
			if chart.mainIndicator == "BOLL":
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "MID":
					drawChartLines(chart, paint, clipRect, 0, chart.boll_mid, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.boll_mid, chart.indicatorColors[0], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "UP":
					drawChartLines(chart, paint, clipRect, 0, chart.boll_up, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.boll_up, chart.indicatorColors[1], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "DOWN":
					drawChartLines(chart, paint, clipRect, 0, chart.boll_down, chart.indicatorColors[2], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.boll_down, chart.indicatorColors[2], False)
			elif chart.mainIndicator == "MA":
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "5":
					drawChartLines(chart, paint, clipRect, 0, chart.ma5, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.ma5, chart.indicatorColors[0], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "10":
					drawChartLines(chart, paint, clipRect, 0, chart.ma10, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.ma10, chart.indicatorColors[1], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "20":
					drawChartLines(chart, paint, clipRect, 0, chart.ma20, chart.indicatorColors[2], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.ma20, chart.indicatorColors[2], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "30":
					drawChartLines(chart, paint, clipRect, 0, chart.ma30, chart.indicatorColors[3], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.ma30, chart.indicatorColors[3], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "120":
					drawChartLines(chart, paint, clipRect, 0, chart.ma120, chart.indicatorColors[4], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.ma120, chart.indicatorColors[4], False)
				if chart.selectShape == chart.mainIndicator and chart.selectShapeEx == "250":
					drawChartLines(chart, paint, clipRect, 0, chart.ma250, chart.indicatorColors[5], True)
				else:
					drawChartLines(chart, paint, clipRect, 0, chart.ma250, chart.indicatorColors[5], False)
			paint.setClip(0, 0, chart.size.cx, chart.size.cy)
		if indHeight > 0:
			if chart.showIndicator == "MACD":
				zeroY = getChartY(chart, 2, 0)
				paint.fillRect(chart.indicatorColors[4], chart.leftVScaleWidth, zeroY, getChartX(chart, chart.lastVisibleIndex), zeroY + chart.lineWidthChart)
				for i in range(chart.firstVisibleIndex,lastValidIndex + 1):
					x = getChartX(chart, i)
					macd = chart.allmacdarr[i]
					macdY = getChartY(chart, 2, macd)
					if macdY < zeroY:
						paint.fillRect(chart.indicatorColors[3], x, macdY, x + chart.lineWidthChart, zeroY)
					else:
						paint.fillRect(chart.indicatorColors[4], x, zeroY, x + chart.lineWidthChart, macdY)
					if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "MACD":
						kPInterval = int(maxVisibleRecord / 30)
						if kPInterval < 2:
							kPInterval = 3
						if i % kPInterval == 0:
							paint.fillRect(chart.indicatorColors[4], x - 3, macdY - 3, x + 3, macdY + 3)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "DIF":
					drawChartLines(chart, paint, clipRect, 2, chart.alldifarr, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.alldifarr, chart.indicatorColors[0], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "DEA":
					drawChartLines(chart, paint, clipRect, 2, chart.alldeaarr, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.alldeaarr, chart.indicatorColors[1], False)
			elif chart.showIndicator == "KDJ":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "K":
					drawChartLines(chart, paint, clipRect, 2, chart.kdj_k, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.kdj_k, chart.indicatorColors[0], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "D":
					drawChartLines(chart, paint, clipRect, 2, chart.kdj_d, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.kdj_d, chart.indicatorColors[1], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "J":
					drawChartLines(chart, paint, clipRect, 2, chart.kdj_j, chart.indicatorColors[2], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.kdj_j, chart.indicatorColors[2], False)
			elif chart.showIndicator == "RSI":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "6":
					drawChartLines(chart, paint, clipRect, 2, chart.rsi1, chart.indicatorColors[5], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.rsi1, chart.indicatorColors[5], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "12":
					drawChartLines(chart, paint, clipRect, 2, chart.rsi2, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.rsi2, chart.indicatorColors[1], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "24":
					drawChartLines(chart, paint, clipRect, 2, chart.rsi3, chart.indicatorColors[2], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.rsi3, chart.indicatorColors[2], False)
			elif chart.showIndicator == "BIAS":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "1":
					drawChartLines(chart, paint, clipRect, 2, chart.bias1, chart.indicatorColors[5], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.bias1, chart.indicatorColors[5], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "2":
					drawChartLines(chart, paint, clipRect, 2, chart.bias2, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.bias2, chart.indicatorColors[1], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "3":
					drawChartLines(chart, paint, clipRect, 2, chart.bias3, chart.indicatorColors[2], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.bias3, chart.indicatorColors[2], False)
			elif chart.showIndicator == "ROC":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "ROC":
					drawChartLines(chart, paint, clipRect, 2, chart.roc, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.roc, chart.indicatorColors[0], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "ROCMA":
					drawChartLines(chart, paint, clipRect, 2, chart.roc_ma, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.roc_ma, chart.indicatorColors[1], False)
			elif chart.showIndicator == "WR":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "1":
					drawChartLines(chart, paint, clipRect, 2, chart.wr1, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.wr1, chart.indicatorColors[0], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "2":
					drawChartLines(chart, paint, clipRect, 2, chart.wr2, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.wr2, chart.indicatorColors[1], False)
			elif chart.showIndicator == "CCI":
				if chart.selectShape == chart.showIndicator:
					drawChartLines(chart, paint, clipRect, 2, chart.cci, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.cci, chart.indicatorColors[0], False)
			elif chart.showIndicator == "BBI":
				if chart.selectShape == chart.showIndicator:
					drawChartLines(chart, paint, clipRect, 2, chart.bbi, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.bbi, chart.indicatorColors[0], False)
			elif chart.showIndicator == "TRIX":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "TRIX":
					drawChartLines(chart, paint, clipRect, 2, chart.trix, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.trix, chart.indicatorColors[0], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "TRIXMA":
					drawChartLines(chart, paint, clipRect, 2, chart.trix_ma, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.trix_ma, chart.indicatorColors[1], False)
			elif chart.showIndicator == "DMA":
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "DIF":
					drawChartLines(chart, paint, clipRect, 2, chart.dma1, chart.indicatorColors[0], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.dma1, chart.indicatorColors[0], False)
				if chart.selectShape == chart.showIndicator and chart.selectShapeEx == "DIFMA":
					drawChartLines(chart, paint, clipRect, 2, chart.dma2, chart.indicatorColors[1], True)
				else:
					drawChartLines(chart, paint, clipRect, 2, chart.dma2, chart.indicatorColors[1], False)
	#绘制扩展线条
	if len(chart.shapes) > 0:
		for i in range(0, len(chart.shapes)):
			shape = chart.shapes[i]
			if shape.shapeType == "bar":
				for j in range(chart.firstVisibleIndex,lastValidIndex + 1):
					if len(shape.showHideDatas) > j and str(shape.showHideDatas[j]) == "0":
						continue
					x = getChartX(chart, j)
					y1 = 0
					if shape.leftOrRight:
						y1 = getChartY(chart, shape.divIndex, shape.datas[j])
					else:
						y1 = getChartYInRight(chart, shape.divIndex, shape.datas[j])
					if shape.style != "2color":
						y2 = 0
						if shape.leftOrRight:
							y2 = getChartY(chart, shape.divIndex, shape.datas2[j])
						else:
							y2 = getChartYInRight(chart, shape.divIndex, shape.datas2[j])
						if y1 >= y2:
							paint.fillRect(shape.color, x - cWidth, y2, x + cWidth, y1)
						else:
							paint.fillRect(shape.color, x - cWidth, y1, x + cWidth, y2)
					else:
						if shape.leftOrRight:
							y2 = 0
							y2 = getChartY(chart, shape.divIndex, 0)
						else:
							y2 = getChartYInRight(chart, shape.divIndex, 0)
						if y1 >= y2:
							paint.drawLine(shape.color2, 1, 0, x, y1, x, y2)
						else:
							paint.drawLine(shape.color, 1, 0, x, y1, x, y2)
						if j == lastValidIndex:
							paint.drawLine(shape.color2, 1, 0, chart.leftVScaleWidth, y2, chart.size.cx - chart.rightVScaleWidth, y2)
			elif shape.shapeType == "text":
				for j in range(chart.firstVisibleIndex,lastValidIndex + 1):
					x = getChartX(chart, j)
					if shape.datas[j] != 0:
						y1 = 0
						if shape.leftOrRight:
							y1 = getChartY(chart, shape.divIndex, shape.value)
						else:
							y1 = getChartYInRight(chart, shape.divIndex, shape.value)
						drawText = shape.text
						tSize = paint.textSize(drawText, "Default,14")
						paint.drawText(drawText, shape.color, "Default,14", x - tSize.cx / 2, y1 - tSize.cy / 2)
			else:
				if shape.leftOrRight:
					if chart.selectShape == shape.shapeName:
						drawChartLines(chart, paint, clipRect, shape.divIndex, shape.datas, shape.color, True)
					else:
						drawChartLines(chart, paint, clipRect, shape.divIndex, shape.datas, shape.color, False)
				else:
					if chart.selectShape == shape.shapeName:
						drawChartLinesInRight(chart, paint, clipRect, shape.divIndex, shape.datas, shape.color, True)
					else:
						drawChartLinesInRight(chart, paint, clipRect, shape.divIndex, shape.datas, shape.color, False)

#清除图形
#chart:图表
#paint:绘图对象
#clipRect:裁剪区域
def drawChart(chart, paint, clipRect):
	if chart.backColor != "none":
		paint.fillRect(chart.backColor, 0, 0, chart.size.cx, chart.size.cy)
	if chart.onPaintChartScale != None:
		chart.onPaintChartScale(chart, paint, clipRect)
	elif paint.onPaintChartScale != None:
		paint.onPaintChartScale(chart, paint, clipRect)
	else:
		drawChartScale(chart, paint, clipRect)
	if chart.onPaintChartStock != None:
		chart.onPaintChartStock(chart, paint, clipRect)
	elif paint.onPaintChartStock != None:
		paint.onPaintChartStock(chart, paint, clipRect)
	else:
		drawChartStock(chart, paint, clipRect)
	if chart.onPaintChartPlot != None:
		chart.onPaintChartPlot(chart, paint, clipRect)
	elif paint.onPaintChartPlot != None:
		paint.onPaintChartPlot(chart, paint, clipRect)
	else:
		drawChartPlot(chart, paint, clipRect)
	if chart.onPaintChartCrossLine != None:
		chart.onPaintChartCrossLine(chart, paint, clipRect)
	elif paint.onPaintChartCrossLine != None:
		paint.onPaintChartCrossLine(chart, paint, clipRect)
	else:
		drawChartCrossLine(chart, paint, clipRect)
	if chart.borderColor != "none":
		paint.drawRect(chart.borderColor, chart.lineWidthChart, 0, 0, 0, chart.size.cx, chart.size.cy)

#重绘视图 
#views:视图集合 
#paint:绘图对象 
#rect:区域
def renderViews(views, paint, rect):
	size = len(views)
	for i in range(0, size):
		view = views[i]
		if rect == None:
			subViews = view.views
			subViewsSize = len(subViews)
			if subViewsSize > 0:
				renderViews(subViews, paint, None)
			view.clipRect = None
			continue
		if view.topMost == False and isPaintVisible(view) and view.allowDraw:
			clx = clientX(view)
			cly = clientY(view)
			drawRect = FCRect(0, 0, view.size.cx, view.size.cy)
			clipRect = FCRect(clx, cly, clx + view.size.cx, cly + view.size.cy)
			destRect = FCRect(0, 0, 0, 0)
			if getIntersectRect(destRect, rect, clipRect) > 0:
				view.clipRect = destRect
				paint.setOffset(clx, cly)
				clRect = FCRect(destRect.left - clx, destRect.top - cly, destRect.right - clx, destRect.bottom - cly)
				paint.setClip(destRect.left - clx, destRect.top - cly, destRect.right - clx, destRect.bottom - cly)
				if paint.onPaint != None:
					paint.onPaint(view, paint, rect)
				else:
					onPaintDefault(view, paint, rect)
				subViews = view.views
				subViewsSize = len(subViews)
				if subViewsSize > 0:
					renderViews(subViews, paint, destRect)
				paint.setOffset(clx, cly)
				paint.setClip(destRect.left - clx, destRect.top - cly, destRect.right - clx, destRect.bottom - cly)
				if paint.onPaintBorder != None:
					paint.onPaintBorder(view, paint, rect)
				else:
					onPaintBorderDefault(view, paint, rect)
			else:
				subViews = view.views
				subViewsSize = len(subViews)
				if subViewsSize > 0:
					renderViews(subViews, paint, None)
				view.clipRect = None
	for i in range(0, size):
		view = views[i]
		if rect == None:
			continue
		if view.topMost and isPaintVisible(view) and view.allowDraw:
			clx = clientX(view)
			cly = clientY(view)
			drawRect = FCRect(0, 0, view.size.cx, view.size.cy)
			clipRect = FCRect(clx, cly, clx + view.size.cx, cly + view.size.cy)
			destRect = FCRect(0, 0, 0, 0)
			if getIntersectRect(destRect, rect, clipRect) > 0:
				view.clipRect = destRect
				paint.setOffset(clx, cly)
				clRect = FCRect(destRect.left - clx, destRect.top - cly, destRect.right - clx, destRect.bottom - cly)
				paint.setClip(destRect.left - clx, destRect.top - cly, destRect.right - clx, destRect.bottom - cly)
				if paint.onPaint != None:
					paint.onPaint(view, paint, rect)
				else:
					onPaintDefault(view, paint, rect)
				subViews = view.views
				subViewsSize = len(subViews)
				if subViewsSize > 0:
					renderViews(subViews, paint, destRect)
				paint.setOffset(clx, cly)
				paint.setClip(destRect.left - clx, destRect.top - cly, destRect.right - clx, destRect.bottom - cly)
				if paint.onPaintBorder != None:
					paint.onPaintBorder(view, paint, rect)
				else:
					onPaintBorderDefault(view, paint, rect)
			else:
				subViews = view.views
				subViewsSize = len(subViews)
				if subViewsSize > 0:
					renderViews(subViews, paint, None)
				view.clipRect = None	

#全局刷新方法
#views:视图集合
#paint:绘图对象
def invalidate(paint):
	if paint.onInvalidate:
		paint.onInvalidate(paint)
	else:
		rect = RECT()
		rect.left = 0
		rect.top = 0
		rect.right = paint.size.cx
		rect.bottom = paint.size.cy
		user32.InvalidateRect(paint.hWnd, ct.byref(rect), True)

#刷新视图方法
#view:视图
def invalidateView(view):
	if view.paint.allowPartialPaint:
		if view.paint.onInvalidateView:
			view.paint.onInvalidateView(view)
		else:
			if isPaintVisible(view):
				paint = view.paint
				hDC = user32.GetDC(paint.hWnd)
				paint.hdc = hDC
				clX = clientX(view)
				clY = clientY(view)
				drawRect = FCRect(clX, clY, clX + view.size.cx, clY + view.size.cy)
				drawViews = paint.views
				paint.clipRect = drawRect
				allRect = FCRect(0, 0, paint.size.cx, paint.size.cy)
				if paint.gdiPlusPaint != None:
					paint.gdiPlusPaint.setScaleFactor(paint.scaleFactorX, paint.scaleFactorY)
				paint.beginPaint(allRect, drawRect)
				if paint.onRenderViews:
					paint.onRenderViews(drawViews, paint, drawRect)
				else:
					renderViews(drawViews, paint, drawRect)
				paint.endPaint()
				user32.ReleaseDC(paint.hWnd, hDC)
	else:
		invalidate(view.paint)

#更新悬浮状态
#views:视图集合
def updateViewDefault(views):
	for i in range(0,len(views)):
		view = views[i]
		if "leftstr" in view.exAttributes:
			pWidth = view.paint.size.cx / view.paint.scaleFactorX
			if view.parent != None:
				pWidth = view.parent.size.cx
			newStr = view.exAttributes["leftstr"].replace("%", "")
			view.location.x = int(float(newStr) * pWidth / 100)
		if "topstr" in view.exAttributes:
			pHeight = view.paint.size.cy / view.paint.scaleFactorY
			if view.parent != None:
				pHeight = view.parent.size.cy
			newStr = view.exAttributes["topstr"].replace("%", "")
			view.location.y = int(float(newStr) * pHeight / 100)
		if "widthstr" in view.exAttributes:
			pWidth = view.paint.size.cx / view.paint.scaleFactorX
			if view.parent != None:
				pWidth = view.parent.size.cx
			newStr = view.exAttributes["widthstr"].replace("%", "")
			view.size.cx = int(float(newStr) * pWidth / 100)
		if "heightstr" in view.exAttributes:
			pHeight = view.paint.size.cy / view.paint.scaleFactorY
			if view.parent != None:
				pHeight = view.parent.size.cy
			newStr = view.exAttributes["heightstr"].replace("%", "")
			view.size.cy = int(float(newStr) * pHeight / 100)
		if view.parent != None and view.parent.viewType != "split":
			margin = view.margin
			padding = view.parent.padding
			if view.dock == "fill":
				view.location = FCPoint(margin.left + padding.left, margin.top + padding.top)
				vcx = view.parent.size.cx - margin.left - padding.left - margin.right - padding.right
				if vcx < 0:
					vcx = 0
				vcy = view.parent.size.cy - margin.top - padding.top - margin.bottom - padding.bottom
				if vcy < 0:
					vcy = 0
				view.size = FCSize(vcx, vcy)
			elif view.dock == "left":
				view.location = FCPoint(margin.left + padding.left, margin.top + padding.top)
				vcy = view.parent.size.cy - margin.top - padding.top - margin.bottom - padding.bottom
				if vcy < 0:
					vcy = 0
				view.size = FCSize(view.size.cx, vcy)
			elif view.dock == "top":
				view.location = FCPoint(margin.left + padding.left, margin.top + padding.top)
				vcx = view.parent.size.cx - margin.left - padding.left - margin.right - padding.right
				if vcx < 0:
					vcx = 0
				view.size = FCSize(vcx, view.size.cy)
			elif view.dock == "right":
				view.location = FCPoint(view.parent.size.cx - view.size.cx - padding.right - margin.right, margin.top + padding.top)
				vcy = view.parent.size.cy - margin.top - padding.top - margin.bottom - padding.bottom
				if vcy < 0:
					vcy = 0
				view.size = FCSize(view.size.cx, vcy)
			elif view.dock == "bottom":
				view.location = FCPoint(margin.left + padding.left, view.parent.size.cy - view.size.cy - margin.bottom - padding.bottom)
				vcx = view.parent.size.cx - margin.left - padding.left - margin.right - padding.right
				if vcx < 0:
					vcx = 0
				view.size = FCSize(vcx, view.size.cy)
			if view.align == "center":
				view.location = FCPoint((view.parent.size.cx - view.size.cx) / 2, view.location.y)
			elif view.align == "right":
				view.location = FCPoint(view.parent.size.cx - view.size.cx - padding.right - margin.right, view.location.y)
			if view.verticalAlign == "middle":
				view.location = FCPoint(view.location.x, (view.parent.size.cy - view.size.cy) / 2)
			elif view.verticalAlign == "bottom":
				view.location = FCPoint(view.location.x, view.parent.size.cy - view.size.cy - padding.bottom - margin.bottom)
		elif view.parent == None:
			if view.dock == "fill":
				view.size = FCSize(view.paint.size.cx / view.paint.scaleFactorX, view.paint.size.cy / view.paint.scaleFactorY)
		if view.viewType == "split":
			resetSplitLayoutDiv(view)
		elif view.viewType == "tabview":
			updateTabLayout(view)
		elif view.viewType == "layout":
			resetLayoutDiv(view)
		elif view.viewType == "calendar":
			updateCalendar(view)
		elif view.viewType == "chart":
			chart = view
			resetChartVisibleRecord(chart)
			checkChartLastVisibleIndex(chart)
			if chart.onCalculateChartMaxMin != None:
				chart.onCalculateChartMaxMin(chart)
			elif chart.paint.onCalculateChartMaxMin != None:
				chart.paint.onCalculateChartMaxMin(chart)
			else:
				calculateChartMaxMin(chart)
		subViews = view.views
		if len(subViews) > 0:
			updateViewDefault(subViews)

#视图尺寸改变
def windowResize(rect, resizePoint, nowPoint, startTouchPoint):
	if resizePoint == 0:
		rect.left = rect.left + nowPoint.x - startTouchPoint.x
		rect.top = rect.top + nowPoint.y - startTouchPoint.y
	elif resizePoint == 1:
		rect.left = rect.left + nowPoint.x - startTouchPoint.x
		rect.bottom = rect.bottom + nowPoint.y - startTouchPoint.y
	elif resizePoint == 2:
		rect.right = rect.right + nowPoint.x - startTouchPoint.x
		rect.top = rect.top + nowPoint.y - startTouchPoint.y
	elif resizePoint == 3:
		rect.right = rect.right + nowPoint.x - startTouchPoint.x
		rect.bottom = rect.bottom + nowPoint.y - startTouchPoint.y
	elif resizePoint == 4:
		rect.left = rect.left + nowPoint.x - startTouchPoint.x
	elif resizePoint == 5:
		rect.top = rect.top + nowPoint.y - startTouchPoint.y
	elif resizePoint == 6:
		rect.right = rect.right + nowPoint.x - startTouchPoint.x
	elif resizePoint == 7:
		rect.bottom = rect.bottom + nowPoint.y - startTouchPoint.y

#获取调整尺寸的点
def getResizeState(view, mp):
	bWidth = 5
	width = view.size.cx
	height = view.size.cy
	if mp.x >= 0 and mp.x <= bWidth * 2 and mp.y >= 0 and mp.y <= bWidth * 2:
		return 0
	elif mp.x >= 0 and mp.x <= bWidth * 2 and mp.y >= height - bWidth * 2 and mp.y <= height:
		return 1
	elif mp.x >= width - bWidth * 2 and mp.x <= width and mp.y >= 0 and mp.y <= bWidth * 2:
		return 2
	elif mp.x >= width - bWidth * 2 and mp.x <= width and mp.y >= height - bWidth * 2 and mp.y <= height:
		return 3
	elif mp.x >= 0 and mp.x <= bWidth and mp.y >= 0 and mp.y <= height:
		return 4
	elif mp.x >= 0 and mp.x <= width and mp.y >= 0 and mp.y <= bWidth:
		return 5
	elif mp.x >= width - bWidth and mp.x <= width and mp.y >= 0 and mp.y <= height:
		return 6
	elif mp.x >= 0 and mp.x <= width and mp.y >= height - bWidth and mp.y <= height:
		return 7
	else:
		return -1

#鼠标移动方法
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
#paint 绘图对象
def handleMouseMove(mp, buttons, clicks, delta, paint):
	if paint.touchDownView != None:
		paint.touchMoveView = paint.touchDownView
		cmpPoint = FCPoint(mp.x - clientX(paint.touchDownView), mp.y - clientY(paint.touchDownView))
		if paint.onMouseMove != None:
			paint.onMouseMove(paint.touchDownView, cmpPoint, buttons, clicks, 0)
		else:
			onMouseMoveDefault(paint.touchDownView, cmpPoint, buttons, clicks, 0)
		if paint.isDoubleClick == False:
			if paint.focusedView != None and paint.focusedView.exView:
				paint.gdiPlusPaint.mouseMoveView(paint.focusedView.viewName, int(cmpPoint.x), int(cmpPoint.y), 1, 1)
				invalidateView(paint.focusedView)
		if paint.touchDownView.resizePoint != -1:
			newBounds = FCRect(paint.touchDownView.startRect.left, paint.touchDownView.startRect.top, paint.touchDownView.startRect.right, paint.touchDownView.startRect.bottom)
			windowResize(newBounds, paint.touchDownView.resizePoint, mp, paint.touchDownPoint)
			paint.touchDownView.location = FCPoint(newBounds.left, newBounds.top)
			paint.touchDownView.size = FCSize(newBounds.right - newBounds.left, newBounds.bottom - newBounds.top)
			if paint.touchDownView.parent != None:
				invalidateView(paint.touchDownView.parent)
			else:
				invalidate(paint)
		elif paint.touchDownView.allowDrag:
			if abs(mp.x - paint.touchDownPoint.x) > 5 or abs(mp.y - paint.touchDownPoint.y) > 5:
				paint.dragBeginRect = FCRect(paint.touchDownView.location.x, paint.touchDownView.location.y, paint.touchDownView.location.x + paint.touchDownView.size.cx, paint.touchDownView.location.y + paint.touchDownView.size.cy)
				paint.dragBeginPoint = FCPoint(paint.touchDownPoint.x, paint.touchDownPoint.y)
				paint.draggingView = paint.touchDownView
				paint.touchDownView = None
	elif paint.draggingView != None and buttons == 1:
		offsetX = mp.x - paint.dragBeginPoint.x
		offsetY = mp.y - paint.dragBeginPoint.y
		newBounds = FCRect(paint.dragBeginRect.left + offsetX, paint.dragBeginRect.top + offsetY, paint.dragBeginRect.right + offsetX, paint.dragBeginRect.bottom + offsetY)
		paint.draggingView.location = FCPoint(newBounds.left, newBounds.top)
		if paint.draggingView.parent != None and paint.draggingView.parent.viewType == "split":
			paint.draggingView.parent.splitPercent = -1
			resetSplitLayoutDiv(paint.draggingView.parent)
			if paint.onUpdateView != None:
				paint.onUpdateView(paint.draggingView.parent.views)
			else:
				updateViewDefault(paint.draggingView.parent.views)
		if paint.draggingView.parent != None:
			invalidateView(paint.draggingView.parent)
		else:
			invalidate(paint)
	else:
		topViews = paint.views
		view = findView(mp, topViews)
		cmpPoint = FCPoint(mp.x - clientX(view), mp.y - clientY(view))
		if view != None:
			oldMouseMoveView = paint.touchMoveView
			paint.touchMoveView = view
			if oldMouseMoveView != None and oldMouseMoveView != view:
				if oldMouseMoveView.onMouseLeave != None:
					oldMouseMoveView.onMouseLeave(oldMouseMoveView, cmpPoint, buttons, clicks, 0)
				elif paint.onMouseLeave != None:
					paint.onMouseLeave(oldMouseMoveView, cmpPoint, buttons, clicks, 0)
				invalidateView(oldMouseMoveView)
			if oldMouseMoveView == None or oldMouseMoveView != view:
				if view.onMouseEnter != None:
					view.onMouseEnter(view, cmpPoint, buttons, clicks, 0)
				elif paint.onMouseEnter != None:
					paint.onMouseEnter(view, cmpPoint, buttons, clicks, 0)
			paint.gdiPlusPaint.setCursor(view.cursor)
			if paint.onMouseMove != None:
				paint.onMouseMove(view, cmpPoint, buttons, clicks, 0)
			else:
				onMouseMoveDefault(view, cmpPoint, buttons, clicks, 0)

#鼠标按下方法
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
#paint 绘图对象
def handleMouseDown(mp, buttons, clicks, delta, paint):
	if clicks == 2:
		paint.isDoubleClick = True
	else:
		paint.isDoubleClick = False
	paint.cancelClick = False
	paint.touchDownPoint = mp
	autoHideView(paint.touchDownPoint, paint)
	topViews = paint.views
	paint.touchDownView = findView(mp, topViews)
	checkShowMenu(paint)
	if paint.touchDownView != None:
		if paint.focusedView != None and paint.focusedView != paint.touchDownView and paint.focusedView.exView:
			paint.gdiPlusPaint.unFocusView(paint.focusedView.viewName)
			invalidateView(paint.focusedView)
		paint.focusedView = paint.touchDownView
		cmpPoint = FCPoint(mp.x - clientX(paint.touchDownView), mp.y - clientY(paint.touchDownView))
		if paint.onMouseDown != None:
			paint.onMouseDown(paint.touchDownView, cmpPoint, buttons, clicks, 0)
		else:
			onMouseDownDefault(paint.touchDownView, cmpPoint, buttons, clicks, 0)
		if paint.focusedView != None and paint.focusedView.exView:
			paint.gdiPlusPaint.focusView(paint.focusedView.viewName)
			paint.gdiPlusPaint.mouseDownView(paint.focusedView.viewName, int(cmpPoint.x), int(cmpPoint.y), buttons, clicks)
			invalidateView(paint.focusedView)
		if paint.touchDownView.allowResize:
			paint.touchDownView.resizePoint = getResizeState(paint.touchDownView, cmpPoint)
			if paint.touchDownView.resizePoint != -1:
				paint.touchDownView.startRect = FCRect(paint.touchDownView.location.x, paint.touchDownView.location.y, paint.touchDownView.location.x + paint.touchDownView.size.cx, paint.touchDownView.location.y + paint.touchDownView.size.cy)

#鼠标抬起方法
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
#paint 绘图对象
def handleMouseUp(mp, buttons, clicks, delta, paint):
	paint.isDoubleClick = False
	if paint.touchDownView != None:
		cmpPoint = FCPoint(mp.x - clientX(paint.touchDownView), mp.y - clientY(paint.touchDownView))
		topViews = paint.views
		view = findView(mp, topViews)
		if view != None and view == paint.touchDownView:
			if paint.cancelClick == False:
				if paint.onClick != None:
					paint.onClick(paint.touchDownView, True, cmpPoint, False, cmpPoint, clicks)
				else:
					onClickDefault(paint.touchDownView, True, cmpPoint, False, cmpPoint, clicks)
		if paint.touchDownView != None:
			mouseDownView = paint.touchDownView
			paint.touchDownView.resizePoint = -1
			paint.touchDownView = None
			paint.touchMoveDiv = None
			if paint.onMouseUp != None:
				paint.onMouseUp(mouseDownView, cmpPoint, buttons, clicks, 0)
			else:
				onMouseUpDefault(mouseDownView, cmpPoint, buttons, clicks, 0)
			if paint.focusedView != None and paint.focusedView.exView:
				paint.gdiPlusPaint.focusView(paint.focusedView.viewName)
				paint.gdiPlusPaint.mouseUpView(paint.focusedView.viewName, int(cmpPoint.x), int(cmpPoint.y), buttons, clicks)
				invalidateView(paint.focusedView)
	paint.draggingView = None

#鼠标滚动方法
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
#paint 绘图对象
def handleMouseWheel(mp, buttons, clicks, delta, paint):
	topViews = paint.views
	view = findView(mp, topViews)
	if view != None:
		cmpPoint = FCPoint(mp.x - clientX(view), mp.y - clientY(view))
		if paint.onMouseWheel != None:
			paint.onMouseWheel(view, cmpPoint, buttons, clicks, delta)
		else:
			onMouseWheelDefault(view, cmpPoint, buttons, clicks, delta)
		if view.exView:
			paint.gdiPlusPaint.mouseWheelView(view.viewName, int(cmpPoint.x), int(cmpPoint.y), buttons, clicks, delta)
			invalidateView(view)

#获取饼图的最大值
#pie 饼图
def getPieMaxValue(pie):
	maxValue = 0
	for i in range(0, len(pie.items)):
		item = pie.items[i]
		maxValue += item.value
	return maxValue

#绘图饼图
#pie:饼图
#paint:绘图对象
#clipRect:裁剪区域
def drawPie(pie, paint, clipRect):
	width = pie.size.cx
	height = pie.size.cy
	oX = width / 2
	oY = height / 2
	eRect = FCRect(oX - pie.pieRadius, oY - pie.pieRadius, oX + pie.pieRadius, oY + pie.pieRadius)
	maxValue = getPieMaxValue(pie)
	if maxValue > 0:
		startAngle = pie.startAngle
		for i in range(0, len(pie.items)):
			item = pie.items[i]
			sweepAngle = item.value / maxValue * 360
			paint.fillPie(item.color, eRect.left, eRect.top, eRect.right, eRect.bottom, startAngle, sweepAngle)
			x1 = oX + (pie.pieRadius) * math.cos((startAngle + sweepAngle / 2) * 3.1415926 / 180)
			y1 = oY + (pie.pieRadius) * math.sin((startAngle + sweepAngle / 2) * 3.1415926 / 180)
			x2 = oX + (pie.textRadius) * math.cos((startAngle + sweepAngle / 2) * 3.1415926 / 180)
			y2 = oY + (pie.textRadius) * math.sin((startAngle + sweepAngle / 2) * 3.1415926 / 180)
			itemText = item.text + " " + str(item.value)
			itemTextSize = paint.textSize(itemText, pie.font)
			paint.drawLine(pie.textColor, 1, 0, x1, y1, x2, y2)
			x3 = oX + (pie.textRadius + itemTextSize.cx / 2 + 5) * math.cos((startAngle + sweepAngle / 2) * 3.1415926 / 180)
			y3 = oY + (pie.textRadius + itemTextSize.cy / 2 + 5) * math.sin((startAngle + sweepAngle / 2) * 3.1415926 / 180)
			paint.drawText(itemText, pie.textColor, pie.font, x3 - itemTextSize.cx / 2, y3 - itemTextSize.cy / 2)
			startAngle += sweepAngle
	paint.drawEllipse(pie.borderColor, 1, 0, eRect.left, eRect.top, eRect.right, eRect.bottom)

#获取视图文本
#view 视图
#atrName 属性名称
def getViewAttribute(view, atrName):
	viewText = ""
	recvData = create_string_buffer(102400)
	view.paint.gdiPlusPaint.getAttribute(view.viewName, atrName, recvData)
	viewText = str(recvData.value, encoding="gbk")
	return viewText

#设置视图文本
#view 视图
#atrName 属性名称
#text 文本
def setViewAttribute(view, atrName, text):
	view.paint.gdiPlusPaint.setAttribute(view.viewName, atrName, text)

#获取月的日数
#year:年
#month:月
def getDaysInMonth(year, month):
	if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
		return 31
	elif month == 4 or month == 6 or month == 9 or month == 11:
		return 30
	else:
		if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
				return 29
		else:
			return 28

#根据字符获取月份
#month:月
def getMonthStr(month):
	if month == 1:
		return "一月"
	elif month == 2:
		return "二月"
	elif month == 3:
		return "三月"
	elif month == 4:
		return "四月"
	elif month == 5:
		return "五月"
	elif month == 6:
		return "六月"
	elif month == 7:
		return "七月"
	elif month == 8:
		return "八月"
	elif month == 9:
		return "九月"
	elif month == 10:
		return "十月"
	elif month == 11:
		return "十一月"
	elif month == 12:
		return "十二月"
	else:
		return ""

#获取年
#years:年的集合
#year:年
def getYear(years, year):
	cy = None
	if (year in years) == False:
		cy = CYear()
		cy.year = year
		years[year] = cy
		for i in range(1,13):
			cMonth = CMonth()
			cMonth.year = year
			cMonth.month = i
			cy.months[i] = cMonth
			daysInMonth = getDaysInMonth(year, i)
			for j in range(1,daysInMonth + 1):
				cDay = CDay()
				cDay.year = year
				cDay.month = i
				cDay.day = j
				cMonth.days[j] = cDay
	else:
		cy = years[year]
	return cy

#显示隐藏日期层
#dayDiv:日期层
#visible:是否可见
def showOrHideDayDiv(dayDiv, visible):
	dayButtonSize = len(dayDiv.dayButtons)
	for i in range(0, dayButtonSize):
		dayButton = dayDiv.dayButtons[i]
		dayButton.visible = visible

#显示隐藏月层
#monthDiv:月层
#visible:是否可见
def showOrHideMonthDiv(monthDiv, visible):
	monthButtonSize = len(monthDiv.monthButtons)
	for i in range(0, monthButtonSize):
		monthButton = monthDiv.monthButtons[i]
		monthButton.visible = visible

#显示隐藏年层
#yearButtons:年层
#visible:是否可见
def showOrHideYearDiv(yearDiv, visible):
	yearButtonSize = len(yearDiv.yearButtons)
	for i in range(0,yearButtonSize):
		yearButton = yearDiv.yearButtons[i]
		yearButton.visible = visible

#初始化日历
#calendar:日历
def initCalendar(calendar):
	calendar.dayDiv.calendar = calendar
	calendar.monthDiv.calendar = calendar
	calendar.yearDiv.calendar = calendar
	for i in range(0,42):
		dayButton = DayButton()
		dayButton.calendar = calendar
		calendar.dayDiv.dayButtons.append(dayButton)
		dayFCButtonm = DayButton()
		dayFCButtonm.calendar = calendar
		dayFCButtonm.visible = False
		calendar.dayDiv.dayButtons_am.append(dayFCButtonm)
	for i in range(0,12):
		monthButton = MonthButton()
		monthButton.calendar = calendar
		monthButton.month = (i + 1)
		calendar.monthDiv.monthButtons.append(monthButton)
		monthButtonAm = MonthButton()
		monthButtonAm.calendar = calendar
		monthButtonAm.visible = False
		monthButtonAm.month = (i + 1)
		calendar.monthDiv.monthButtons_am.append(monthButtonAm)

	for i in range(0,12):
		yearButton = YearButton()
		yearButton.calendar = calendar
		calendar.yearDiv.yearButtons.append(yearButton)
		yearButtonAm = YearButton()
		yearButtonAm.calendar = calendar
		yearButtonAm.visible = False
		calendar.yearDiv.yearButtons_am.append(yearButtonAm)
	calendar.headDiv.calendar = calendar
	calendar.timeDiv.calendar = calendar

#获取星期
#y:年
#m:月
#d:日
def dayOfWeek(y, m, d):
	if m == 1 or m == 2:
		m += 12
		y = y - 1
	return int(((d + 2 * m + 3 * (m + 1) / 5 + y + y / 4 - y / 100 + y / 400) + 1) % 7)

#获取当月
#calendar:日历
def getMonth(calendar):
	return getYear(calendar.years, calendar.selectedDay.year).months.get(calendar.selectedDay.month)

#获取下个月
#calendar:日历
#year:年
#month:月
def getNextMonth(calendar, year, month):
	nextMonth = month + 1
	nextYear = year
	if nextMonth == 13:
		nextMonth = 1
		nextYear += 1
	return getYear(calendar.years, nextYear).months.get(nextMonth)

#获取上个月
#calendar:日历
#year:年
#month:月
def getLastMonth(calendar, year, month):
	lastMonth = month - 1
	lastYear = year
	if lastMonth == 0:
		lastMonth = 12
		lastYear -= 1
	return getYear(calendar.years, lastYear).months.get(lastMonth)

#重置日期层布局
#dayDiv:日期层
#state:状态
def resetDayDiv(dayDiv, state):
	calendar = dayDiv.calendar
	thisMonth = getMonth(calendar)
	lastMonth = getLastMonth(calendar, thisMonth.year, thisMonth.month)
	nextMonth = getNextMonth(calendar, thisMonth.year, thisMonth.month)
	left = 0
	headHeight = calendar.headDiv.bounds.bottom
	top = headHeight
	width = calendar.size.cx
	height = calendar.size.cy
	height -= calendar.timeDiv.bounds.bottom - calendar.timeDiv.bounds.top
	dayButtonHeight = height - headHeight
	if dayButtonHeight < 1:
		dayButtonHeight = 1
	toY = 0
	if dayDiv.aDirection == 1:
		toY = dayButtonHeight * dayDiv.aTick / dayDiv.aTotalTick
		if state == 1:
			thisMonth = nextMonth
			month = thisMonth.month
			lastMonth = getLastMonth(calendar, thisMonth.year, month)
			nextMonth = getNextMonth(calendar, thisMonth.year, month)
	elif dayDiv.aDirection == 2:
		toY = -dayButtonHeight * dayDiv.aTick / dayDiv.aTotalTick
		if state == 1:
			thisMonth = lastMonth
			month = thisMonth.month
			lastMonth = getLastMonth(calendar, thisMonth.year, month)
			nextMonth = getNextMonth(calendar, thisMonth.year, month)
	buttonSize = 0
	if state == 0:
		buttonSize = len(dayDiv.dayButtons)
	elif state == 1:
		buttonSize = len(dayDiv.dayButtons_am)
	dheight = dayButtonHeight / 6
	days = thisMonth.days
	firstDay = days.get(1)
	startDayOfWeek = dayOfWeek(firstDay.year, firstDay.month, firstDay.day)
	for i in range(0, buttonSize):
		dayButton = None
		if state == 0:
			dayButton = dayDiv.dayButtons[i]
			buttonSize = len(dayDiv.dayButtons)
		elif state == 1:
			dayButton = dayDiv.dayButtons_am[i]
			buttonSize = len(dayDiv.dayButtons_am)
		if i == 35:
			dheight = height - top
		vOffset = 0
		if state == 1:
			if dayDiv.aTick > 0:
				dayButton.visible = True
				if dayDiv.aDirection == 1:
					vOffset = toY - dayButtonHeight
				elif dayDiv.aDirection == 2:
					vOffset = toY + dayButtonHeight
			else:
				dayButton.visible = False
				continue
		else:
			vOffset = toY
		if (i + 1) % 7 == 0:
			dp = FCPoint(left, top + vOffset)
			ds = FCSize(width - left, dheight)
			bounds = FCRect(dp.x, dp.y, dp.x + ds.cx, dp.y + ds.cy)
			dayButton.bounds = bounds
			left = 0
			if i != 0 and i != buttonSize - 1:
				top += dheight
		else:
			dp = FCPoint(left, top + vOffset)
			ds = FCSize(width / 7 + ((i + 1) % 7) % 2, dheight)
			bounds = FCRect(dp.x, dp.y, dp.x + ds.cx, dp.y + ds.cy)
			dayButton.bounds = bounds
			left += ds.cx
		cDay = None
		dayButton.inThisMonth = False
		if i >= startDayOfWeek and i <= startDayOfWeek + len(days) - 1:
			cDay = days.get(i - startDayOfWeek + 1)
			dayButton.inThisMonth = True
		elif i < startDayOfWeek:
			cDay = lastMonth.days.get(len(lastMonth.days) - startDayOfWeek + i + 1)
		elif i > startDayOfWeek + len(days) - 1:
			cDay = nextMonth.days.get(i - startDayOfWeek - len(days) + 1)
		dayButton.day = cDay
		if state == 0 and dayButton.day and dayButton.day == calendar.selectedDay:
			dayButton.selected = True
		else:
			dayButton.selected = False

#重置月层布局
#monthDiv:月层
#state:状态
def resetMonthDiv(monthDiv, state):
	calendar = monthDiv.calendar
	thisYear = monthDiv.year
	lastYear = monthDiv.year - 1
	nextYear = monthDiv.year + 1
	left = 0
	headHeight = calendar.headDiv.bounds.bottom
	top = headHeight
	width = calendar.size.cx
	height = calendar.size.cy
	height -= calendar.timeDiv.bounds.bottom - calendar.timeDiv.bounds.top
	monthButtonHeight = height - top
	if monthButtonHeight < 1:
		monthButtonHeight = 1
	toY = 0
	monthButtons = None
	if monthDiv.aDirection == 1:
		toY = monthButtonHeight * monthDiv.aTick / monthDiv.aTotalTick
		if state == 1:
			thisYear = nextYear
			lastYear = thisYear - 1
			nextYear = thisYear + 1
	elif monthDiv.aDirection == 2:
		toY = -monthButtonHeight * monthDiv.aTick / monthDiv.aTotalTick
		if state == 1:
			thisYear = lastYear
			lastYear = thisYear - 1
			nextYear = thisYear + 1
	if state == 0:
		monthButtons = monthDiv.monthButtons
	elif state == 1:
		monthButtons = monthDiv.monthButtons_am
	dheight = monthButtonHeight / 3
	buttonSize = len(monthButtons)
	for i in range(0, buttonSize):
		if i == 8:
			dheight = height - top
		monthButton = monthButtons[i]
		monthButton.year = thisYear
		vOffSet = 0
		if state == 1:
			if monthDiv.aTick > 0:
				monthButton.visible = True
				if monthDiv.aDirection == 1:
					vOffSet = toY - monthButtonHeight
				elif monthDiv.aDirection == 2:
					vOffSet = toY + monthButtonHeight
			else:
				monthButton.visible = False
				continue
		else:
			vOffSet = toY
		if (i + 1) % 4 == 0:
			dp = FCPoint(left, top + vOffSet)
			ds = FCSize(width - left, dheight)
			bounds = FCRect(dp.x, dp.y, dp.x + ds.cx, dp.y + ds.cy)
			monthButton.bounds = bounds
			left = 0
			if i != 0 and i != buttonSize - 1:
				top += dheight
		else:
			dp = FCPoint(left, top + vOffSet)
			ds = FCSize( width / 4 + ((i + 1) % 4) % 2, dheight)
			bounds = FCRect(dp.x, dp.y, dp.x + ds.cx, dp.y + ds.cy)
			monthButton.bounds = bounds
			left += ds.cx

#重置年层布局
#yearDiv:年层
#state:状态
def resetYearDiv(yearDiv, state):
	calendar = yearDiv.calendar
	thisStartYear = yearDiv.startYear
	lastStartYear = yearDiv.startYear - 12
	nextStartYear = yearDiv.startYear + 12
	left = 0
	headHeight = calendar.headDiv.bounds.bottom
	top = headHeight
	width = calendar.size.cx
	height = calendar.size.cy
	height -= calendar.timeDiv.bounds.bottom - calendar.timeDiv.bounds.top
	yearButtonHeight = height - top
	if yearButtonHeight < 1:
		yearButtonHeight = 1
	toY = 0
	yearButtons = None
	if yearDiv.aDirection == 1:
		toY = yearButtonHeight * yearDiv.aTick / yearDiv.aTotalTick
		if state == 1:
			thisStartYear = nextStartYear
			lastStartYear = thisStartYear - 12
			nextStartYear = thisStartYear + 12
	elif yearDiv.aDirection == 2:
		toY = -yearButtonHeight * yearDiv.aTick / yearDiv.aTotalTick
		if state == 1:
			thisStartYear = lastStartYear
			lastStartYear = thisStartYear - 12
			nextStartYear = thisStartYear + 12
	if state == 0:
		yearButtons = yearDiv.yearButtons
	elif state == 1:
		yearButtons = yearDiv.yearButtons_am
	dheight = yearButtonHeight / 3
	buttonSize = len(yearDiv.yearButtons)
	for i in range(0, buttonSize):
		if i == 8:
			dheight = height - top
		yearButton = yearButtons[i]
		yearButton.year = thisStartYear + i
		vOffSet = 0
		if state == 1:
			if yearDiv.aTick > 0:
				yearButton.visible = True
				if yearDiv.aDirection == 1:
					vOffSet = toY - yearButtonHeight
				elif yearDiv.aDirection == 2:
					vOffSet = toY + yearButtonHeight
			else:
				yearButton.visible = False
				continue
		else:
			vOffSet = toY
		if (i + 1) % 4 == 0:
			dp = FCPoint(left, top + vOffSet)
			ds = FCSize(width - left, dheight)
			bounds = FCRect(dp.x, dp.y, dp.x + ds.cx, dp.y + ds.cy)
			yearButton.bounds = bounds
			left = 0
			if i != 0 and i != buttonSize - 1:
				top += dheight
		else:
			dp = FCPoint(left, top + vOffSet)
			ds = FCSize(width / 4 + ((i + 1) % 4) % 2, dheight)
			bounds = FCRect(dp.x, dp.y, dp.x + ds.cx, dp.y + ds.cy)
			yearButton.bounds = bounds
			left += ds.cx

#选择开始年份
#yearDiv:年层
#startYear:开始年
def selectStartYear(yearDiv, startYear):
	if yearDiv.startYear != startYear:
		if startYear > yearDiv.startYear:
			yearDiv.aDirection = 1
		else:
			yearDiv.aDirection = 2
		if yearDiv.calendar.useAnimation:
			yearDiv.aTick = yearDiv.aTotalTick
		yearDiv.startYear = startYear

#选择年份
#monthDiv:月层
#year:年
def selectYear(monthDiv, year):
	if monthDiv.year != year:
		if year > monthDiv.year:
			monthDiv.aDirection = 1
		else:
			monthDiv.aDirection = 2
		if monthDiv.calendar.useAnimation:
			monthDiv.aTick = monthDiv.aTotalTick
		monthDiv.year = year

#选中日期
#dayDiv:日期层
#selectedDay:选中日
#lastDay:上一日
def selectDay(dayDiv, selectedDay, lastDay):
	calendar = dayDiv.calendar
	m = getYear(calendar.years, selectedDay.year).months.get(selectedDay.month)
	thisMonth = getYear(calendar.years, lastDay.year).months.get(lastDay.month)
	if m != thisMonth:
		if thisMonth.year * 12 + thisMonth.month > m.year * 12 + m.month:
			dayDiv.aDirection = 2
		else:
			dayDiv.aDirection = 1
		i = 0
		buttonSize = len(dayDiv.dayButtons)
		for i in range(0, buttonSize):
			dayButton = dayDiv.dayButtons[i]
			if (dayDiv.aDirection == 1 and dayButton.day == thisMonth.days.get(0)) or (dayDiv.aDirection == 2 and dayButton.day == thisMonth.days.get(len(thisMonth.days) - 1)):
				dayDiv.aClickRowFrom = i / 7
				if i % 7 != 0:
					dayDiv.aClickRowFrom += 1
		resetDayDiv(dayDiv, 0)
		buttonSize = len(dayDiv.dayButtons_am)
		for i in range(0, buttonSize):
			dayFCButtonm = dayDiv.dayButtons_am[i]
			if (dayDiv.aDirection == 1 and dayFCButtonm.day == m.days.get(0)) or (dayDiv.aDirection == 2 and dayFCButtonm.day == m.days.get(len(m.days) - 1)):
				dayDiv.aClickRowTo = i / 7
				if i % 7 != 0:
					dayDiv.aClickRowTo += 1
		if calendar.useAnimation:
			dayDiv.aTick = dayDiv.aTotalTick
	else:
		dayButtonsSize = len(dayDiv.dayButtons)
		for i in range(0, dayButtonsSize):
			dayButton = dayDiv.dayButtons[i]
			if dayButton.day != selectedDay:
				dayButton.selected = False

#日历的秒表
#calendar:日历
def calendarTimer(calendar):
	paint = False
	if calendar.dayDiv.aTick > 0:
		calendar.dayDiv.aTick = int(calendar.dayDiv.aTick * 2 / 3)
		paint = True
	if calendar.monthDiv.aTick > 0:
		calendar.monthDiv.aTick = int(calendar.monthDiv.aTick * 2 / 3)
		paint = True
	if calendar.yearDiv.aTick > 0:
		calendar.yearDiv.aTick = int(calendar.yearDiv.aTick * 2 / 3)
		paint = True
	if paint:
		updateCalendar(calendar)
		if calendar.paint:
			invalidateView(calendar)

#更新日历的布局
#calendar:日历
def updateCalendar(calendar):
	calendar.headDiv.bounds = FCRect(0, 0, calendar.size.cx, 80)
	if calendar.mode == "day":
		resetDayDiv(calendar.dayDiv, 0)
		resetDayDiv(calendar.dayDiv, 1)
	elif calendar.mode == "month":
		resetMonthDiv(calendar.monthDiv, 0)
		resetMonthDiv(calendar.monthDiv, 1)
	elif calendar.mode == "year":
		resetYearDiv(calendar.yearDiv, 0)
		resetYearDiv(calendar.yearDiv, 1)

#绘制头部层
#headDiv:头部层
#paint:绘图对象
def drawHeadDiv(headDiv, paint):
	calendar = headDiv.calendar
	bounds = headDiv.bounds
	if headDiv.backColor != "none":
		paint.fillRect(headDiv.backColor, bounds.left, bounds.top, bounds.right, bounds.bottom)
	weekStrings = []
	weekStrings.append("周日")
	weekStrings.append("周一")
	weekStrings.append("周二")
	weekStrings.append("周三")
	weekStrings.append("周四")
	weekStrings.append("周五")
	weekStrings.append("周六")
	w = bounds.right - bounds.left
	left = bounds.left
	for i in range(0, 7):
		weekDaySize = paint.textSize(weekStrings[i], headDiv.weekFont)
		textX = left + (w / 7) / 2 - weekDaySize.cx / 2
		textY = bounds.bottom - weekDaySize.cy - 2
		paint.drawText(weekStrings[i], headDiv.textColor, headDiv.weekFont, textX, textY)
		left += w / 7
	drawTitle = ""
	if calendar.mode == "day":
		drawTitle = str(calendar.selectedDay.year) + "年" + str(calendar.selectedDay.month) + "月"
	elif calendar.mode == "month":
		drawTitle = str(calendar.monthDiv.year) + "年"
	else:
		drawTitle = str(calendar.yearDiv.startYear) + "年-" + str(calendar.yearDiv.startYear + 11) + "年"
	tSize = paint.textSize(drawTitle, headDiv.titleFont)
	paint.drawText(drawTitle, headDiv.textColor, headDiv.titleFont, bounds.left + (w - tSize.cx) / 2, 30)
	tR = 10
	#画左右三角
	drawPoints = []
	drawPoints.append(FCPoint(5, bounds.top + (bounds.bottom - bounds.top) / 2))
	drawPoints.append(FCPoint(5 + tR * 2, bounds.top + (bounds.bottom - bounds.top) / 2 - tR))
	drawPoints.append(FCPoint(5 + tR * 2, bounds.top + (bounds.bottom - bounds.top) / 2 + tR))
	paint.fillPolygon(headDiv.arrowColor, drawPoints)
	drawPoints = []
	drawPoints.append(FCPoint(bounds.right - 5, bounds.top + (bounds.bottom - bounds.top) / 2))
	drawPoints.append(FCPoint(bounds.right - 5 - tR * 2, bounds.top + (bounds.bottom - bounds.top) / 2 - tR))
	drawPoints.append(FCPoint(bounds.right - 5 - tR * 2, bounds.top + (bounds.bottom - bounds.top) / 2 + tR))
	paint.fillPolygon(headDiv.arrowColor, drawPoints)

#绘制日的按钮
#dayButton:日期按钮
#paint:绘图对象
def drawDayButton(dayButton, paint):
	if dayButton.day != None:
		calendar = dayButton.calendar
		bounds = dayButton.bounds
		text = str(dayButton.day.day)
		tSize = paint.textSize(text, dayButton.font)
		if dayButton.backColor != "none":
			paint.fillRect(dayButton.backColor, bounds.left + 2, bounds.top + 2, bounds.right - 2, bounds.bottom - 2)
		if dayButton.inThisMonth:
			paint.drawText(text, dayButton.textColor, dayButton.font, bounds.left + 5, bounds.top + 7)
		else:
			paint.drawText(text, dayButton.textColor2, dayButton.font, bounds.left + 5, bounds.top + 7)
		if dayButton.borderColor != "none":
			paint.drawRect(dayButton.borderColor, 1, 0, bounds.left + 2, bounds.top + 2, bounds.right - 2, bounds.bottom - 2)

#绘制月的按钮
#monthButton:月按钮
#paint:绘图对象
def drawMonthButton(monthButton, paint):
    calendar = monthButton.calendar
    bounds = monthButton.bounds
    text = getMonthStr(monthButton.month)
    tSize = paint.textSize(text, monthButton.font)
    if monthButton.backColor != "none":
        paint.fillRect(monthButton.backColor, bounds.left + 2, bounds.top + 2, bounds.right - 2, bounds.bottom - 2)
    paint.drawText(text, monthButton.textColor, monthButton.font, bounds.left + 5, bounds.top + 7)
    if monthButton.borderColor != "none":
        paint.drawRect(monthButton.borderColor, 1, 0, bounds.left + 2, bounds.top + 2, bounds.right - 2, bounds.bottom - 2)

#绘制年的按钮
#yearButton:年按钮
#paint:绘图对象
def drawYearButton(yearButton, paint):
    calendar = yearButton.calendar
    bounds = yearButton.bounds
    text = str(yearButton.year)
    tSize = paint.textSize(text, yearButton.font)
    if yearButton.backColor != "none":
        paint.fillRect(yearButton.backColor, bounds.left + 2, bounds.top + 2, bounds.right - 2, bounds.bottom - 2)
    paint.drawText(text, yearButton.textColor, yearButton.font, bounds.left + 5, bounds.top + 7)
    if yearButton.borderColor != "none":
        paint.drawRect(yearButton.borderColor, 1, 0, bounds.left + 2, bounds.top + 2, bounds.right - 2, bounds.bottom - 2)

#绘制日历
#calendar:日历
#paint:绘图对象
def drawCalendar(calendar, paint):
	if calendar.backColor != "none":
		paint.fillRect(calendar.backColor, 0, 0, calendar.size.cx, calendar.size.cy)
	if calendar.mode == "day":
		dayButtonsSize = len(calendar.dayDiv.dayButtons)
		for i in range(0,dayButtonsSize):
			dayButton = calendar.dayDiv.dayButtons[i]
			if dayButton.visible:
				if calendar.onPaintCalendarDayButton != None:
					calendar.onPaintCalendarDayButton(dayButton, paint)
				elif paint.onPaintCalendarDayButton != None:
					paint.onPaintCalendarDayButton(dayButton, paint)
				else:
					drawDayButton(dayButton, paint)
		dayFCButtonmSize = len(calendar.dayDiv.dayButtons_am)
		for i in range(0,dayFCButtonmSize):
			dayButton = calendar.dayDiv.dayButtons_am[i]
			if dayButton.visible:
				if calendar.onPaintCalendarDayButton != None:
					calendar.onPaintCalendarDayButton(dayButton, paint)
				elif paint.onPaintCalendarDayButton != None:
					paint.onPaintCalendarDayButton(dayButton, paint)
				else:
					drawDayButton(dayButton, paint)
	elif calendar.mode == "month":
		monthButtonsSize = len(calendar.monthDiv.monthButtons)
		for i in range(0,monthButtonsSize):
			monthButton = calendar.monthDiv.monthButtons[i]
			if monthButton.visible:
				if calendar.onPaintCalendarMonthButton != None:
					calendar.onPaintCalendarMonthButton(monthButton, paint)
				elif paint.onPaintCalendarMonthButton != None:
					paint.onPaintCalendarMonthButton(monthButton, paint)
				else:
					drawMonthButton(monthButton, paint)
		monthFCButtonmSize = len(calendar.monthDiv.monthButtons_am)
		for i in range(0,monthFCButtonmSize):
			monthButton = calendar.monthDiv.monthButtons_am[i]
			if monthButton.visible:
				if calendar.onPaintCalendarMonthButton != None:
					calendar.onPaintCalendarMonthButton(monthButton, paint)
				elif paint.onPaintCalendarMonthButton != None:
					paint.onPaintCalendarMonthButton(monthButton, paint)
				else:
					drawMonthButton(monthButton, paint)
	elif calendar.mode == "year":
		yearButtonsSize = len(calendar.yearDiv.yearButtons)
		for i in range(0,yearButtonsSize):
			yearButton = calendar.yearDiv.yearButtons[i]
			if yearButton.visible:
				if calendar.onPaintCalendarYearButton != None:
					calendar.onPaintCalendarYearButton(yearButton, paint)
				elif paint.onPaintCalendarYearButton != None:
					paint.onPaintCalendarYearButton(yearButton, paint)
				else:
					drawYearButton(yearButton, paint)
		yearFCButtonmSize = len(calendar.yearDiv.yearButtons_am)
		for i in range(0,yearFCButtonmSize):
			yearButton = calendar.yearDiv.yearButtons_am[i]
			if yearButton.visible:
				if calendar.onPaintCalendarYearButton != None:
					calendar.onPaintCalendarYearButton(yearButton, paint)
				elif paint.onPaintCalendarYearButton != None:
					paint.onPaintCalendarYearButton(yearButton, paint)
				else:
					drawYearButton(yearButton, paint)
	if calendar.onPaintCalendarHeadDiv != None:
		calendar.onPaintCalendarHeadDiv(calendar.headDiv, paint)
	elif paint.onPaintCalendarHeadDiv != None:
		paint.onPaintCalendarHeadDiv(calendar.headDiv, paint)
	else:
		drawHeadDiv(calendar.headDiv, paint)
	if calendar.borderColor != "none":
		paint.drawRect(calendar.borderColor, 1, 0, 0, 0, calendar.size.cx, calendar.size.cy)

#点击日的按钮
#dayButton:日期按钮
#mp:坐标
def clickDayButton(dayButton, mp):
	calendar = dayButton.calendar
	lastDay = calendar.selectedDay
	calendar.selectedDay = dayButton.day
	selectDay(calendar.dayDiv, calendar.selectedDay, lastDay)
	updateCalendar(calendar)
	if calendar.paint != None:
	    invalidateView(calendar)

#点击月的按钮
#monthButton:月按钮
#mp:坐标
def clickMonthButton(monthButton, mp):
	calendar = monthButton.calendar
	month = getYear(calendar.years, monthButton.year).months[monthButton.month]
	calendar.mode = "day"
	lastDay = calendar.selectedDay
	calendar.selectedDay = month.days.get(1)
	selectDay(calendar.dayDiv, calendar.selectedDay, lastDay)
	updateCalendar(calendar)
	if calendar.paint != None:
	    invalidateView(calendar)

#点击年的按钮
#mp:坐标
#yearButton:年按钮
def clickYearButton(yearButton, mp):
	calendar = yearButton.calendar
	calendar.mode = "month"
	selectYear(calendar.monthDiv, yearButton.year)
	updateCalendar(calendar)
	if calendar.paint != None:
	    invalidateView(calendar)

#点击左侧的按钮
#headDiv:头部层
#mp:坐标
def clickLastButton(headDiv, mp):
	calendar = headDiv.calendar
	if calendar.mode == "day":
		lastMonth = getLastMonth(calendar, calendar.selectedDay.year, calendar.selectedDay.month)
		lastDay = calendar.selectedDay
		calendar.selectedDay = lastMonth.days.get(1)
		selectDay(calendar.dayDiv, calendar.selectedDay, lastDay)
		updateCalendar(calendar)
		if calendar.paint != None:
			invalidateView(calendar)
	elif calendar.mode == "month":
		year = calendar.monthDiv.year
		year -= 1
		selectYear(calendar.monthDiv, year)
		updateCalendar(calendar)
		if calendar.paint != None:
			invalidateView(calendar)
	elif calendar.mode == "year":
		year = calendar.yearDiv.startYear
		year -= 12
		selectStartYear(calendar.yearDiv, year)
		updateCalendar(calendar)
		if calendar.paint != None:
		    invalidateView(calendar)

#点击右侧的按钮
#headDiv:头部层
#mp:坐标
def clickNextButton(headDiv, mp):
	calendar = headDiv.calendar
	if calendar.mode == "day":
		nextMonth = getNextMonth(calendar, calendar.selectedDay.year, calendar.selectedDay.month)
		lastDay = calendar.selectedDay
		calendar.selectedDay = nextMonth.days.get(1)
		selectDay(calendar.dayDiv, calendar.selectedDay, lastDay)
		updateCalendar(calendar)
		if calendar.paint != None:
			invalidateView(calendar)
	elif calendar.mode == "month":
		year = calendar.monthDiv.year
		year += 1
		selectYear(calendar.monthDiv, year)
		updateCalendar(calendar)
		if calendar.paint != None:
			invalidateView(calendar)
	elif calendar.mode == "year":
		year = calendar.yearDiv.startYear
		year += 12
		selectStartYear(calendar.yearDiv, year)
		updateCalendar(calendar)
		if calendar.paint != None:
		    invalidateView(calendar)

#改变模式的按钮
#headDiv:头部层
#mp:坐标
def clickModeButton(headDiv, mp):
	calendar = headDiv.calendar
	if calendar.mode == "day":
		calendar.mode = "month"
		calendar.monthDiv.month = calendar.selectedDay.month
		calendar.monthDiv.year = calendar.selectedDay.year
		updateCalendar(calendar)
		if calendar.paint != None:
			invalidateView(calendar)
	elif calendar.mode == "month":
		calendar.mode = "year"
		selectStartYear(calendar.yearDiv, calendar.monthDiv.year)
		updateCalendar(calendar)
		if calendar.paint != None:
		    invalidateView(calendar)

#点击日历
#calendar:日历
#mp:坐标
def clickCalendar(calendar, mp):
	headBounds = calendar.headDiv.bounds
	if mp.x >= headBounds.left and mp.x <= headBounds.right and mp.y >= headBounds.top and mp.y <= headBounds.bottom:
		tR = 10
		if mp.x < headBounds.left + tR * 3:
			clickLastButton(calendar.headDiv, mp)
			return
		elif mp.x > headBounds.right - tR * 3:
			clickNextButton(calendar.headDiv, mp)
			return
		else:
			clickModeButton(calendar.headDiv, mp)
			return
	if calendar.mode == "day":
		dayButtonsSize = len(calendar.dayDiv.dayButtons)
		for i in range(0,dayButtonsSize):
			dayButton = calendar.dayDiv.dayButtons[i]
			if dayButton.visible:
				bounds = dayButton.bounds
				if mp.x >= bounds.left and mp.x <= bounds.right and mp.y >= bounds.top and mp.y <= bounds.bottom:
					clickDayButton(dayButton, mp)
					return
	elif calendar.mode == "month":
		monthButtonsSize = len(calendar.monthDiv.monthButtons)
		for i in range(0,monthButtonsSize):
			monthButton = calendar.monthDiv.monthButtons[i]
			if monthButton.visible:
				bounds = monthButton.bounds
				if mp.x >= bounds.left and mp.x <= bounds.right and mp.y >= bounds.top and mp.y <= bounds.bottom:
					clickMonthButton(monthButton, mp)
					return
	elif calendar.mode == "year":
		yearButtonsSize = len(calendar.yearDiv.yearButtons)
		for i in range(0,yearButtonsSize):
			yearButton = calendar.yearDiv.yearButtons[i]
			if yearButton.visible:
				bounds = yearButton.bounds
				if mp.x >= bounds.left and mp.x <= bounds.right and mp.y >= bounds.top and mp.y <= bounds.bottom:
					clickYearButton(yearButton, mp)
					return

#自动适应位置和大小
#menu:菜单
def adjustMenu(menu):
	resetLayoutDiv(menu)
	if menu.autoSize:
		contentHeight = getDivContentHeight(menu)
		maximumHeight = menu.maximumSize.cy
		menu.size.cy = min(contentHeight, maximumHeight)
	mPoint = menu.location
	mSize = menu.size
	paint = menu.paint
	nSize = FCSize(paint.size.cx / paint.scaleFactorX, paint.size.cy / paint.scaleFactorY)
	if mPoint.x < 0:
		mPoint.x = 0
	if mPoint.y < 0:
		mPoint.y = 0
	if mPoint.x + mSize.cx > nSize.cx:
		mPoint.x = nSize.cx - mSize.cx
	if mPoint.y + mSize.cy > nSize.cy:
		mPoint.y = nSize.cy - mSize.cy
	menu.location = mPoint
	menu.scrollV = 0

#添加菜单项
#item:菜单项
#menu:菜单
def addMenuItem(item, menu):
	addViewToParent(item, menu)
	item.parentMenu = menu
	menu.items.append(item)

#添加菜单项
#item:菜单项
#parentItem:父菜单项
def addMenuItemToParent(item, parentItem):
	item.parentItem = parentItem
	if parentItem.dropDownMenu == None:
		parentItem.dropDownMenu = FCMenu()
		addView(parentItem.dropDownMenu, parentItem.paint)
	item.parentMenu = parentItem.dropDownMenu
	addViewToParent(item, parentItem.dropDownMenu)
	parentItem.items.append(item)
	parentItem.dropDownMenu.items.append(item)

#控制菜单的显示隐藏
#paint:绘图对象
def checkShowMenu(paint):
	paintAll = False
	clickItem = False
	for i in range(0, len(paint.views)):
		view = paint.views[i]
		if view.viewType == "menu":
			if view.visible:
				if view == paint.touchDownView:
					clickItem = True
				for j in range(0, len(view.items)):
					item = view.items[j]
					if item == paint.touchDownView:
						clickItem = True
						break
	if clickItem == False:
		for i in range(0, len(paint.views)):
			view = paint.views[i]
			if view.viewType == "menu":
				view.visible = False
				paintAll = True
	if paintAll:
		invalidate(paint)

#关闭网格视图
#items:菜单集合
def closeMenus(items):
	itemSize = len(items)
	close = False
	for i in range(0, itemSize):
		item = items[i]
		subItems = item.items
		if closeMenus(subItems):
			close = True
		dropDownMenu = item.dropDownMenu
		if dropDownMenu != None and dropDownMenu.visible:
			dropDownMenu.visible = False
			close = True
	return close

#鼠标移动到菜单项
#item 菜单项
def touchMoveMenuItem(item):
	parentItem = item.parentItem
	items = []
	if parentItem != None:
		if parentItem.dropDownMenu != None:
			items = parentItem.dropDownMenu.items
	else:
		if item.parentMenu != None:
			items = item.parentMenu.items
	closeMenus(items)
	if len(item.items) > 0:
		dropDownMenu = item.dropDownMenu
		#获取位置和大小
		if dropDownMenu != None and dropDownMenu.visible == False:
			layoutStyle = dropDownMenu.layoutStyle
			location = FCPoint(clientX(item) + item.size.cx, clientY(item))
			if layoutStyle == "lefttoright" or layoutStyle == "righttoleft":
				location.x = clientX(item)
				location.y = clientY(item) + item.size.cy
			#设置弹出位置
			dropDownMenu.location = location
			dropDownMenu.visible = True
			adjustMenu(dropDownMenu)
			invalidate(item.paint)
			return
	invalidate(item.paint)

#重绘按钮
#item:菜单项
#paint:绘图对象
#clipRect:裁剪区域
def drawMenuItem(item, paint, clipRect):
	if item == paint.touchDownView:
		if item.pushedColor != None:
			paint.fillRect(item.pushedColor, 0, 0, item.size.cx, item.size.cy)
		else:
			if item.backColor != None:
				paint.fillRect(item.backColor, 0, 0, item.size.cx, item.size.cy)
	elif item == paint.touchMoveView:
		if item.hoveredColor != None:
			paint.fillRect(item.hoveredColor, 0, 0, item.size.cx, item.size.cy)
		else:
			if item.backColor != None:
				paint.fillRect(item.backColor, 0, 0, item.size.cx, item.size.cy)
	elif item.backColor != None:
		paint.fillRect(item.backColor, 0, 0, item.size.cx, item.size.cy)
	if item.textColor != None and len(item.text) > 0:
		tSize = paint.textSize(item.text, item.font)
		paint.drawText(item.text, item.textColor, item.font, (item.size.cx - tSize.cx) / 2, (item.size.cy - tSize.cy) / 2)
	if item.borderColor != None:
		paint.drawRect(item.borderColor, item.borderWidth, 0, 0, 0, item.size.cx, item.size.cy)
	if len(item.items) > 0:
		tR = 5
		drawPoints = []
		drawPoints.append(FCPoint(item.size.cx - 2, item.size.cy / 2))
		drawPoints.append(FCPoint(item.size.cx - 2 - tR * 2, item.size.cy / 2 - tR))
		drawPoints.append(FCPoint(item.size.cx - 2 - tR * 2, item.size.cy / 2 + tR))
		paint.fillPolygon(item.textColor, drawPoints)

#点击菜单项
#item:菜单项
def clickMenuItem(item):
	paintAll = False
	if item.parentMenu != None:
		if item.parentMenu.comboBox != None:
			index = -1
			for i in range(0, len(item.parentMenu.items)):
				if item.parentMenu.items[i] == item:
					index = i
					break
			item.parentMenu.comboBox.selectedIndex = index
			item.parentMenu.comboBox.text = item.parentMenu.items[index].text
			paintAll = True
	if len(item.items) == 0:
		for i in range(0, len(item.paint.views)):
			subView = item.paint.views[i]
			if subView.viewType == "menu":
				if subView.visible:
					subView.visible = False
					paintAll = True
	if paintAll:
		invalidate(item.paint)

#重绘按钮
#comboBox:下拉列表
#paint:绘图对象
#clipRect:裁剪区域
def drawComboBox(comboBox, paint, clipRect):
	if comboBox.backColor != None:
		paint.fillRect(comboBox.backColor, 0, 0, comboBox.size.cx, comboBox.size.cy)
	if comboBox.textColor != None and len(comboBox.text) > 0:
		tSize = paint.textSize(comboBox.text, comboBox.font)
		paint.drawText(comboBox.text, comboBox.textColor, comboBox.font, 5, (comboBox.size.cy - tSize.cy) / 2)
	if comboBox.borderColor != None:
		paint.drawRect(comboBox.borderColor, comboBox.borderWidth, 0, 0, 0, comboBox.size.cx, comboBox.size.cy)
	tR = 5
	drawPoints = []
	drawPoints.append(FCPoint(comboBox.size.cx - 5 - tR * 2, comboBox.size.cy / 2 - tR))
	drawPoints.append(FCPoint(comboBox.size.cx - 5, comboBox.size.cy / 2 - tR))
	drawPoints.append(FCPoint(comboBox.size.cx - 5 - tR, comboBox.size.cy / 2 + tR))
	paint.fillPolygon(comboBox.textColor, drawPoints)

#点击下拉菜单
#comboBox:下拉菜单
def clickComboBox(comboBox):
	showX = clientX(comboBox)
	showY = clientY(comboBox) + comboBox.size.cy
	comboBox.dropDownMenu.location = FCPoint(showX, showY)
	comboBox.dropDownMenu.visible = True
	adjustMenu(comboBox.dropDownMenu)
	invalidate(comboBox.paint)

#设置属性
#view:视图
#node:xml节点
def setAttributeDefault(view, child):
	if view.paint != None:
		if view.paint.defaultUIStyle == "dark":
			view.backColor = "rgb(0,0,0)"
			view.borderColor = "rgb(100,100,100)"
			view.textColor = "rgb(255,255,255)"
			view.scrollBarColor = "rgb(100,100,100)"
		elif view.paint.defaultUIStyle == "light":
			view.backColor = "rgb(255,255,255)"
			view.borderColor = "rgb(150,150,150)"
			view.textColor = "rgb(0,0,0)"
			view.scrollBarColor = "rgb(200,200,200)"
		for key in child.attrib:
			name = key.lower()
			value = child.attrib[key]
			if name == "location":
				xStr = value.split(',')[0]
				yStr = value.split(',')[1]
				if xStr.find("%") != -1:
					view.exAttributes["leftstr"] = xStr
				else:
					view.location.x = int(xStr)
				if yStr.find("%") != -1:
					view.exAttributes["topstr"] = yStr
				else:
					view.location.y = int(yStr)
			elif name == "size":
				xStr = value.split(',')[0]
				yStr = value.split(',')[1]
				if xStr.find("%") != -1:
					view.exAttributes["widthstr"] = xStr
				else:
					view.size.cx = int(xStr)
				if yStr.find("%") != -1:
					view.exAttributes["heightstr"] = yStr
				else:
					view.size.cy = int(yStr)
			elif name == "text":
				view.text = value
			elif name == "backcolor":
				lowerStr = value.lower()
				if lowerStr.find("rgb") == 0:
					view.backColor = value
				else:
					view.backColor = "none"
			elif name == "bordercolor":
				lowerStr = value.lower()
				if lowerStr.find("rgb") == 0:
					view.borderColor = value
				else:
					view.borderColor = "none"
			elif name == "textcolor":
				lowerStr = value.lower()
				if lowerStr.find("rgb") == 0:
					view.textColor = value
				else:
					view.textColor = "none"
			elif name == "layoutstyle":
				view.layoutStyle = value.lower()
			elif name == "align":
				view.align = value.lower()
			elif name == "cursor":
				view.cursor = value.lower()
			elif name == "vertical-align":
				view.verticalAlign = value.lower()
			elif name == "dock":
				view.dock = value.lower()
			elif name == "font":
				view.font = value
			elif name == "headerheight":
				view.headerHeight = float(value)
			elif name == "cornerradius":
				view.cornerRadius = float(value)
			elif name == "borderwidth":
				view.borderWidth = float(value)
			elif name == "splitmode":
				view.splitMode = value.lower()
			elif name == "autowrap":
				view.autoWrap = (value.lower() == "true")
			elif name == "tabindex":
				view.tabIndex = int(value)
			elif name == "tabstop":
				view.tabStop = (value.lower() == "true")
			elif name == "name":
				view.viewName = value
			elif name == "enabled":
				view.enabled = (value.lower() == "true")
			elif name == "showvscrollbar":
				view.showVScrollBar = (value.lower() == "true")
			elif name == "showhscrollbar":
				view.showHScrollBar = (value.lower() == "true")
			elif name == "visible":
				view.visible = (value.lower() == "true")
			elif name == "displayoffset":
				view.displayOffset = (value.lower() == "true")
			elif name == "checked":
				view.checked = (value.lower() == "true")
			elif name == "buttonsize":
				view.buttonSize = FCSize(int(value.split(',')[0]), int(value.split(',')[1]))
			elif name == "topmost":
				view.topMost = (value.lower() == "true")
			elif name == "selectedindex":
				view.selectedIndex = int(value)
			elif name == "src":
				view.src = value
			elif name == "backimage":
				view.backImage = value
			elif name == "groupname":
				view.groupName = value
			elif name == "allowdragscroll":
				view.allowDragScroll = (value.lower() == "true")
			elif name == "allowpreviewsevent":
				view.allowPreviewsEvent = (value.lower() == "true")
			elif name == "allowdrag":
				view.allowDrag =  (value.lower() == "true")
			elif name == "allowresize":
				view.allowResize =  (value.lower() == "true")
			elif name == "indent":
				view.indent = float(value)
			elif name == "showcheckbox":
				view.showCheckBox = (value.lower() == "true")
			elif name == "padding":
				view.padding = FCPadding(int(value.split(',')[0]), int(value.split(',')[1]), int(value.split(',')[2]), int(value.split(',')[3]))
			elif name == "margin":
				view.margin = FCPadding(int(value.split(',')[0]), int(value.split(',')[1]), int(value.split(',')[2]), int(value.split(',')[3]))
			elif name == "hoveredcolor":
				lowerStr = value.lower()
				if lowerStr.find("rgb") == 0:
					view.hoveredColor = value
				else:
					view.hoveredColor = "none"
			elif name == "pushedcolor":
				lowerStr = value.lower()
				if lowerStr.find("rgb") == 0:
					view.pushedColor = value
				else:
					view.pushedColor = "none"
			elif name == "layout":
				view.layout = value
			elif name == "width":
				if value.find("%") != -1:
					view.exAttributes["widthstr"] = value
				else:
					view.size.cx = int(value)
			elif name == "height":
				if value.find("%") != -1:
					view.exAttributes["heightstr"] = value
				else:
					view.size.cy = int(value)
			elif name == "top":
				if value.find("%") != -1:
					view.exAttributes["topstr"] = value
				else:
					view.location.y = int(value)
			elif name == "left":
				if value.find("%") != -1:
					view.exAttributes["leftstr"] = value
				else:
					view.location.x = int(value)
			else:
				view.exAttributes[name] = value

#读取Xml中的树节点
#tree 树
#parentNode 父节点
#xmlNode Xml节点
def readTreeXmlNodeDefault(tree, parentNode, xmlNode):
	treeNode = FCTreeNode()
	treeNode.value = xmlNode.attrib["text"]
	appendTreeNode(tree, treeNode, parentNode)
	for child in xmlNode:
		nodeName = child.tag.replace("{facecat}", "").lower()
		if nodeName == "node":
			readTreeXmlNodeDefault(tree, treeNode, child)

#读取Xml
#paint 绘图对象
#node节点
#parent 父视图
def readXmlNodeDefault(paint, node, parent):
	for child in node:
		view = None
		typeStr = ""
		nodeName = child.tag.replace("{facecat}", "").lower()
		if nodeName == "div" or nodeName == "view":
			if "type" in child.attrib:
				typeStr = child.attrib["type"]
			if typeStr == "splitlayout":
				view = FCSplitLayoutDiv()
			elif typeStr == "layout":
				view = FCLayoutDiv()
			elif typeStr == "tab":
				view = FCTabView()
			elif typeStr == "tabpage":
				view = FCTabPage()
			elif typeStr == "radio":
				view = FCRadioButton()
				view.backColor = "none"
			elif typeStr == "checkbox":
				view = FCCheckBox()
				view.backColor = "none"
			elif typeStr == "button":
				view = FCButton()
			elif typeStr == "text" or typeStr == "range" or typeStr == "datetime":
				view = FCTextBox()
			elif typeStr == "custom":
				cid = child.attrib["cid"]
				view = FCDiv()
				view.viewType = cid
			else:
				view = FCDiv()
		elif nodeName == "table":
			view = FCGrid()
		elif nodeName == "chart":
			view = FCChart()
		elif nodeName == "tree":
			view = FCTree()
		elif nodeName == "select":
			view = FCComboBox()
		elif nodeName == "calendar":
			view = FCCalendar()
		elif nodeName == "label":
			view = FCLabel()
		elif nodeName == "input":
			if "type" in child.attrib:
				typeStr = child.attrib["type"]
			if typeStr == "radio":
				view = FCRadioButton()
				view.backColor = "none"
			elif typeStr == "checkbox":
				view = FCCheckBox()
				view.backColor = "none"
			elif typeStr == "button":
				view = FCButton()
			elif typeStr == "text" or typeStr == "range" or typeStr == "datetime":
				view = FCTextBox()
			elif typeStr == "custom":
				cid = child.attrib["cid"]
				view = FCView()
				view.viewType = cid
			else:
				view = FCButton()
		else:
			view = FCView()
		view.paint = paint
		view.parent = parent
		setAttributeDefault(view, child)
		if view != None:
			if typeStr == "tabpage":
				tabButton = FCView()
				tabButton.viewType = "tabbutton"
				if "headersize" in child.attrib:
					atrHeaderSize = child.attrib["headersize"]
					tabButton.size = FCSize(int(atrHeaderSize.split(',')[0]), int(atrHeaderSize.split(',')[1]))
				else:
					tabButton.size = FCSize(100, 20)
				if view.paint.defaultUIStyle == "dark":
					tabButton.backColor = "rgb(0,0,0)"
					tabButton.borderColor = "rgb(100,100,100)"
					tabButton.textColor = "rgb(255,255,255)"
				elif view.paint.defaultUIStyle == "light":
					tabButton.backColor = "rgb(255,255,255)"
					tabButton.borderColor = "rgb(150,150,150)"
					tabButton.textColor = "rgb(0,0,0)"
				tabButton.text = view.text
				tabButton.paint = paint
				addTabPage(view.parent, view, tabButton)
			else:
				if parent != None:
					parent.views.append(view)
				else:
					paint.views.append(view)
			if typeStr == "splitlayout":
				if "datumsize" in child.attrib:
					atrDatum = child.attrib["datumsize"]
					view.size = FCSize(int(atrDatum.split(',')[0]), int(atrDatum.split(',')[1]))
				splitter = FCView()
				splitter.paint = paint
				splitter.parent = view
				if view.paint.defaultUIStyle == "dark":
					splitter.backColor = "rgb(100,100,100)"
				elif view.paint.defaultUIStyle == "light":
					splitter.backColor = "rgb(150,150,150)"
				if "candragsplitter" in child.attrib:
					if child.attrib["candragsplitter"] == "true":
						splitter.allowDrag = True
				view.splitter = splitter
				splitterposition = child.attrib["splitterposition"]
				splitStr = splitterposition.split(',')
				if len(splitStr) >= 4:
					splitRect = FCRect(float(splitStr[0]), float(splitStr[1]), float(splitStr[2]), float(splitStr[3]))
					splitter.location = FCPoint(splitRect.left, splitRect.top)
					splitter.size = FCSize(splitRect.right - splitRect.left, splitRect.bottom - splitRect.top)
				else:
					sSize = float(splitStr[1])
					sPosition = float(splitStr[0])
					if view.layoutStyle == "lefttoright" or view.layoutStyle == "righttoleft":
						splitter.location = FCPoint(sPosition, 0)
						splitter.size = FCSize(sSize, view.size.cy)
					else:
						splitter.location = FCPoint(0, sPosition)
						splitter.size = FCSize(view.size.cx, sSize)
				readXmlNodeDefault(paint, child, view)
				subViews = view.views
				view.firstView = subViews[0]
				view.secondView = subViews[1]
				view.views.append(splitter)
				view.oldSize = FCSize(view.size.cx, view.size.cy)
				resetSplitLayoutDiv(view)
			elif typeStr == "tab":
				readXmlNodeDefault(paint, child, view)
				tabPages = view.tabPages
				if len(tabPages) > 0:
					if "selectedindex" in child.attrib:
						strSelectedIndex = child.attrib["selectedindex"]
						selectedIndex = int(strSelectedIndex)
						if selectedIndex >= 0 and selectedIndex < len(tabPages):
							tabPages[selectedIndex].visible = True
						else:
							tabPages[len(tabPages) - 1].visible = True
					else:
						tabPages[len(tabPages) - 1].visible = True
			elif nodeName == "table":
				for tChild in child:
					if tChild.tag.replace("{facecat}", "") == "tr":
						gridRow = None
						for sunNode in tChild:
							sunNodeName = sunNode.tag.lower().replace("{facecat}", "")
							if sunNodeName == "th":
								gridColumn = FCGridColumn()
								if view.paint.defaultUIStyle == "light":
									gridColumn.backColor = "rgb(230,230,230)"
									gridColumn.borderColor = "rgb(150,150,150)"
									gridColumn.textColor = "rgb(0,0,0)"
								elif view.paint.defaultUIStyle == "dark":
									gridColumn.backColor = "rgb(50,50,50)"
									gridColumn.borderColor = "rgb(100,100,100)"
									gridColumn.textColor = "rgb(255,255,255)"
								gridColumn.width = 100
								if "text" in sunNode.attrib:
									gridColumn.text = sunNode.attrib["text"]
								if "width" in sunNode.attrib:
									strWidth = sunNode.attrib["width"]
									if strWidth.find("%") != -1:
										gridColumn.widthStr = strWidth
									else:
										gridColumn.width = float(strWidth)
								if "backcolor" in sunNode.attrib:
									gridColumn.backColor = sunNode.attrib["backcolor"]
								if "textcolor" in sunNode.attrib:
									gridColumn.textColor = sunNode.attrib["textcolor"]
								if "bordercolor" in sunNode.attrib:
									gridColumn.borderColor = sunNode.attrib["bordercolor"]
								if "font" in  sunNode.attrib:
									gridColumn.font = sunNode.attrib["font"]
								view.columns.append(gridColumn)
							elif sunNodeName == "td":
								if gridRow == None:
									gridRow = FCGridRow()
									view.rows.append(gridRow)
								gridCell = FCGridCell()
								gridCell.value = sunNode.text
								gridRow.cells.append(gridCell)
			elif nodeName == "tree":
				treeColumn = FCTreeColumn()
				view.columns.append(treeColumn)
				columnWidth = 0
				for tChild in child:
					if tChild.tag.replace("{facecat}", "") == "nodes":
						for sunNode in tChild:
							sunNodeName = sunNode.tag.lower().replace("{facecat}", "")
							if sunNodeName == "node":
								readTreeXmlNodeDefault(view, None, sunNode)
					elif tChild.tag.replace("{facecat}", "") == "tr":
						gridRow = None
						for sunNode in tChild:
							sunNodeName = sunNode.tag.lower().replace("{facecat}", "")
							if sunNodeName == "th":
								if "width" in sunNode.attrib:
									strWidth = sunNode.attrib["width"]
									if strWidth.find("%") != -1:
										treeColumn.widthStr = strWidth
									else:
										columnWidth += float(strWidth)	
				if columnWidth > 0:
					treeColumn.width = columnWidth
			elif view.viewType == "textbox":
				if len(view.viewName) > 0:
					view.exView = True
					paint.init()
					paint.gdiPlusPaint.createView(view.viewType, view.viewName)
					if view.paint.defaultUIStyle == "dark":
						view.backColor = "rgb(0,0,0)"
						view.borderColor = "rgb(100,100,100)"
						view.textColor = "rgb(255,255,255)"
					elif view.paint.defaultUIStyle == "light":
						view.backColor = "rgb(255,255,255)"
						view.borderColor = "rgb(150,150,150)"
						view.textColor = "rgb(0,0,0)"
				for key in child.attrib:
					setViewAttribute(view, key.lower(), child.attrib[key])
			elif nodeName == "calendar":
				initCalendar(view)
				view.selectedDay = getYear(view.years, 2022).months[10].days[1]
			elif nodeName == "select":
				view.dropDownMenu = FCMenu()
				view.dropDownMenu.comboBox = view
				addView(view.dropDownMenu, paint)
				view.dropDownMenu.size.cx = view.size.cx
				for tChild in child:
					if tChild.tag.replace("{facecat}", "") == "option":
						menuItem = FCMenuItem()
						addMenuItem(menuItem, view.dropDownMenu)
						setAttributeDefault(menuItem, tChild)
				if len(view.dropDownMenu.items) > 0:
					if "selectedindex" in child.attrib:
						strSelectedIndex = child.attrib["selectedindex"]
						selectedIndex = int(strSelectedIndex)
						if selectedIndex >= 0 and selectedIndex < len(view.dropDownMenu.items):
							view.selectedIndex = selectedIndex
							view.text = view.dropDownMenu.items[selectedIndex].text
						else:
							view.selectedIndex = 0
							view.text = view.dropDownMenu.items[0].text
					else:
						view.selectedIndex = 0
						view.text = view.dropDownMenu.items[0].text
			else:
				if view.viewType != "chart":
					readXmlNodeDefault(paint, child, view)

#绘制视图
#view:视图
#paint:绘图对象
#clipRect:区域
def onPaintDefault(view, paint, clipRect):
	if view.onPaint != None:
		view.onPaint(view, paint, clipRect)
		return
	if view.viewType == "radiobutton":
		drawRadioButton(view, paint, clipRect)
	elif view.viewType == "checkbox":
		drawCheckBox(view, paint, clipRect)
	elif view.viewType == "chart":
		drawChart(view, paint, clipRect)
	elif view.viewType == "grid":
		drawDiv(view, paint, clipRect)
		drawGrid(view, paint, clipRect)
	elif view.viewType == "tree":
		drawDiv(view, paint, clipRect)
		drawTree(view, paint, clipRect)
	elif view.viewType == "label":
		if view.textColor != "none":
			tSize = paint.textSize(view.text, view.font)
			paint.drawText(view.text, view.textColor, view.font, 0, (view.size.cy - tSize.cy) / 2)
	elif view.viewType == "div" or view.viewType =="tabpage" or view.viewType =="tabview" or view.viewType =="layout":
		drawDiv(view, paint, clipRect)
	elif view.viewType == "calendar":
		drawCalendar(view, paint)
	elif view.exView:
		paint.gdiPlusPaint.paintView(view.viewName, 0, 0, int(view.size.cx), int(view.size.cy))
	elif view.viewType == "menuitem":
		drawMenuItem(view, paint, clipRect)
	elif view.viewType == "combobox":
		drawComboBox(view, paint, clipRect)
	else:
		drawButton(view, paint, clipRect)

#绘制视图边线
#view:视图
#paint:绘图对象
#clipRect:区域
def onPaintBorderDefault(view, paint, clipRect):
	if view.onPaintBorder != None:
		view.onPaintBorder(view, paint, clipRect)
		return
	if view.viewType == "grid":
		drawGridScrollBar(view, paint, clipRect)
		drawDivBorder(view, paint, clipRect)
	elif view.viewType == "tree":
		drawTreeScrollBar(view, paint, clipRect)
		drawDivBorder(view, paint, clipRect)
	elif view.viewType == "div" or view.viewType =="tabpage" or view.viewType =="tabview" or view.viewType =="layout" or view.viewType == "menu":
		drawDivBorder(view, paint, clipRect)
		drawDivScrollBar(view, paint, clipRect)

#视图的鼠标移动方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onMouseMoveDefault(view, mp, buttons, clicks, delta):
	if view.onMouseMove != None:
		view.onMouseMove(view, mp, buttons, clicks, delta)
		return
	firstTouch = False
	secondTouch = False
	firstPoint = mp
	secondPoint = mp
	if buttons == 1:
		firstTouch = True
	elif buttons == 2:
		secondTouch = True
	if view.viewType == "grid":
		touchMoveGrid(view, firstTouch, firstPoint, secondTouch, secondPoint)
		invalidateView(view)
	elif view.viewType == "tree":
		touchMoveTree(view, firstTouch, firstPoint, secondTouch, secondPoint)
		invalidateView(view)
	elif view.viewType == "chart":
		touchMoveChart(view, firstTouch, firstPoint, secondTouch, secondPoint)
		invalidateView(view)
	elif view.viewType == "div" or view.viewType =="layout" or view.viewType == "menu":
		touchMoveDiv(view, firstTouch, firstPoint, secondTouch, secondPoint)
		invalidateView(view)
	elif view.viewType == "button":
		invalidateView(view)
	elif view.viewType == "menuitem":
		touchMoveMenuItem(view)
	else:
		if view.allowDrag and view.parent != None and view.parent.viewType == "split" and view.parent.splitter == view:
			if view.parent.layoutStyle == "lefttoright" or view.parent.layoutStyle == "righttoleft":
				view.paint.gdiPlusPaint.setCursor("SizeWE")
			else:
				view.paint.gdiPlusPaint.setCursor("SizeNS")
		invalidateView(view)
		
#视图的鼠标按下方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onMouseDownDefault(view, mp, buttons, clicks, delta):
	if view.onMouseDown != None:
		view.onMouseDown(view, mp, buttons, clicks, delta)
		return
	firstTouch = False
	secondTouch = False
	firstPoint = mp
	secondPoint = mp
	if buttons == 1:
		firstTouch = True
	elif buttons == 2:
		secondTouch = True
	if view.viewType == "grid":
		touchDownGrid(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
		invalidateView(view)
	elif view.viewType == "tree":
		touchDownTree(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
		invalidateView(view)
	elif view.viewType == "div" or view.viewType =="layout" or view.viewType == "menu":
		touchDownDiv(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
		invalidateView(view)
	elif view.viewType == "button":
		invalidateView(view)
	elif view.viewType == "calendar":
		clickCalendar(view, firstPoint)
	elif view.viewType == "chart":
		touchDownChart(view, firstTouch, firstPoint, secondTouch, secondPoint)
		invalidateView(view)

#视图的鼠标抬起方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onMouseUpDefault(view, mp, buttons, clicks, delta):
	if view.onMouseUp != None:
		view.onMouseUp(view, mp, buttons, clicks, delta)
		return
	firstTouch = False
	secondTouch = False
	firstPoint = mp
	secondPoint = mp
	if buttons == 1:
		firstTouch = True
	elif buttons == 2:
		secondTouch = True
	if view.viewType == "grid":
		touchUpGrid(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
	elif view.viewType == "tree":
		touchUpTree(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
	elif view.viewType == "div" or view.viewType =="layout" or view.viewType == "menu":
		touchUpDiv(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
	elif view.viewType == "chart":
		view.firstTouchIndexCache = -1
		view.secondTouchIndexCache = -1
	invalidateView(view)	

#视图的鼠标点击方法
#view 视图
#firstTouch:是否第一次触摸 
#firstPoint:第一次触摸的坐标 
#secondTouch:是否第二次触摸 
#secondPoint:第二次触摸的坐标
#clicks 点击次数
def onClickDefault(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks):
	if view.onClick != None:
		view.onClick(view, firstTouch, firstPoint, secondTouch, secondPoint, clicks)
		return
	if view.viewType == "radiobutton":
		clickRadioButton(view, firstPoint)
		if view.parent != None:
			invalidateView(view.parent)
		else:
			invalidateView(view)
	elif view.viewType == "checkbox":
		clickCheckBox(view, firstPoint)
		invalidateView(view)
	elif view.viewType == "tabbutton":
		tabView = view.parent
		for i in range(0, len(tabView.tabPages)):
			if tabView.tabPages[i].headerButton == view:
				selectTabPage(tabView, tabView.tabPages[i])
		invalidateView(tabView)
	elif view.viewType == "menuitem":
		clickMenuItem(view)
	elif view.viewType == "combobox":
		clickComboBox(view)

#视图的鼠标滚动方法
#view 视图
#mp 坐标
#buttons 按钮 0未按下 1左键 2右键
#clicks 点击次数
#delta 滚轮值
def onMouseWheelDefault(view, mp, buttons, clicks, delta):
	if view.onMouseWheel != None:
		view.onMouseWheel(view, mp, buttons, clicks, delta)
		return
	if view.viewType == "grid":
		touchWheelGrid(view, delta)
		invalidateView(view)
	elif view.viewType == "tree":
		touchWheelTree(view, delta)
		invalidateView(view)
	elif view.viewType == "div" or view.viewType =="layout" or view.viewType =="menu":
		touchWheelDiv(view, delta)
		invalidateView(view)
	elif view.viewType == "chart":
		if delta > 0:
			zoomOutChart(view)
		elif delta < 0:
			zoomInChart(view)
		invalidateView(view)

#视图的键盘按下方法
#view 视图
#value 按键值
def onKeyDownDefault(view, value):
	if view.onKeyDown != None:
		view.onKeyDown(view, value)
		return
	if view.viewType == "chart":
		keyDownChart(view, value)
		invalidateView(view)

#视图的键盘抬起方法
#view 视图
#value 按键值
def onKeyUpDefault(view, value):
	if view.onKeyUp != None:
		view.onKeyUp(view, value)
		return

#视图的输入方法
#view 视图
#value 按键值
def onCharDefault(view, value):
	key = value

#消息循环
def WndProcDefault(paint, hwnd, msg, wParam, lParam):
	global mainWindowHandle
	if msg == 0x0020:
		if lParam == 33554433:
			return 1	
	elif msg == WM_DESTROY:
		if hwnd == mainWindowHandle:
			user32.PostQuitMessage(0)
			paint.hWnd = 0
	elif msg == paint.pInvokeMsgID:
		vID = int(wParam)
		args = None
		view = None
		paint.lock.acquire()
		if vID in paint.invokeViews:
			view = paint.invokeViews[vID]
			args = paint.invokeArgs[vID]
			paint.invokeViews.pop(vID)
			paint.invokeArgs.pop(vID)
		paint.lock.release()
		if view != None:
			if view.onInvoke != None:
				view.onInvoke(view, args)
			elif paint.onInvoke != None:
				paint.onInvoke(view, args)
	if hwnd == paint.hWnd:
		if msg == WM_ERASEBKGND:
			return 1
		#大小改变
		elif msg == WM_SIZE:
			rect = RECT()
			user32.GetClientRect(paint.hWnd, ct.byref(rect))
			wWidth = rect.right - rect.left
			wHeight = rect.bottom - rect.top
			if wWidth > 0 and wHeight > 0:
				if paint.size.cx != wWidth or paint.size.cy != wHeight:
					paint.size = FCSize(wWidth, wHeight)
					if paint.onUpdateView != None:
						paint.onUpdateView(paint.views)
					else:
						updateViewDefault(paint.views)
				invalidate(paint)
		#鼠标左键按下
		elif msg == WM_LBUTTONDOWN:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			handleMouseDown(mp, 1, 1, 0, paint)
		#鼠标左键按下
		elif msg == WM_RBUTTONDOWN:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			handleMouseDown(mp, 2, 1, 0, paint)
		#鼠标左键双击
		elif msg == WM_LBUTTONDBLCLK:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			handleMouseDown(mp, 1, 2, 0, paint)
		#鼠标左键双击
		elif msg == WM_RBUTTONDBLCLK:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			handleMouseDown(mp, 2, 2, 0, paint)
		#鼠标左键抬起
		elif msg == WM_LBUTTONUP:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			if paint.isDoubleClick:
				handleMouseUp(mp, 1, 2, 0, paint)
			else:
				handleMouseUp(mp, 1, 1, 0, paint)
		#鼠标左键抬起
		elif msg == WM_RBUTTONUP:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			if paint.isDoubleClick:
				handleMouseUp(mp, 2, 2, 0, paint)
			else:
				handleMouseUp(mp, 2, 1, 0, paint)
		#鼠标滚动
		elif msg == WM_MOUSEWHEEL:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			if wParam > 4000000000:
				handleMouseWheel(mp, 0, 0, -1, paint)
			else:
				handleMouseWheel(mp, 0, 0, 1, paint)
		#鼠标移动
		elif msg == WM_MOUSEMOVE:
			point = POINT()
			user32.GetCursorPos(ct.byref(point))
			user32.ScreenToClient(hwnd, ct.byref(point))
			mp = FCPoint(point.x, point.y)
			mp.x /= paint.scaleFactorX
			mp.y /= paint.scaleFactorY
			if wParam == 1:
				handleMouseMove(mp, 1, 1, 0, paint)
			elif wParam == 2:
				handleMouseMove(mp, 2, 1, 0, paint)
			else:
				handleMouseMove(mp, 0, 0, 0, paint)
		#重绘
		elif msg == WM_PAINT:
			rect = RECT()
			user32.GetClientRect(paint.hWnd, ct.byref(rect))
			wWidth = rect.right - rect.left
			wHeight = rect.bottom - rect.top
			if wWidth > 0 and wHeight > 0:
				if paint.size.cx != wWidth or paint.size.cy != wHeight:
					paint.size = FCSize(wWidth, wHeight)
					if paint.onUpdateView != None:
						paint.onUpdateView(paint.views)
					else:
						updateViewDefault(paint.views)
				hDC = user32.GetDC(paint.hWnd)
				paint.hdc = hDC
				paint.clipRect = None
				paint.size = FCSize(wWidth, wHeight)
				allRect = FCRect(0, 0, paint.size.cx, paint.size.cy)
				drawRect = FCRect(0, 0, (paint.size.cx / paint.scaleFactorX), (paint.size.cy / paint.scaleFactorY))
				if paint.gdiPlusPaint != None:
					paint.gdiPlusPaint.setScaleFactor(paint.scaleFactorX, paint.scaleFactorY)
				paint.beginPaint(allRect, drawRect)
				if paint.onRenderViews:
					paint.onRenderViews(paint.views, paint, drawRect)
				else:
					renderViews(paint.views, paint, drawRect)
				paint.endPaint()
				user32.ReleaseDC(paint.hWnd, hDC)
	#输入法事件
		elif msg == 0x010F or msg == 0x0286 or msg == 0x0281:
			if paint.gdiPlusPaint != None:
				paint.gdiPlusPaint.onMessage(hwnd,msg,wParam,lParam)
		#按键输入
		elif msg == WM_CHAR or msg == WM_KEYDOWN or msg == WM_SYSKEYDOWN or msg == WM_KEYUP or msg == WM_SYSKEYUP:
			if paint.focusedView != None:
				if paint.focusedView.exView:
					if paint.gdiPlusPaint != None:
						paint.gdiPlusPaint.onMessage(hwnd,msg,wParam,lParam)
						invalidateView(paint.focusedView)
				if msg == WM_KEYDOWN or msg == WM_SYSKEYDOWN:
					if paint.focusedView.onKeyDown != None:
						onKeyDownDefault(paint.focusedView, wParam)
					else:
						if paint.onKeyDown != None:
							paint.onKeyDown(paint.focusedView, wParam)
						else:
							onKeyDownDefault(paint.focusedView, wParam)
				elif msg == WM_KEYUP or msg == WM_SYSKEYUP:
					if paint.focusedView.onKeyUp != None:
						onKeyUpDefault(paint.focusedView, wParam)
					else:
						if paint.onKeyUp != None:
							paint.onKeyUp(paint.focusedView, wParam)
						else:
							onKeyUpDefault(paint.focusedView, wParam)	
				elif msg == WM_CHAR:
					if paint.onChar != None:
						paint.onChar(paint.focusedView, wParam)
					else:
						onCharDefault(paint.focusedView, wParam)	
	return DefWindowProc(hwnd,msg,wParam,lParam)

#加载FaceCat
#paint:绘图对象
#xml:Xml内容
def renderFaceCat(paint, xml):
	root  = ET.fromstring(xml)
	for child in root:
		if child.tag == "{facecat}body":
			readXmlNodeDefault(paint, child, None)
	#获取窗体大小
	rect = RECT()
	user32.GetClientRect(paint.hWnd, ct.byref(rect))
	#更新布局
	if rect.right - rect.left > 0 and rect.bottom - rect.top > 0:
		paint.size = FCSize(rect.right - rect.left, rect.bottom - rect.top)
		if paint.onUpdateView != None:
			paint.onUpdateView(paint.views)
		else:
			updateViewDefault(paint.views)
		invalidate(paint)

mainWindowHandle = 0 #主窗体句柄
showWindowState = 0 #显示的窗体状态
showWindowSize = FCSize(0, 0) #显示的窗体大小
showWindowLocation = FCPoint(0, 0) #显示的窗体位置
centerScreenWindow = False #是否居中显示

#设置显示最大化
def setMaxWindow():
	global showWindowState
	showWindowState = 1

#隐藏窗体
def hideWindow(paint):
	global showWindowState
	showWindowState = 1
	user32.ShowWindow(paint.hWnd, SW_HIDE)

#设置要创建的窗体大小
def setWindowRect(location, size):
	global showWindowSize
	global showWindowLocation
	showWindowLocation = location
	showWindowSize = size

#设置窗体的位置
def setWindowLocation(location):
	global showWindowLocation
	showWindowLocation = location

#是否居中显示
def setCenterScreen(isCenter):
	global centerScreenWindow
	centerScreenWindow = isCenter

#设置窗体的大小
def setWindowSize(size):
	global showWindowSize
	showWindowSize = size

#显示窗体
def showWindow(paint):
	global mainWindowHandle
	global showWindowState
	global showWindowSize
	global showWindowLocation
	if showWindowSize.cx > 0 and showWindowSize.cy > 0:
		global centerScreenWindow
		if centerScreenWindow:
			wRect = RECT()
			user32.GetWindowRect(user32.GetDesktopWindow(), ct.byref(wRect))
			showWindowLocation.x = int((wRect.right - wRect.left - showWindowSize.cx) / 2)
			showWindowLocation.y = int((wRect.bottom - wRect.top - showWindowSize.cy) / 2)
			centerScreenWindow = False
		user32.MoveWindow(paint.hWnd, showWindowLocation.x, showWindowLocation.y, showWindowSize.cx, showWindowSize.cy, True)
	if showWindowState == 1:
		user32.ShowWindow(paint.hWnd, SW_SHOWMAXIMIZED)
	else:
		user32.ShowWindow(paint.hWnd, SW_SHOW)
	user32.UpdateWindow(paint.hWnd)
	showWindowState = 0
	showWindowSize = FCSize(0, 0)
	showWindowLocation = FCPoint(0, 0)
	if paint.hWnd == mainWindowHandle:
		msg = cwintypes.MSG()
		pmsg = ct.byref(msg)
		while res := user32.GetMessageW(pmsg, None, 0, 0):
			if res < 0:
				break
			user32.TranslateMessage(pmsg)
			user32.DispatchMessageW(pmsg)

lastWndClass = None
#创建默认的窗体
def createMainWindow(paint, title, wndProc):
	global mainWindowHandle
	global lastWndClass
	clsName = str(uuid.uuid4())
	wcx = WNDCLASSEXW()
	wcx.cbSize = ct.sizeof(WNDCLASSEXW)
	wcx.lpfnWndProc = WNDPROC(wndProc)
	wcx.style = CS_HREDRAW | CS_VREDRAW | CS_DBLCLKS
	wcx.hInstance = kernel32.GetModuleHandleW(None)
	wcx.lpszClassName = clsName
	lastWndClass = wcx
	res = user32.RegisterClassExW(ct.byref(wcx))
	hwnd = CreateWindowEx(0, clsName, title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, None, wcx.hInstance, None)
	paint.hWnd = hwnd
	mainWindowHandle = hwnd

#创建默认的窗体
def createWindow(paint, title, wndProc):
	global lastWndClass
	clsName = str(uuid.uuid4())
	wcx = WNDCLASSEXW()
	wcx.cbSize = ct.sizeof(WNDCLASSEXW)
	wcx.lpfnWndProc = WNDPROC(wndProc)
	wcx.style = CS_HREDRAW | CS_VREDRAW | CS_DBLCLKS
	wcx.hInstance = kernel32.GetModuleHandleW(None)
	wcx.lpszClassName = clsName
	lastWndClass = wcx
	res = user32.RegisterClassExW(ct.byref(wcx))
	hwnd = CreateWindowEx(0, clsName, title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, 0, None, wcx.hInstance, None)
	paint.hWnd = hwnd
	
	