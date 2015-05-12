import wx
class Example(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Example', size=(312,170))
        self.panel=wx.Panel(self)
        ntext=wx.StaticText(self.panel, -1, "Name: ", pos=(3,6))
        self.name=wx.TextCtrl(self.panel, -1, "Your name", size=(220, -1), pos=(60,2))
        self.name.SetInsertionPoint(0)
        Namo=wx.Button(self.panel, -1, "Namo", pos=(150,50), size=(60,30))
        self.Bind(wx.EVT_BUTTON, self.GetName, Namo)
        Quit=wx.Button(self.panel, -1, "Quit", pos=(50,50), size=(60,30))
        self.panel.Bind(wx.EVT_BUTTON, self.closebutton, Quit)
    def GetName(self, panel):
        ntext=wx.StaticText(self.panel, -1, "New Text: ", pos=(3,85))
        self.panel.name=wx.TextCtrl(self.panel, -1, "Your Static Text", size=(220, -1), pos=(60,85))
        self.panel.name.SetInsertionPoint(0)
        print(self.name.GetValue())
    def closebutton(self, panel):
        self.Close(True)
        
if __name__ == '__main__':
    app=wx.PySimpleApp()
    frame=Example(parent=None,id=-1)
    frame.Show()
    app.MainLoop()