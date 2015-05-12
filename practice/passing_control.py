import wx
import wx.grid as gridlib
# import  pyodbc


class RightPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        grid = gridlib.Grid(self)
        grid.CreateGrid(5, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)


class LeftPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        self.create_controls()
        self.SetBackgroundColour("light green")

    def create_controls(self):

        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.button = wx.Button(self, label="Press me!")

        self.v_sizer.Add(self.button, 0)

        self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND)
        self.SetSizer(self.v_sizer)


class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "DB Viewer", size=(350, 250))

        splitter = wx.SplitterWindow(self)
        leftP = LeftPanel(splitter)
        self.rightP = RightPanel(splitter)

        splitter.SplitVertically(leftP, self.rightP)
        splitter.SetMinimumPaneSize(20)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        leftP.button.Bind(wx.EVT_BUTTON, self.on_button_pressed)

        self.Layout()

    def on_button_pressed(self, event):
            self.rightP.SetBackgroundColour("light blue")
            self.Refresh()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()