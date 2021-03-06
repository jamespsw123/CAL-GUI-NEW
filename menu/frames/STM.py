import wx
import os
import time
import math
from RPI_I2C_ARDUINO import *
addr = 0x04
MotorSpeed = 60

def Stepper(position, speed,SampleLength,position_num):
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
	distance_ = int(float(x - position - SampleLength)*(3200/(math.pi*70)))
	distance_ = str(distance_)
	Distance = distance_ + 'Dis'  
	# convert speed unit rpm to stepper motor's microsteps/sec
	speed_ = int(float(speed)*(3200/60))
	speed_ = str(speed_)
	Speed = speed_ + 'Spd' 
	position = str(position_num) + 'P'
	direct = '1' + 'E'# 'E' stands for end.
	cmd = Distance + Speed + position + direct
	communication_send(addr, "stm", cmd)

class STM_T(wx.Frame): # STM_T is a frame for stepper motor testing

	def __init__(self):
		wx.Frame.__init__(self,None, title= 'Stepper Motor Test',
			size=(450, 355), style= wx.STAY_ON_TOP)
		self.Centre()
		self.statusbar = self.CreateStatusBar()
		self.panel2 = panel2 = wx.Panel(self)

		sizer = wx.GridBagSizer(5,4)

		text1 = wx.StaticText(panel2, label='Stepper Motor Testing')

		sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM,
			border=15)

		# use os.path find the path of images directry
		imagesPath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

		icon = wx.StaticBitmap(panel2, 
			bitmap=wx.Bitmap(os.path.join(imagesPath, 'images/stm2.png')))
		sizer.Add(icon, pos=(0, 3), flag=wx.TOP|wx.RIGHT,
			border=7)
		line = wx.StaticLine(panel2)
		sizer.Add(line, pos=(1, 0), span=(1, 5),
			flag=wx.EXPAND|wx.BOTTOM, border=10)

		text2 = wx.StaticText(panel2, label='Distance')
		sizer.Add(text2, pos=(2, 0), flag=wx.LEFT, border=10)

		unit1 = wx.StaticText(panel2, label='mm')
		sizer.Add(unit1, pos=(2, 3), flag=wx.LEFT, border=7)

		unit2 = wx.StaticText(panel2, label='rpm')
		sizer.Add(unit2, pos=(3, 3), flag=wx.LEFT|wx.TOP, border=7)
		distance=''
		speed=''
		self.tc1= tc1 = wx.TextCtrl(panel2,value=distance)
		sizer.Add(tc1, pos=(2, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND)

		text3 = wx.StaticText(panel2, label='Speed')
		sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

		self.tc2 = tc2 = wx.TextCtrl(panel2, value=speed)
		sizer.Add(tc2, pos=(3, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND,
			border=5)

		#button1 = wx.Button(panel2, label='Browse...')
		#sizer.Add(button1, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

		text4 = wx.StaticText(panel2, label='Direction')
		sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

		self.combo3 = combo3 = wx.ComboBox(panel2, style=wx.CB_DROPDOWN|wx.CB_READONLY,
			choices=['Clockwise','Counter Clockwise' ])
		combo3.SetSelection(0)
		sizer.Add(combo3, pos=(4, 1), span=(1, 3), 
			flag=wx.TOP|wx.EXPAND, border=5)

		#button2 = wx.Button(panel2, label='Browse...')
		#sizer.Add(button2, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)

		sb = wx.StaticBox(panel2, label='Optional Attributes')

		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		boxsizer.Add(wx.CheckBox(panel2, label='Decay Mode'),
			flag=wx.LEFT|wx.TOP, border=5)
		boxsizer.Add(wx.CheckBox(panel2, label='With Ramp Acceleration'),
			flag=wx.LEFT,border=5)
		boxsizer.Add(wx.CheckBox(panel2, label='One Direction Only'),
			flag=wx.LEFT|wx.BOTTOM, border=5)

		sizer.Add(boxsizer, pos=(5, 0), span=(1, 5),
			flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

		#button3 = wx.Button(panel2, label='Help')
		#sizer.Add(button3, pos=(7, 0), flag=wx.LEFT, border=10)
		button1 = wx.Button(panel2, label='Position Demonstration')
		sizer.Add(button1, pos=(7, 3), span=(1, 1), 
			flag=wx.LEFT, border=10)
		panel2.Bind(wx.EVT_BUTTON, self.OnPD, button1)

		button4 = wx.Button(panel2, label='RUN')
		sizer.Add(button4, pos=(8, 2), flag=wx.LEFT, border=10)
		panel2.Bind(wx.EVT_BUTTON, self.OnRun, button4)

		button5 = wx.Button(panel2, label='QUIT')
		sizer.Add(button5, pos=(8, 3), span=(1, 1), 
			flag=wx.BOTTOM|wx.RIGHT, border=5)
		panel2.Bind(wx.EVT_BUTTON, self.OnStop, button5)

		button6 = wx.BitmapButton(panel2, 
			bitmap=wx.Bitmap(os.path.join(imagesPath, 'images/back.png')))
		sizer.Add(button6, pos=(8, 0), span=(1, 1), 
			flag=wx.LEFT, border=10)
		panel2.Bind(wx.EVT_BUTTON, self.OnQuit, button6)

		sizer.AddGrowableCol(2)

		panel2.SetSizer(sizer)

		#self.Bind(wx.EVT_RIGHT_DONW, Onrightdown())
		self.popupmenu = wx.Menu()
		menulist = ['Save', 'Quit']
		for text in menulist:
			item = self.popupmenu.Append(-1, text)
			self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
		panel2.Bind(wx.EVT_CONTEXT_MENU, self.showPopupMenu)

	# on position demonstration
	def OnPD(self, event):
		#Stepper(position, speed, SampleLength, position_num)
		Stepper(450, MotorSpeed, 150, 4)
		self.statusbar.SetStatusText("going to loading position")
		time.sleep(10)
		Stepper(100, MotorSpeed, 150, 1)
		self.statusbar.SetStatusText("going to waiting position")
		time.sleep(25)
		Stepper(130, MotorSpeed, 150, 2)
		self.statusbar.SetStatusText("going into first furnace")
		time.sleep(15)
		Stepper(50, MotorSpeed, 150, 3)
		self.statusbar.SetStatusText("going into cooling position")
		time.sleep(15)
		Stepper(130, MotorSpeed, 150, 4)
		self.statusbar.SetStatusText("going into 2nd furnace to reheat")
		time.sleep(15)
		Stepper(450, MotorSpeed, 150, 4)
		self.statusbar.SetStatusText("back to loading position")





	def OnPopupItemSelected(self, event):
		item = self.popupmenu.FindItemById(event.GetId())
		text = item.GetText()
		wx.MessageBox("You selected item '%s'" % text)

	def OnShowPopup(self, event):
		pos = event.GetPosition()
		pos = self.panel2.ScreenToClient(pos)
		self.panel2.PopupMenu(self.popupmenu, pos)		

	def OnQuit(self, event):
		self.Close()

	def OnRun(self, event):
		distance_ = int(float(self.tc1.GetValue())*(3200/(math.pi*70)))
		distance_ = str(distance_)
		Distance = distance_ + 'Dis'  
		speed_ = int(float(self.tc2.GetValue())*(3200/60))
		speed_ = str(speed_)
		Speed = speed_ + 'Spd' 
		Direction = self.combo3.GetValue()
		direct = ''
		if Direction == 'Clockwise':
			direct = '0' + 'E'  # 'E' stands for end.
		elif Direction == 'Counter Clockwise':
			direct = '1' + 'E'
		#Direction = ord(Direction[0].upper())
		cmd = Distance + Speed + direct
		communication_send(addr, "stm", cmd)
		received = getStatus(addr)
		print received




	def OnStop(self, event):
		self.Close()

	def showPopupMenu(self, event):
		"""
		Create and display a popup menu on right-click event
		"""
		if not hasattr(self, "popupID1"):
			self.popupID1 = wx.NewId()
			self.popupID2 = wx.NewId()
			#self.popupID3 = wx.NewId()
		menu = wx.Menu()
		sitem = wx.MenuItem(menu, self.popupID1,"Save")

		menu.AppendItem(sitem)
		qitem = menu.Append(self.popupID2, "Back")
		self.Bind(wx.EVT_MENU, self.OnQuit, qitem)

		#item3 = menu.Append(self.popupID3, "3")

		self.PopupMenu(menu)
		menu.Destroy()
