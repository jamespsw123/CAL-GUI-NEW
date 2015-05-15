# wxpython menu&toolbar practice
# IR_sensor Branch
import time
import wx
import os
import serial
import spidev

import wx.aui,wx.lib.intctrl, wx.lib.scrolledpanel
import wx.lib.agw.flatnotebook as fnb
import numpy as np
from numpy import arange, sin, pi
import matplotlib
matplotlib.interactive( True )
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import mygrid
import panelOne
import panelTwo
import panelThree
import tempSettingOne
import tempSettingTwo
import GasQuenching
from STM import *
from RPI_I2C_ARDUINO import *
from FastRead import *


addr = 0x04  
STX = chr(2)
ETX = chr(3)
CR = chr(13)

"""
ser = serial.Serial(
				port = '/dev/ttyUSB0',
				baudrate = 9600,
				bytesize = serial.EIGHTBITS,
				parity = serial.PARITY_EVEN,
				stopbits = serial.STOPBITS_ONE,
				timeout = 0.2
				)
"""

# read temperature from (mcp3008+ad8495) module
def read3008(channel):
	data = ReadChannel(channel) # ReadChannel is defined in FastRead.py, assume thermocouple is on channel 0
	volt = ConvertVolts(data, 3)
	# the temperature-volt relationship of thermocouple amplifier AD8495 is:
	# temp = (Vout - 1.25)/0.005
	temp = (volt - 1.25)/0.005
	return temp



# to convert time interval list into a list of time coordinates for drawing the presets
def newlist(l):
	for i in range(len(l)):
		if i != 0:
			l[i] = l[i] +l[i-1]
	return l

def RunStepper(position, speed,SampleLength,position_num):
	# convert distance unit mm to stepper motor's microsteps
	# 1 stepper motor step equals 1.8 degree,
	# 16 micro-steps equals 1 step
	if position_num == 1:
		x = 1800
	elif position_num == 2:
		x = 1490
	elif position_num == 3:
		x = 1080
	elif position_num == 4:
		x = 750
	distance_ = int(float(x - position-SampleLength)*(3200/(math.pi*70)))
	distance_ = str(distance_)
	Distance = distance_ + 'Dis'  
	# convert speed unit rpm to stepper motor's microsteps/sec
	speed_ = int(float(speed)*(3200/60))
	speed_ = str(speed_)
	Speed = speed_ + 'Spd' 
	position = str(position_num) + 'P'
	direct = '0' + 'E'# 'E' stands for end.
	cmd = Distance + Speed + position + direct
	communication_send(addr, "stm", cmd)



def dig_convert(number, n):
	number = str(number)
	while len(number) < n:
		number = '0' + number
	return number



def hex_convert(number):
	number = hex(number)[2:]
	if len(number) > 4 :
		print "Value more than FFFF, invalid"
	else:
		while len(number) < 4:
			number = '0' + number
		#print number
		return number



def readlineCR(port):
	rv = ""
	while 1:
		ch = port.read()
		rv += ch
		if ch == '\r' or ch == CR:
			return rv

def getPV(slave, port):
	port.write(STX+slave+"010WRDD0002,01"+ETX+CR)
	return  readlineCR(port)

def getCSP(slave, port):
	port.write(STX+slave+"010WRDD0120,01"+ETX+CR)
	return  readlineCR(port)

def getUPR(slave, port):
	port.write(STX+slave+"010WRDD0201,01"+ETX+CR)
	return  readlineCR(port)

def getDNR(slave, port):
	port.write(STX+slave+"010WRDD0202,01"+ETX+CR)
	return  readlineCR(port)

def getPID_P(slave, port):
	port.write(STX+slave+"010WRDD0105,01"+ETX+CR)
	return  readlineCR(port)

def getPID_I(slave, port):
	port.write(STX+slave+"010WRDD0106,01"+ETX+CR)
	return  readlineCR(port)

def getPID_D(slave, port):
	port.write(STX+slave+"010WRDD0107,01"+ETX+CR)
	return  readlineCR(port)

def setTemp(slave, temps1, port):
	#Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	message = STX+Slave_Address+"01"+"0"+"WRW"+"01"+"D0114,"+str(hex_convert(temps1)).upper()+ETX+CR
	port.write(message)
	#print readlineCR(port)

def setRamp(slave, Ramp, UD, port):
	#Master_Number = "01"
	Slave_Address = dig_convert(slave, 2)
	if UD == 1:
		D_Register = "D0201,"
		message = STX+Slave_Address+"01"+"0"+"WRW"+"01"+D_Register+str(hex_convert(Ramp)).upper()+ETX+CR
		#message2 = STX+Slave_Address+"01"+"0"+"WRW"+"01"+"D0202,"+str(hex_convert(Ramp)).upper()+ETX+CR
		#print "setRamp"
		port.write(message)
		#print readlineCR(port)[1:]
		#port.write(message2)
		#print readlineCR(port)[1:]
	elif UD == -1:
		D_Register = "D0202,"
		message = STX+Slave_Address+"01"+"0"+"WRW"+"01"+D_Register+str(hex_convert(Ramp)).upper()+ETX+CR
		#message2 = STX+Slave_Address+"01"+"0"+"WRW"+"01"+"D0201,"+str(hex_convert(Ramp)).upper()+ETX+CR
		#print "setRamp"
		port.write(message)
		#print readlineCR(port)[1:]
		#port.write(message2)
		#print readlineCR(port)[1:]
	
