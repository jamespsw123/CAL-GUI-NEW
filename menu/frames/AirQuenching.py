import wx
import wx.lib.intctrl
class TabPanel(wx.Panel):
	def __init__(self, parent):

		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

		self.MainSizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
		self.ST = '0'
		self.Start_Temp = wx.StaticText(self, label = "Start Temperature :") 
		self.ST_Input = wx.StaticText(self, label = self.ST)
		self.Start_Temp_Unit = wx.StaticText(self, label = "  C") 


		self.End_Temp = wx.StaticText(self, label = "End Temperature: ")
		self.ET = wx.lib.intctrl.IntCtrl(self, 131, 20, size=(30, -1),style=wx.TE_RIGHT)
		self.End_Temp_Unit = wx.StaticText(self, label = "C")

		self.Sampling_Rate = wx.StaticText(self, label = "Temperature Sampling rate: ") 
		self.CR = wx.lib.intctrl.IntCtrl(self, 132, 0, size=(30, -1),style=wx.TE_RIGHT)
		self.CR_Unit = wx.StaticText(self, label = "HZ")

		self.upDate = wx.Button(self, label="Update", size=(-1, 20))


		self.sizer1.Add(self.Start_Temp, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer1.Add(self.ST_Input, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer1.Add(self.Start_Temp_Unit, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer2.Add(self.End_Temp, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer2.Add(self.ET)
		self.sizer2.Add(self.End_Temp_Unit, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer3.Add(self.Sampling_Rate, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer3.Add(self.CR, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=3)
		self.sizer3.Add(self.CR_Unit, flag=wx.LEFT|wx.TOP, border=7)
		self.sizer4.Add(self.upDate, flag = wx.LEFT, border= 90)

		self.MainSizer.Add(self.sizer1)
		self.MainSizer.Add(self.sizer2)
		self.MainSizer.Add(self.sizer3)
		self.MainSizer.Add(self.sizer4)
		self.SetSizer(self.MainSizer)

class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Air Quenching")
        panel = TabPanel(self)
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
