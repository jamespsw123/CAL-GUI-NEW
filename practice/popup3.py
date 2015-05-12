import wx

########################################################################
class TestPopup(wx.PopupWindow):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, style):
        """Constructor"""
        wx.PopupWindow.__init__(self, parent, style)

        panel = wx.Panel(self)
        self.panel = panel
        panel.SetBackgroundColour("CADET BLUE")

        st = wx.StaticText(panel, -1,
                           "This is a special kind of top level\n"
                           "window that can be used for\n"
                           "popup menus, combobox popups\n"
                           "and such.\n\n"
                           "Try positioning the demo near\n"
                           "the bottom of the screen and \n"
                           "hit the button again.\n\n"
                           "In this demo this window can\n"
                           "be dragged with the left button\n"
                           "and closed with the right."
                           ,
                           pos=(10,10))
        sz = st.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
        panel.SetSize( (sz.width+20, sz.height+20) )

        panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        panel.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        panel.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        panel.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        st.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        st.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        st.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        st.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        wx.CallAfter(self.Refresh)    

    def OnMouseLeftDown(self, evt):
        self.Refresh()
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.ClientToScreen((0,0))
        self.panel.CaptureMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.Move(nPos)

    def OnMouseLeftUp(self, evt):
        if self.panel.HasCapture():
            self.panel.ReleaseMouse()

    def OnRightUp(self, evt):
        self.Show(False)
        self.Destroy()

########################################################################
class TestPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        btn = wx.Button(self, label="Open Popup")
        btn.Bind(wx.EVT_BUTTON, self.onShowPopup)


    #----------------------------------------------------------------------
    def onShowPopup(self, event):
        """"""
        win = TestPopup(self.GetTopLevelParent(), wx.SIMPLE_BORDER)

        btn = event.GetEventObject()
        pos = btn.ClientToScreen( (0,0) )
        sz =  btn.GetSize()
        win.Position(pos, (0, sz[1]))

        win.Show(True)

########################################################################
class TestFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Test Popup")
        panel = TestPanel(self)
        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = TestFrame()
    app.MainLoop()