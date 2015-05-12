import wx
import wx.lib.intctrl
import wx.lib.masked as masked
class TabPanel(wx.Panel):
	def __init__(self, parent):

		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		self.number_of_buttons = 0
		self.spt = []
		self.setpoint = [None]*15
		
		self.frame = parent
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		controlSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
		instructionSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.addButton = wx.Button(self, label="Add", size=(-1, 20))
		self.addButton.Bind(wx.EVT_BUTTON, self.onAddWidget)
		controlSizer.Add(self.addButton, 0, wx.CENTER|wx.TOP|wx.RIGHT, 5)

		self.removeButton = wx.Button(self, label="Remove", size=(-1, 20))
		self.removeButton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
		controlSizer.Add(self.removeButton, 0, wx.CENTER|wx.TOP|wx.RIGHT|wx.LEFT, 5)

		self.updateButton = wx.Button(self, label="Update", size=(-1, 20))
		#self.updateButton.Bind(wx.EVT_BUTTON, self.onUpdate)
		controlSizer.Add(self.updateButton, 0, wx.CENTER|wx.TOP|wx.LEFT, 5)

		self.new_setpoint = wx.StaticText(self, label='Presets', size=(70, 20))
		instructionSizer.Add(self.new_setpoint, 0, wx.CENTER|wx.LEFT, 30)

		self.new_setpoint_temp = wx.StaticText(self, label='Temperature', size=(70, 20))
		instructionSizer.Add(self.new_setpoint_temp, 0, wx.CENTER|wx.LEFT, 10)

		self.new_setpoint_interval = wx.StaticText(self, label='Interval \n (h/m/s)', size=(70, 20))
		instructionSizer.Add(self.new_setpoint_interval, 0, wx.CENTER|wx.LEFT, 35)

		self.Bind(wx.EVT_TEXT, self.UpdateText)


		self.mainSizer.Add(controlSizer, 0, wx.CENTER)
		self.mainSizer.Add(instructionSizer, 0, wx.CENTER)
		self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER)
		self.SetSizer(self.mainSizer)

	def UpdateText(self, event):
		#make sure the right text boxes are selected
		if (event.GetId()<=self.number_of_buttons and event.GetId()>=1):
			self.object = event.GetEventObject()

			self.setpoint[event.GetId()-1] = self.object.GetValue()

			

	def onAddWidget(self, event):
		self.number_of_buttons += 1
		label = "Set Point %s :" %  self.number_of_buttons
		name = "SP%s" %self.number_of_buttons
		ID = self.number_of_buttons
		self.new_SP = wx.StaticText(self,ID, label=label, name=name)
		self.new_Temp = wx.lib.intctrl.IntCtrl(self, ID, size=(30, -1),style=wx.TE_RIGHT, name=name)
		self.new_Temp_Unit = wx.StaticText(self,ID , label = "F", name=name)
		self.new_Interval = masked.TimeCtrl(self, ID + 100 , -1 , fmt24hr=True, name=name)
		self.SPsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.SPsizer.Add(self.new_SP, 0,  wx.CENTER|wx.RIGHT, 45)
		self.SPsizer.Add(self.new_Temp, 0,  wx.CENTER, 5)
		self.SPsizer.Add(self.new_Temp_Unit, 0, wx.RIGHT|wx.TOP|wx.LEFT, 3)
		self.SPsizer.Add(self.new_Interval, 0,  wx.CENTER|wx.LEFT, 35)
		self.widgetSizer.Add(self.SPsizer, 0, wx.TOP, 3)
		self.frame.Fit()

	def onRemoveWidget(self, event):
		""""""
		if self.widgetSizer.GetChildren():
			self.widgetSizer.Hide(self.number_of_buttons-1)
			self.widgetSizer.Remove(self.number_of_buttons-1)
			self.number_of_buttons -= 1
			self.setpoint[self.number_of_buttons] = None
			self.frame.Fit()



class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Add / Remove Buttons")
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = TabPanel(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()