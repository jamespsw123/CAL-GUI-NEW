import wx

class windowClass(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)
        self.basicGUI()

    def basicGUI(self):
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit')

        menuBar.Append(fileButton, 'File')
        
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.Quit, exitItem)

        self.SetTitle('CAL simulator')

        self.Show(True)

    def Quit(self,e):
        self.Close()

def main():
    app = wx.App()
    windowClass(None)

    app.MainLoop()
main()