# creating Notebook class
class Notebook(fnb.FlatNotebook):
	def __init__(self, parent):
		windowstyle = fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NO_X_BUTTON
		fnb.FlatNotebook.__init__(self, parent, wx.ID_ANY, agwStyle=windowstyle)

		self.SetTabAreaColour('white')
		#self.SetActiveTabTextColour('black')
		self.tabOne = panelOne.TabPanel(self)
		self.tabTwo = panelTwo.TabPanel(self)
		self.tabThree = panelThree.TabPanel(self)
		
		

		self.AddPage(self.tabOne, "Furnace One")
		self.AddPage(self.tabTwo, "Furnace Two")
		self.AddPage(self.tabThree, "Combined Plot") 



class Notebook2(fnb.FlatNotebook):
	def __init__(self, parent):
		windowstyle = fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NO_X_BUTTON
		fnb.FlatNotebook.__init__(self, parent, wx.ID_ANY, agwStyle=windowstyle)	
		self.parent = parent
		#self.SetActiveTabTextColour('black')
		
		self.tabOne = tempSettingOne.TabPanel(self)
		self.tabTwo = tempSettingTwo.TabPanel(self)
		self.tabThree = GasQuenching.TabPanel(self)

		

		self.AddPage(self.tabOne, "Furnace One")
		self.AddPage(self.tabTwo, "Furnace Two")
		self.AddPage(self.tabThree, "Gas Quenching")

		   
		
class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)



class RandomPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)



class MainFrame(wx.Frame):

	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title=title,
			size=wx.DisplaySize())
		self.mgr = wx.aui.AuiManager(self)
		self.InitUI()
		self.Centre()
		self.RunFlag = 0
		

	def CoolingProcess(self):
		self.ADT_Time,self.ADT_Data = fastRead(self.FC_SR, self.FC_ET)
		# when using mcp3008(10 bit adc)
		#self.ADT_Volt = [round((elem*3.3)/float(1023),4) for elem in self.ADT_Data]
		#self.ADT_Temp = [(elem-1.25)/0.005 for elem in self.ADT_Volt]

		# when using mcp3208(10 bit adc)
		self.ADT_Volt = [round((elem*3.3)/float(4095),4) for elem in self.ADT_Data]
		self.ADT_Temp = [(elem*1000/165.0-0.8)/(8.0/375.0) for elem in self.ADT_Volt]

		self.notebook.tabThree.axes.clear() 
		self.notebook.tabThree.plot_data = self.notebook.tabOne.axes.plot(
			self.ADT_Volt, 
			linewidth=1,
			color='purple',
			)[0]
		self.notebook.tabThree.plot_data.set_xdata(np.array(self.ADT_Time))
		self.notebook.tabThree.plot_data.set_ydata(np.array(self.ADT_Temp))

		self.notebook.tabThree.axes.set_xlabel('time (s)')
		self.notebook.tabThree.axes.set_ylabel('Sample temprature (C)', color='purple')
		self.adt_ymax = self.temps1[len(self.temps1) - 1]*1.15
		self.adt_ymin = 0
		self.adt_xmax = max(self.ADT_Time)*1.15
		self.adt_xmin = 0
		self.notebook.tabThree.axes.set_ybound(lower=self.adt_ymin, upper=self.adt_ymax)
		self.notebook.tabThree.axes.set_xbound(lower=self.adt_xmin, upper=self.adt_xmax)
		self.notebook.tabThree.axes.grid(True)
		self.notebook.tabThree.canvas.draw()


	def InitUI(self):
		self.flag = 0
		self.Furnace1_Temp = []
		self.Furnace2_Temp = []
		self.Run_Time = []
		imagesPath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
		# creating a toolbar 
		toolbar = self.CreateToolBar()
		tool1 = toolbar.AddLabelTool(wx.ID_ANY, 'New'
			, wx.Bitmap(os.path.join(imagesPath, 'images/new3.png')))
		tool2 = toolbar.AddLabelTool(wx.ID_ANY, 'Open'
			, wx.Bitmap(os.path.join(imagesPath, 'images/open3.png')))
		tool3 = toolbar.AddLabelTool(wx.ID_ANY, 'Save'
			, wx.Bitmap(os.path.join(imagesPath, 'images/save3.png')))
		tool4 = toolbar.AddLabelTool(wx.ID_ANY, 'Print'
			, wx.Bitmap(os.path.join(imagesPath, 'images/printer3.png')))
		tool5 = toolbar.AddLabelTool(wx.ID_ANY, 'Setting'
			, wx.Bitmap(os.path.join(imagesPath, 'images/setting.png')))
		tool6 = toolbar.AddLabelTool(wx.ID_ANY, 'Quit'
			, wx.Bitmap(os.path.join(imagesPath, 'images/exit3.png')))
		toolbar.SetToolBitmapSize((16,16))
		toolbar.Realize()
		
		# creating panes 
		self.panel1 =panel1= wx.lib.scrolledpanel.ScrolledPanel(parent=self, id=-1,
			size=(290, 100))
		#panel2 = wx.Panel(self, -1, size=(200, 205))
		self.panel2 =panel2= mygrid.MyGrid(self)
		panel3 = wx.Panel(self, -1, size=(600, 400))
		panel3.SetBackgroundColour('white')
		self.panel4 = panel4 = wx.Panel(self, -1, size=(200, 100))
		#panel5 = wx.Panel(self, -1, size=(200, 100))
