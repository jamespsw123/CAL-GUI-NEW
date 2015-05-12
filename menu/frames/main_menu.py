import wx
import wx.aui
 
########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="SplitterWindow", size=(1000,720))
        self.mgr = wx.aui.AuiManager(self)
 
        self.panel1 =panel1= wx.Panel(self, -1, size=(200, 100))
        panel2 = wx.Panel(self, -1, size=(200, 100))
        panel3 = wx.Panel(self, -1, size=(200, 100))
        panel4 = wx.Panel(self, -1, size=(200, 100))
        panel5 = wx.Panel(self, -1, size=(200, 100))


        static = wx.StaticText(panel1, -1, 'Hello World', pos=(0, 0))

        self.mgr.AddPane(panel2, wx.aui.AuiPaneInfo().Bottom()
            .CloseButton(False).CaptionVisible(False))
        self.mgr.AddPane(panel1, wx.aui.AuiPaneInfo().Left().Layer(1).CloseButton(False))
        self.mgr.AddPane(panel3, wx.aui.AuiPaneInfo().Center().Layer(2).CloseButton(False))
        self.mgr.AddPane(panel4, wx.aui.AuiPaneInfo().Right().Layer(1).CloseButton(False))
        self.mgr.AddPane(panel5, wx.aui.AuiPaneInfo().Top().CloseButton(False))
        self.mgr.Update()
        self.Show()
 
        
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()