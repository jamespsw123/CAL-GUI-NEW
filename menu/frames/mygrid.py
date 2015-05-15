import wx
import wx.grid as  gridlib
 
class MyGrid(wx.Panel):
 
    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
 
        # Add a panel so it looks the correct on all platforms
        #panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(self)
        self.grid.CreateGrid(0,4)
        #grid.SetRowLabelSize(0)
 
        # change a couple column labels
        self.grid.SetColLabelValue(0, "Time")
        #grid.AutoSizeColumn(0)

        self.grid.SetColLabelValue(1, "Furnace Temperature")
        self.grid.AutoSizeColumn(1)
        
        self.grid.SetColLabelValue(2, "Current Set-point Temperature")
        self.grid.AutoSizeColumn(2)

        self.grid.SetColLabelValue(3, "Indi-Thermocouple Temperature")
        self.grid.AutoSizeColumn(3)

        self.grid.AppendRows(numRows=1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)

class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Panel One")
        panel = MyGrid(self)
        self.Show()
 
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = DemoFrame()
    app.MainLoop()