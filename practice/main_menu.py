import wx
import os
'''
########################################################################
class RandomPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
 
########################################################################
'''
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
 
        topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(topSplitter)
 
        self.panelOne = panelOne = wx.Panel(vSplitter)
        panelTwo = wx.Panel(vSplitter)
        vSplitter.SplitVertically(panelOne, panelTwo)
        vSplitter.SetSashGravity(0.5)
 
        panelThree = wx.Panel(topSplitter)
        topSplitter.SplitHorizontally(vSplitter, panelThree)
        topSplitter.SetSashGravity(0.5)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
 
########################################################################
class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Nested Splitters",
                          size=(800,600))
        panel = MainPanel(self)
        panel.panelOne.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.InitUI()
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

        '''
        topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(topSplitter)

        panel1 = RandomPanel(vSplitter,"blue")
        panel2 = RandomPanel(vSplitter,"red")
        vSplitter.SplitVertically(panel1, panel2)
        vSplitter.SetSashGravity(0.5)

        panel3 = RandomPanel(topSplitter,"green")
        topSplitter.SplitHorizontally(vSplitter, panel3)
        topSplitter.SetSashGravity(0.5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        '''
        TopSplitter = wx.SplitterWindow(self)
        panel1 = wx.Panel(TopSplitter, -1)
        panel1.SetBackgroundColour(wx.LIGHT_GREY)
        panel2 = wx.Panel(TopSplitter, -1)

        TopSplitter.SplitVertically(panel1, panel2, sashPosition=280)
        TopSplitter.SetSashGravity(0.5)



        #vbox = wx.BoxSizer(wx.VERTICAL)

        #midPan = wx.Panel(panel)
        #midPan.SetBackgroundColour('#ededed')

        #vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 20)
        #panel.SetSizer(vbox)
        imagesPath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        # creating a toolbar 
        toolbar = self.CreateToolBar()
        tool1 = toolbar.AddLabelTool(wx.ID_ANY, 'New', 
            wx.Bitmap(os.path.join(imagesPath, 'images/new3.png')))
        tool2 = toolbar.AddLabelTool(wx.ID_ANY, 'Open', 
            wx.Bitmap(os.path.join(imagesPath, 'images/open3.png')))
        tool3 = toolbar.AddLabelTool(wx.ID_ANY, 'Save', 
            wx.Bitmap(os.path.join(imagesPath, 'images/save3.png')))
        tool4 = toolbar.AddLabelTool(wx.ID_ANY, 'Print', 
            wx.Bitmap(os.path.join(imagesPath, 'images/printer3.png')))
        tool5 = toolbar.AddLabelTool(wx.ID_ANY, 'Setting', 
            wx.Bitmap(os.path.join(imagesPath, 'images/setting.png')))
        tool6 = toolbar.AddLabelTool(wx.ID_ANY, 'Quit', 
            wx.Bitmap(os.path.join(imagesPath, 'images/exit3.png')))
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
        panel1.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    def OnQuit(self, e):
        self.Close()
    def OnSetting(self, e):
        Setting = STM_T()
        Setting.Show()

    def OnRightDown(self, e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())

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
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()