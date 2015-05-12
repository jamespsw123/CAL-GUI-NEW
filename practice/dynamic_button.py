import wx
import wx.lib.intctrl
########################################################################
class MyPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.number_of_buttons = 0
        self.frame = parent
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        
 
        self.addButton = wx.Button(self, label="Add")
        self.addButton.Bind(wx.EVT_BUTTON, self.onAddWidget)
        controlSizer.Add(self.addButton, 0, wx.CENTER|wx.ALL, 5)
 
        self.removeButton = wx.Button(self, label="Remove")
        self.removeButton.Bind(wx.EVT_BUTTON, self.onRemoveWidget)
        controlSizer.Add(self.removeButton, 0, wx.CENTER|wx.ALL, 5)
 
        self.mainSizer.Add(controlSizer, 0, wx.CENTER)
        self.mainSizer.Add(self.widgetSizer, 0, wx.CENTER|wx.ALL, 10)
 
        self.SetSizer(self.mainSizer)
 
    #----------------------------------------------------------------------
    def onAddWidget(self, event):
        """"""
        self.number_of_buttons += 1
        label = "Set Point %s :" %  self.number_of_buttons
        name = "SP%s" % self.number_of_buttons
        new_SP = wx.StaticText(self, label=label, name=name)
        new_Temp = wx.lib.intctrl.IntCtrl(self, 90, 0, size=(30, -1),style=wx.TE_RIGHT, name = name)
        new_Temp_Unit = wx.StaticText(self, label = "F", name = name)
        self.SPsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SPsizer.Add(new_SP, 0, wx.ALL, 5)
        self.SPsizer.Add(new_Temp, 0, wx.ALL, 5)
        self.SPsizer.Add(new_Temp_Unit, 0, wx.ALL, 5)
        self.widgetSizer.Add(self.SPsizer, 0, wx.ALL, 5)
        #self.frame.fSizer.Layout()
        self.frame.Fit()
 
    #----------------------------------------------------------------------
    def onRemoveWidget(self, event):
        """"""
        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(self.number_of_buttons-1)
            self.widgetSizer.Remove(self.number_of_buttons-1)
            self.number_of_buttons -= 1
            #self.frame.fSizer.Layout()
            self.frame.Fit()
 
########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Add / Remove Buttons")
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        panel = MyPanel(self)
        self.fSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.fSizer)
        self.Fit()
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()