from OxyPlot import *
from System import *
from System.IO import *
import math

def Color(r, g, b, a = 255, hascmyk=False, c=0, m=0, y=0, k=0):
	color = OxyColor()
	color.R, color.G, color.B, color.A = r, g, b, a
	color.HasCmyk = hascmyk
	color.C, color.M, color.Y, color.K = c, m, y, k
	return color

def ColorFromString(color):
	# possible opts are #RRGGBB [ cmyk(c,m,y,k)]
	c, m ,y, k = 0, 0, 0, 0
	hascmyk = False

	if color.find('cmyk') > 0:
		s = color.split(' ')[1].strip()
		color = color.split(' ')[0].strip()
		s = s.replace('cmyk(', '').replace(')', '')
		z = s.split(',')
		c = float(z[0])
		m = float(z[1])
		y = float(z[2])
		k = float(z[3])
		hascmyk = True
		
	if color.startswith('#'):
		color = '0x' + color[1:]
	
	color = int(color, 0)
	
	return Color(
		(color >> 16) & 255,
		(color >>  8) & 255,
		(color >>  0) & 255,
		255 if hascmyk else 255 - (color >> 24) & 255,
		hascmyk, c, m, y, k
	)

def TickInterval(xMinValue, xMaxValue, minTickCount = 3, maxTickCount = 6):
	TickIntervals = [0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 25]
	
	for item in TickIntervals:
		tickCount = math.ceil(xMaxValue / item) + math.ceil(abs(xMinValue) / item) + 1
		
		if minTickCount <= tickCount <= maxTickCount:
			return item
	
	assert False, 'There is no tick interval value for selected range.'

def SplitString (inputStr, maxLen):
	strLen = 0
	resStr = ''
	
	for word in inputStr.split():
		wordLen = len(word)
		
		if strLen + wordLen <= maxLen:
			resStr = resStr + word + ' '
			strLen = strLen + wordLen + 1
		else:
			resStr = resStr + "\r\n" + word + ' '
			strLen = wordLen + 1
	
	return resStr
