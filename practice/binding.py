import wx
 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Button Tutorial")
        panel = wx.Panel(self, wx.ID_ANY)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        buttonOne = wx.Button(panel, label="One", name = "1")
        buttonTwo = wx.Button(panel, label="Two", name = "2")
        buttonThree = wx.Button(panel, label="Three", name = "3")
        buttons = [buttonOne, buttonTwo, buttonThree]
 
        for button in buttons:
            self.buildButtons(button, sizer)
 
        panel.SetSizer(sizer)
 
    #----------------------------------------------------------------------
    def buildButtons(self, btn, sizer):
        """"""
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        sizer.Add(btn, 0, wx.ALL, 5)
 
    #----------------------------------------------------------------------
    def onButton(self, event):
        """
        This method is fired when its corresponding button is pressed
        """
        #button = event.GetEventObject()
        #print "The button you pressed was labeled: " + button.GetLabel()
        #print "The button's name is " + button.GetName()
 
        button_id = event.GetId()
        print button_id
        button_by_id = self.FindWindowById(button_id)
        print "The button you pressed was labeled: " + button_by_id.GetLabel()
        print "The button's name is " + button_by_id.GetName()
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()