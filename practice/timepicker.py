import wx
import wx.lib.masked as masked

########################################################################
class MyPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        text1 = wx.StaticText( self, -1, "12-hour format:", size=(150,-1))
        self.time12 = masked.TimeCtrl( self, -1, name="12 hour control" )
        h = self.time12.GetSize().height
        spin1 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL )
        self.time12.BindSpinButton( spin1 )
        self.addWidgets([text1, self.time12, spin1])

        text2 = wx.StaticText( self, -1, "24-hour format:")
        spin2 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL )
        self.time24 = masked.TimeCtrl(
                        self, -1, name="24 hour control", fmt24hr=True,
                        spinButton = spin2
                        )
        self.addWidgets([text2, self.time24, spin2])

        text3 = wx.StaticText( self, -1, "No seconds\nor spin button:")
        self.spinless_ctrl = masked.TimeCtrl(
                                self, -1, name="spinless control",
                                display_seconds = False
                                )
        self.addWidgets([text3, self.spinless_ctrl])

        self.SetSizer(self.mainSizer)

    #----------------------------------------------------------------------
    def addWidgets(self, widgets):
        """"""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for widget in widgets:
            if isinstance(widget, wx.StaticText):
                sizer.Add(widget, 0, wx.ALL|wx.CENTER, 5),
            else:
                sizer.Add(widget, 0, wx.ALL, 5)
        self.mainSizer.Add(sizer)

########################################################################
class MyFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Spinner Demo")
        panel = MyPanel(self)
        self.Show()

if __name__ == "__main__":        
    app = wx.App(False)
    f = MyFrame()
    app.MainLoop()