#--------------------------------------------------------------------------------------------
#for panel1(leftpane) which is on the left
		panel1.SetupScrolling()
		self.leftpane= leftpane = panel1

		# creating a static box in leftpane
		leftsizer = wx.BoxSizer(wx.VERTICAL)

		sb1 = wx.StaticBox(leftpane,label='Basic Settings',style=wx.TE_CENTRE)
		self.sl = wx.lib.intctrl.IntCtrl(leftpane, 90, 0, size=(30, -1),style=wx.TE_RIGHT)
		self.setbutton1 = wx.Button(leftpane, label='SET', size=(40, 20))	
		boxsizer1 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
		boxsizer1.Add(wx.StaticText(leftpane, label="Sample Length:"), 
		    flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)		
		boxsizer1.Add(self.sl,flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		boxsizer1.Add(wx.StaticText(leftpane, label="mm"), 
		    flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
		boxsizer1.Add(self.setbutton1, flag=wx.LEFT|wx.ALIGN_RIGHT, border =95)	

		sb3 = wx.StaticBox(leftpane,label='Sample Transportation',style=wx.TE_CENTRE)
		self.sms = wx.lib.intctrl.IntCtrl(leftpane, 91, 120, size=(30, -1),style=wx.TE_RIGHT)
		self.setbutton2 = wx.Button(leftpane, label='SET', size=(40, 20))	
		boxsizer3 = wx.StaticBoxSizer(sb3, wx.HORIZONTAL)
		boxsizer3.Add(wx.StaticText(leftpane, label="Stepper Mottor Speed:"), 
		    flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)		
		boxsizer3.Add(self.sms,flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		boxsizer3.Add(wx.StaticText(leftpane, label="rpm"), 
		    flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
		boxsizer3.Add(self.setbutton2, flag=wx.LEFT|wx.ALIGN_RIGHT, border =60)

		# creating a separating line between two statcibox
		line1 = wx.StaticLine(leftpane)
		line2 = wx.StaticLine(leftpane)
		line3 = wx.StaticLine(leftpane)

		sb2 = wx.StaticBox(leftpane,label='Sample Stop Point (inch)',style=wx.TE_CENTRE)

		boxsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)

		slBoxsizer = wx.GridBagSizer(1, 4)

		# creating widgets in sb2
		self.preview1 = wx.Button(leftpane, label='Preview', size=(50, 20))
		self.preview2 = wx.Button(leftpane, label='Preview', size=(50, 20))
		self.preview3 = wx.Button(leftpane, label='Preview', size=(50, 20))
		self.preview4 = wx.Button(leftpane, label='Preview', size=(50, 20))

		self.sld1= sld1 = wx.Slider(leftpane, value=0, minValue=0, maxValue=350, 
            size=(-1, 130), style=wx.SL_VERTICAL|wx.SL_LEFT)
		self.ssp1 = wx.lib.intctrl.IntCtrl(leftpane, 100, 0, size=(30, -1), min=0, max=350,
			style=wx.TE_CENTRE)
		
		self.sld2 = sld2 = wx.Slider(leftpane, value=0, minValue=0, maxValue=410, 
            size=(-1, 130), style=wx.SL_VERTICAL|wx.SL_LEFT)
		self.ssp2 = wx.lib.intctrl.IntCtrl(leftpane, 101, 0, size=(30, -1), min=0, max=410,
			style=wx.TE_CENTRE)

		self.sld3 = sld3 = wx.Slider(leftpane, value=0, minValue=0, maxValue=330, 
            size=(-1, 130), style=wx.SL_VERTICAL|wx.SL_LEFT)
		self.ssp3 = wx.lib.intctrl.IntCtrl(leftpane, 102, 0, size=(30, -1), min=0, max=330,
			style=wx.TE_CENTRE)
		
		self.sld4 = sld4 = wx.Slider(leftpane, value=0, minValue=0, maxValue=750, 
            size=(-1, 130), style=wx.SL_VERTICAL|wx.SL_LEFT)
		self.ssp4 = wx.lib.intctrl.IntCtrl(leftpane, 103, 0, size=(30, -1), min=0, max=750,
			style=wx.TE_CENTRE)
		
		# using gridbadsizer to arrange the sliders inside staticbox2(sb2)
		# notebook2 for temperature setting
		self.notebook2 = Notebook2(panel1)
		tempsettingSizer = wx.BoxSizer(wx.VERTICAL)
		tempsettingSizer.Add(self.notebook2, 1, flag = wx.ALL|wx.EXPAND)

		#-------------------------------------------------------------------------------------
		# Set the sizers		
		slBoxsizer.Add(sld1, pos=(1, 1), flag=wx.LEFT, border=14)
		slBoxsizer.Add(wx.StaticText(leftpane, label="SSP 1:"), pos=(2, 1),flag=wx.LEFT, border=7)
		slBoxsizer.Add(self.ssp1, pos=(3, 1), flag=wx.EXPAND)
		slBoxsizer.Add(self.preview1, pos=(4, 1), flag=wx.EXPAND)

		slBoxsizer.Add(sld2, pos=(1, 3), flag=wx.EXPAND)
		slBoxsizer.Add(wx.StaticText(leftpane, label="SSP 2:"), pos=(2, 3),flag=wx.LEFT, border=7)
		slBoxsizer.Add(self.ssp2, pos=(3, 3), flag=wx.EXPAND)
		slBoxsizer.Add(self.preview2, pos=(4, 3), flag=wx.EXPAND)

		slBoxsizer.Add(sld3, pos=(1, 5), flag=wx.EXPAND)
		slBoxsizer.Add(wx.StaticText(leftpane, label="SSP 3:"), pos=(2, 5),flag=wx.LEFT, border=7)
		slBoxsizer.Add(self.ssp3, pos=(3, 5), flag=wx.EXPAND)
		slBoxsizer.Add(self.preview3, pos=(4, 5), flag=wx.EXPAND)
		
		slBoxsizer.Add(sld4, pos=(1, 7), flag=wx.EXPAND)
		slBoxsizer.Add(wx.StaticText(leftpane, label="SSP 4:"), pos=(2, 7),flag=wx.LEFT, border=7)
		slBoxsizer.Add(self.ssp4, pos=(3, 7), flag=wx.EXPAND)
		slBoxsizer.Add(self.preview4, pos=(4, 7), flag=wx.EXPAND)

		boxsizer2.Add(slBoxsizer)
	
		leftsizer.Add(boxsizer1, 0, wx.EXPAND)
		leftsizer.Add(line1, 0, flag=wx.EXPAND|wx.BOTTOM|wx.TOP, border=5)
		leftsizer.Add(boxsizer3, 0, wx.EXPAND)
		leftsizer.Add(line2, 0, flag=wx.EXPAND|wx.BOTTOM|wx.TOP, border=5)
		leftsizer.Add(boxsizer2, 0, wx.EXPAND)
		leftsizer.Add(line3, 0, flag=wx.EXPAND|wx.BOTTOM|wx.TOP, border=5)

		leftsizer.Add(tempsettingSizer, 0, wx.EXPAND)

		leftpane.SetSizer(leftsizer)
#---------------------------------------------------------------------------------------------
#for panel3(middlepane) which is on the centre
		self.notebook = Notebook(panel3)
		panel3sizer = wx.BoxSizer(wx.VERTICAL)

		#-------------------------------------------------------------------------------------
		# Set the sizers
		panel3sizer.Add(self.notebook, 1, flag = wx.ALL|wx.EXPAND)
		panel3.SetSizer(panel3sizer)
#---------------------------------------------------------------------------------------------
# panel4(Right Pane)
		panel4Sizer = wx.BoxSizer(wx.VERTICAL)
		StartBox = wx.StaticBox(panel4,label='Furnace Status',style=wx.TE_CENTRE)
		panel4Box1 = wx.StaticBoxSizer(StartBox, wx.VERTICAL)
		#self.MainRun = wx.Button(panel4, label = 'Run',size=(190, 30))
		self.GetTemp = wx.Button(panel4, label = 'Current Temperature',size=(190, 30))
		self.GetCSP = wx.Button(panel4, label = 'Current Setpoint',size=(190, 30))
		self.GetUPR = wx.Button(panel4, label="Current UpRamp", size = (190, 30))
		self.GetDNR = wx.Button(panel4, label="Current DnRamp", size=(190, 30))
		#self.GetPID_P = wx.Button(panel4, label="P of PID", size=(190, 30))
		#self.GetPID_I = wx.Button(panel4, label="I of PID", size=(190, 30))
		#self.GetPID_D = wx.Button(panel4, label="D of PID", size=(190, 30))
		#panel4Box1.Add(self.MainRun, 0, wx.EXPAND, 0)
		panel4Box1.Add(self.GetTemp, 0, wx.EXPAND, 0)
		panel4Box1.Add(self.GetCSP, 0, wx.EXPAND, 0)
		panel4Box1.Add(self.GetUPR, 0, wx.EXPAND, 0)
		panel4Box1.Add(self.GetDNR, 0, wx.EXPAND, 0)
		#panel4Box1.Add(self.GetPID_P, 0, wx.EXPAND, 0)
		#panel4Box1.Add(self.GetPID_I, 0, wx.EXPAND, 0)
		#panel4Box1.Add(self.GetPID_D, 0, wx.EXPAND, 0)

		RunBox = wx.StaticBox(panel4,label='Start', style = wx.TE_CENTRE)
		panel4Box2 = wx.StaticBoxSizer(RunBox,wx.VERTICAL)
		self.MainRun = wx.Button(panel4, label = 'Run',size=(190, 30))
		panel4Box2.Add(self.MainRun, 0, wx.EXPAND, 0)

		#-------------------------------------------------------------------------------------
		# Set the sizers
		panel4Sizer.Add(panel4Box1, 0, wx.EXPAND)
		panel4Sizer.Add(panel4Box2, 0,flag = wx.TOP|wx.EXPAND, border=50)
		panel4.SetSizer(panel4Sizer)
#---------------------------------------------------------------------------------------------
		# using wx.aui to layout these created panes
		self.mgr.AddPane(panel2, wx.aui.AuiPaneInfo().Bottom().CloseButton(False)
			.CaptionVisible(False))
		self.mgr.AddPane(panel1, wx.aui.AuiPaneInfo().Left().Layer(1).CloseButton(False)
			.CaptionVisible(False))
		self.mgr.AddPane(panel3, wx.aui.AuiPaneInfo().Center().Layer(2).CloseButton(False)
			.CaptionVisible(False))
		self.mgr.AddPane(panel4, wx.aui.AuiPaneInfo().Right().Layer(1).CloseButton(False)
			.CaptionVisible(False))
		#self.mgr.AddPane(panel5, wx.aui.AuiPaneInfo().Top().CloseButton(False)
		#	.CaptionVisible(False))
		self.mgr.Update()
		self.Show()
#---------------------------------------------------------------------------------------------
		#Do all the bindings below

		# Bind MainRun
		self.redraw_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
		self.Bind(wx.EVT_BUTTON, self.onMonitor, self.MainRun)
		# Get temperature
		self.Bind(wx.EVT_BUTTON, self.onGetTemp, self.GetTemp)
		# Get Current Setpoint
		self.Bind(wx.EVT_BUTTON, self.onGetCSP, self.GetCSP)
		# Get UPR
		self.Bind(wx.EVT_BUTTON, self.onGetUPR, self.GetUPR)
		# Get DNR
		self.Bind(wx.EVT_BUTTON, self.onGetDNR, self.GetDNR)
		# Bind timer 
		#self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
		# BIND SLIDER_EVENT
		self.Bind(wx.EVT_SLIDER, self.Updatesliders)
		# bind toolbar event
		self.Bind(wx.EVT_TOOL, self.OnQuit, tool6)
		self.Bind(wx.EVT_TOOL, self.OnSetting, tool5)
		# call popupmenu when right mouse button clicked
		self.panel1.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.leftpane.Bind(wx.EVT_TEXT, self.UpdateText)
		self.leftpane.Bind(wx.EVT_BUTTON, self.setSampleLength, self.setbutton1)
		# Bind preview buttons
		self.panel1.Bind(wx.EVT_BUTTON, self.onPreview1, self.preview1)
		self.panel1.Bind(wx.EVT_BUTTON, self.onPreview2, self.preview2)
		self.panel1.Bind(wx.EVT_BUTTON, self.onPreview3, self.preview3)
		self.panel1.Bind(wx.EVT_BUTTON, self.onPreview4, self.preview4)
		# bind update button to onUpdate functions 
		self.notebook2.tabOne.Bind(wx.EVT_BUTTON, self.onUpdate1, self.notebook2.tabOne.updateButton)
		self.notebook2.tabTwo.Bind(wx.EVT_BUTTON, self.onUpdate2, self.notebook2.tabTwo.updateButton)
		self.notebook2.tabThree.Bind(wx.EVT_BUTTON, self.onUpdate3, self.notebook2.tabThree.upDate)

	def onGetUPR(self,event):
		hex_temp = getUPR("01", ser)[7:11]
		temp = int(hex_temp,16)
		print "current Up Ramp:" 
		print temp, "C/min"

	def onGetDNR(self, event):
		hex_temp = getDNR("01", ser)[7:11]
		temp = int(hex_temp,16)
		print "current Down Ramp:" 
		print temp, "C/min"


	def onGetCSP(self, event):
		hex_temp = getCSP("01", ser)[7:11]
		temp = int(hex_temp,16)
		print "current setpoint temp:" 
		print temp

	def onGetTemp(self, event):
		"""
		# this function is reading the temperature from the furnace built-in controller
		hex_temp = getPV("01", ser)[7:11]
		temp = int(hex_temp,16)
		print "current temp:" 
		print temp
		"""
		# read the tempertaure from the IR SENSOR,
		# the data is read out from the ADC MCP3008, which converts the anolog signals to digital
		temp = read3008(0)
		print "current temp:"
		print temp


	def on_redraw_timer(self, event):
		temp = read3008(0)
		print "temp:"
		print temp
		print "Current set-temp:"
		print self.C_temps1[self.index]
		#print temp
		self.Furnace1_Temp[1] = temp 
		if self.Furnace1_Temp[1]:
			self.Furnace1_Temp[0] = self.Furnace1_Temp[1]
		self.Furnace1_Temp[1] = temp 
		self.j1 =round((time.time() - self.Start_Time),2)

		self.notebook.tabOne.ax2.plot([(self.j1-1), (self.j1)],self.Furnace1_Temp,color="green")
		#self.notebook.tabOne.ax2([self.xmin,self.xmax,self.ymin,self.ymax])
		self.notebook.tabOne.ax2.set_ybound(lower=self.ymin, upper=self.ymax)
		self.notebook.tabOne.ax2.set_xbound(lower=self.xmin, upper=self.xmax)
		self.notebook.tabOne.canvas.draw()
		self.panel2.grid.AppendRows(numRows=1, updateLabels=True)

		self.panel2.grid.SetCellValue(self.GridIndex, 0, "%r"%(self.j1))
		self.panel2.grid.SetCellValue(self.GridIndex, 1, "%r"%(temp))
		self.panel2.grid.SetCellValue(self.GridIndex, 2, "%r"%(self.C_temps1[self.index]))

		self.panel2.grid.SetCellAlignment(self.GridIndex,0,wx.ALIGN_CENTER,wx.ALIGN_CENTER) 
		self.panel2.grid.SetCellAlignment(self.GridIndex,1,wx.ALIGN_CENTER,wx.ALIGN_CENTER) 
		self.panel2.grid.SetCellAlignment(self.GridIndex,2,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
		"""
		msg = self.panel2.grid.GridTableMessage(self,
			self.panel2.GRIDTABLE_NOTIFY_ROWS_APPENDED,
			1)
		self.panel2.GetView().ProgressTableMessage(msg)
		"""
		self.GridIndex+=1
		#self.notebook.tabOne.canvas.draw()


		if temp == self.C_temps1[self.index] and self.C_temps1[self.index]!=self.C_temps1[self.index+1]:
			if self.C_temps1[self.index+1]:
				self.index += 1
				if self.index<len(self.C_temps1) and self.C_temps1[self.index]>self.C_temps1[self.index-1]:
					UD = 1
					ramp = int((self.C_temps1[self.index] - temp) / (self.C_interval1[self.index]/60))
					setRamp(01,ramp,UD,ser)
					time.sleep(1)
					setTemp(01, self.C_temps1[self.index], ser)
				elif self.index<len(self.C_temps1) and self.C_temps1[self.index]<self.C_temps1[self.index-1]:
					UD = -1
					ramp = int((temp - self.C_temps1[self.index]) / (self.C_interval1[self.index]/60))
					setRamp(01,ramp,UD,ser)
					time.sleep(1)
					setTemp(01, self.C_temps1[self.index], ser)
			elif self.C_temps1[self.index+1] == None:
				self.redraw_timer.Stop()
				print "Progress 1 Finished"
				self.CoolingProcess()
				#RunStepper(self.position3, self.speed, 3)


		elif temp == self.C_temps1[self.index] and self.C_temps1[self.index]==self.C_temps1[self.index+1]:
			if (time.time()-self.Start_Time) < self.drawingInterval[self.index+2] and self.flag == 0:
				self.flag = 1
				setRamp(01,0,1,ser)
				setRamp(01,0,-1,ser)
				setTemp(01, self.C_temps1[self.index], ser)
			elif (time.time()-self.Start_Time) > self.drawingInterval[self.index+2]:
				print (time.time()-self.Start_Time) - self.drawingInterval[self.index+2]
				self.flag = 0
				self.index += 2
				if self.index<len(self.C_temps1) and self.C_temps1[self.index]>self.C_temps1[self.index-1]\
					and (temp - self.C_temps1[self.index])!=0:
					UD = 1
					ramp = int((self.C_temps1[self.index] - temp) / (self.C_interval1[self.index]/60))
					setRamp(01,ramp,UD,ser)
					time.sleep(1)
					setTemp(01, self.C_temps1[self.index], ser)
				elif self.index<len(self.C_temps1) and self.C_temps1[self.index]<self.C_temps1[self.index-1]\
					and (temp - self.C_temps1[self.index])!=0:
					UD = -1
					ramp = int((temp - self.C_temps1[self.index]) / (self.C_interval1[self.index]/60))
					setRamp(01,ramp,UD,ser)
					time.sleep(1)
					setTemp(01, self.C_temps1[self.index], ser)
				elif (temp - self.C_temps1[self.index])==0:
					setRamp(01,ramp,1,ser)
					time.sleep(1)
					setTemp(01, temp, ser)
					self.redraw_timer.Stop()
					print "Progress 1 Finished"
					self.CoolingProcess()
					#RunStepper(self.position3, self.speed, 3)


		
		if self.index == (len(self.C_temps1)-1) and temp == self.C_temps1[self.index]:
			self.redraw_timer.Stop()
			print "Progress 1 Finished"
			self.CoolingProcess()
			#RunStepper(self.position3, self.speed, 3)
		


	
	def onMonitor(self, event):
		"""
		if self.RunFlag== 0:
			self.RunFlag = 1
			RunStepper(self.position2, self.speed, 2)
		"""

		self.Start_Time = time.time()
		self.index = 0
		self.GridIndex = 0
		#hex_temp = getPV("01", ser)[7:11]
		#temp = int(hex_temp,16)
		temp = read3008(0)
		print "temp:" 
		print temp
		
		if temp < self.C_temps1[self.index]:
			UD = 1
			ramp = round((self.C_temps1[self.index] - temp) / (self.C_interval1[self.index]/60.0))
			#print (self.C_interval1[self.index]/60)
			ramp = int(ramp)
			print UD,ramp
			setRamp(01,ramp,UD,ser)
			time.sleep(1)
			setTemp(01, self.C_temps1[self.index], ser) 
			print "sent"
			
		elif temp > self.C_temps1[self.index]:
			UD = -1
			ramp = round((temp - self.C_temps1[self.index]) / (self.C_interval1[self.index]/60.0))
			ramp = int(ramp)
			print UD,ramp
			setRamp(01,ramp,UD,ser)
			time.sleep(1)
			setTemp(01, self.C_temps1[self.index], ser)
			print "sent"

		time.sleep(1)

		self.redraw_timer.Start(1000)
		#print getPV(01, ser)[7:11]
		#temp = int(hex_temp,16)
		#print self.Start_Time

		#print self.Start_Time
		
		

		#print "start..."


	def onUpdate1(self, event):
		self.temps1 = self.notebook2.tabOne.setpoint
		self.Furnace1_Temp = [self.temps1[0]]
		self.Furnace1_Temp.append(None)
		self.interval1 = self.notebook2.tabOne.setTime
		# C_temps1 and C_interval1 stands for communicational temps and intervals
		self.C_temps1 = self.temps1[1:]
		self.C_interval1 = self.interval1[1:]
		self.temps1 = [x for x in self.temps1 if x is not None]
		self.interval1 = [x for x in self.interval1 if x is not None]

		print len(self.temps1)
		self.notebook.tabOne.axes.clear() 
		self.notebook.tabOne.plot_data = self.notebook.tabOne.axes.plot(
			self.temps1, 
			linewidth=1,
			color='blue',
			)[0]
		self.drawingInterval = newlist(self.interval1)
		self.notebook.tabOne.plot_data.set_xdata(np.array(self.drawingInterval))
		self.notebook.tabOne.plot_data.set_ydata(np.array(self.temps1))

		self.notebook.tabOne.axes.set_xlabel('time (s)')
		self.notebook.tabOne.axes.set_ylabel('Preset temprature (C)', color='b')
		self.ymax = max(self.temps1) + max(self.temps1)*0.15
		self.ymin = 0
		self.xmax = max(self.drawingInterval)
		self.xmin = 0
		self.notebook.tabOne.axes.set_ybound(lower=self.ymin, upper=self.ymax)
		self.notebook.tabOne.axes.set_xbound(lower=self.xmin, upper=self.xmax)
		self.notebook.tabOne.axes.grid(True)
		self.notebook.tabOne.canvas.draw()
		#print setTemp(01, self.temps1)
		#print setInterval(01, self.interval1)

	def onUpdate2(self, event):
		self.temps2 = self.notebook2.tabTwo.setpoint
		self.notebook.tabTwo.axes.clear() 
		self.notebook.tabTwo.plot_data = self.notebook.tabTwo.axes.plot(
			self.temps2, 
			linewidth=1,
			color='blue',
			)[0]
		self.notebook.tabTwo.plot_data.set_xdata(np.arange(len(self.temps2)))
		self.notebook.tabTwo.plot_data.set_ydata(np.array(self.temps2))

		self.notebook.tabTwo.axes.set_xlabel('time (s)')
		self.notebook.tabTwo.axes.set_ylabel('Preset temprature (C)', color='b')
		ymax = max(self.temps2) + max(self.temps2)*0.15
		ymin = 0
		self.notebook.tabTwo.axes.set_ybound(lower=ymin, upper=ymax)
		self.notebook.tabTwo.axes.grid(True)
		self.notebook.tabTwo.canvas.draw()
		print self.temps2

	def onUpdate3(self, event):
		self.notebook2.tabThree.ST_Input.SetLabel(str(self.temps1[len(self.temps1) - 1]))
		self.FC_ET = self.notebook2.tabThree.ET.GetValue()
		self.FC_SR = self.notebook2.tabThree.SR.GetValue()

	def onFocus(self, event):
		self.panel1.SetFocus()

	def onPreview1(self, event):
		self.position1 = self.sld1.GetValue()
		self.speed = self.sms.GetValue()
		# convert distance unit mm to stepper motor's microsteps
		# 1 stepper motor step equals 1.8 degree,
		# 16 micro-steps equals 1 step
		RunStepper(self.position1, self.speed, self.sl.GetValue(),1)
		"""
		time.sleep(15)
		Distance = '1000' + 'Dis'
		cmd = Distance + Speed + direct
		communication_send(addr, "stm", cmd)
		"""

	def onPreview2(self, event):
		self.position2 = self.sld2.GetValue()
		self.speed = self.sms.GetValue()
		# convert distance unit mm to stepper motor's microsteps
		# 1 stepper motor step equals 1.8 degree,
		# 16 micro-steps equals 1 step
		RunStepper(self.position2, self.speed, self.sl.GetValue(),2)
		"""
		time.sleep(15)
		Distance = '1000' + 'Dis'
		cmd = Distance + Speed + direct
		communication_send(addr, "stm", cmd)
		"""

	def onPreview3(self, event):
		self.position3 = self.sld3.GetValue()
		self.speed = self.sms.GetValue()
		# convert distance unit mm to stepper motor's microsteps
		# 1 stepper motor step equals 1.8 degree,
		# 16 micro-steps equals 1 step
		RunStepper(self.position3, self.speed, self.sl.GetValue(), 3)
		"""
		time.sleep(15)
		Distance = '1000' + 'Dis'
		cmd = Distance + Speed + direct
		communication_send(addr, "stm", cmd)
		"""


	def onPreview4(self, event):
		self.position4 = self.sld4.GetValue()
		self.speed = self.sms.GetValue()
		# convert distance unit mm to stepper motor's microsteps
		# 1 stepper motor step equals 1.8 degree,
		# 16 micro-steps equals 1 step
		RunStepper(self.position4, self.speed, self.sl.GetValue(), 4)
		"""
		time.sleep(15)
		Distance = '1000' + 'Dis'
		cmd = Distance + Speed + direct
		communication_send(addr, "stm", cmd)
		"""

	def setSampleLength(self, event):
		self.SampleLength = self.sl.GetValue()
		self.sld1.SetMax(354 - self.SampleLength)
		self.sld2.SetMax(410 - self.SampleLength)
		self.sld3.SetMax(330 - self.SampleLength)
		self.sld4.SetMax(750 - self.SampleLength)

	def Updatesliders(self, e):
		self.setpoint1 = self.sld1.GetValue()
		self.ssp1.SetValue(self.setpoint1)
		self.setpoint2 = self.sld2.GetValue()
		self.ssp2.SetValue(self.setpoint2)
		self.setpoint3 = self.sld3.GetValue()
		self.ssp3.SetValue(self.setpoint3)
		self.setpoint4 = self.sld4.GetValue()
		self.ssp4.SetValue(self.setpoint4)

	def UpdateText(self, event):
		#make sure the right text boxes are selected
		if (event.GetId()<=103 and event.GetId()>=100):
			self.setpoint1 = self.ssp1.GetValue()
			self.sld1.SetValue(self.setpoint1)
			self.setpoint2 = self.ssp2.GetValue()
			self.sld2.SetValue(self.setpoint2)
			self.setpoint3 = self.ssp3.GetValue()
			self.sld3.SetValue(self.setpoint3)
			self.setpoint4 = self.ssp4.GetValue()
			self.sld4.SetValue(self.setpoint4)

	def OnQuit(self, e):
		self.Close()

	def OnSetting(self, e):
		Setting = STM_T()
		Setting.Show()

	def OnRightDown(self, e):
		self.PopupMenu(MyPopupMenu(self.panel1), e.GetPosition())



class MyPopupMenu(wx.Menu): # popup menu for Example frame
    
    def __init__(self, parent):
        super(MyPopupMenu, self).__init__()
        
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize') # minimize frame
        self.AppendItem(mmi) # append mmi to popupmenu
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi) # bind OnMinimize function to mmi

        cmi = wx.MenuItem(self, wx.NewId(), 'Close') # close frame
        self.AppendItem(cmi) # append cmi to popupmenu
        self.Bind(wx.EVT_MENU, self.OnClose, cmi) # bind OnClose Function to cmi

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()




def main():
	ex = wx.App()
	MainFrame(None, "CAL Simulator")
	ex.MainLoop()

if __name__=='__main__':
	main()

