# wxpython menu&toolbar practice

import wx
import os
# creating a popup menu

class STM_T(wx.Frame): # STM_T is a frame for stepper motor testing

	def __init__(self):
		wx.Frame.__init__(self,None, title= 'Stepper Motor Test',
			size=(400, 305), style= wx.STAY_ON_TOP)
		self.Centre()

		self.panel2 = panel2 = wx.Panel(self)

		sizer = wx.GridBagSizer(5,4)

		text1 = wx.StaticText(panel2, label='Stepper Motor')

		sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM,
			border=15)

		icon = wx.StaticBitmap(panel2, bitmap=wx.Bitmap('images/stm2.png'))
		sizer.Add(icon, pos=(0, 3), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT,
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
		tc1 = wx.TextCtrl(panel2,value=distance)
		sizer.Add(tc1, pos=(2, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND)

		text3 = wx.StaticText(panel2, label='Speed')
		sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

		tc2 = wx.TextCtrl(panel2, value=speed)
		sizer.Add(tc2, pos=(3, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND,
			border=5)

		#button1 = wx.Button(panel2, label='Browse...')
		#sizer.Add(button1, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

		text4 = wx.StaticText(panel2, label='Direction')
		sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

		combo3 = wx.ComboBox(panel2, style=wx.CB_DROPDOWN|wx.CB_READONLY,
			choices=['Clockwise','Counter Clockwise' ])
		combo3.SetSelection(0)
		sizer.Add(combo3, pos=(4, 1), span=(1, 3), 
			flag=wx.TOP|wx.EXPAND, border=5)

		#button2 = wx.Button(panel2, label='Browse...')
		#sizer.Add(button2, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)

		sb = wx.StaticBox(panel2, label='Optional Attributes')

		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		boxsizer.Add(wx.CheckBox(panel2, label='Public'),
			flag=wx.LEFT|wx.TOP, border=5)
		boxsizer.Add(wx.CheckBox(panel2, label='Generate Default Constructor'),
			flag=wx.LEFT,border=5)
		boxsizer.Add(wx.CheckBox(panel2, label='Generate Main Method'),
			flag=wx.LEFT|wx.BOTTOM, border=5)

		sizer.Add(boxsizer, pos=(5, 0), span=(1, 5),
			flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

		#button3 = wx.Button(panel2, label='Help')
		#sizer.Add(button3, pos=(7, 0), flag=wx.LEFT, border=10)

		button4 = wx.Button(panel2, label='RUN')
		sizer.Add(button4, pos=(7, 2), flag=wx.LEFT, border=50)

		button5 = wx.Button(panel2, label='STOP')
		sizer.Add(button5, pos=(7, 3), span=(1, 1), 
			flag=wx.BOTTOM|wx.RIGHT, border=5)

		button6 = wx.BitmapButton(panel2, bitmap=wx.Bitmap('images/back.png'))
		sizer.Add(button6, pos=(7, 0), span=(1, 1), 
			flag=wx.LEFT, border=15)
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

class MainFrame(wx.Frame):

	def __init__(self, parent, title):
		super(MainFrame, self).__init__(parent, title=title,
			size=(600, 400))

		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):

		# creating a menubar 
		"""
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()
		fitem1 = fileMenu.Append(wx.ID_ANY, 'Print')
		fitem2 = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		"""
		# create a panel 
		self.panel = panel = wx.Panel(self)
		panel.SetBackgroundColour('#4f5049')
		#vbox = wx.BoxSizer(wx.VERTICAL)

		#midPan = wx.Panel(panel)
		#midPan.SetBackgroundColour('#ededed')

		#vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 20)
		#panel.SetSizer(vbox)

		# creating a toolbar 
		toolbar = self.CreateToolBar()
		tool1 = toolbar.AddLabelTool(wx.ID_ANY, 'New', wx.Bitmap('images/new3.png'))
		tool2 = toolbar.AddLabelTool(wx.ID_ANY, 'Open', wx.Bitmap('images/open3.png'))
		tool3 = toolbar.AddLabelTool(wx.ID_ANY, 'Save', wx.Bitmap('images/save3.png'))
		tool4 = toolbar.AddLabelTool(wx.ID_ANY, 'Print', wx.Bitmap('images/printer3.png'))
		tool5 = toolbar.AddLabelTool(wx.ID_ANY, 'Setting', wx.Bitmap('images/setting.png'))
		tool6 = toolbar.AddLabelTool(wx.ID_ANY, 'Quit', wx.Bitmap('images/exit3.png'))
		toolbar.Realize()


		"""
		menuBar.Append(fileMenu, '&File')
		self.SetMenuBar(menuBar)
		"""

		# bind toolbar event
		self.Bind(wx.EVT_TOOL, self.OnQuit, tool6)
		self.Bind(wx.EVT_TOOL, self.OnSetting, tool5)
		"""
		# bind menu event
		self.Bind(wx.EVT_MENU, self.OnQuit, fitem1)
		"""
		# call popupmenu when right mouse button clicked
		self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

	def OnQuit(self, e):
		self.Close()
	def OnSetting(self, e):
		Setting = STM_T()
		Setting.Show()

	def OnRightDown(self, e):
		self.PopupMenu(MyPopupMenu(self), e.GetPosition())


	



def main():

	ex = wx.App()
	MainFrame(None, "CAL Simulator")
	ex.MainLoop()

if __name__=='__main__':
	main()

