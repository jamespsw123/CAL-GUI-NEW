import wx
import wx.grid as  gridlib
 
class MyGrid(wx.Panel):
 
    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
 
        # Add a panel so it looks the correct on all platforms
        #panel = wx.Panel(self, wx.ID_ANY)
        grid = gridlib.Grid(self)
        grid.CreateGrid(0,3)
        #grid.SetRowLabelSize(0)
 
        # change a couple column labels
        grid.SetColLabelValue(0, "Time")
        #grid.AutoSizeColumn(0)

        grid.SetColLabelValue(1, "Furnace Temperature")
        grid.AutoSizeColumn(1)
        
        grid.SetColLabelValue(2, "Current Set-point Temperature")
        grid.AutoSizeColumn(2)
        grid.AppendRows(numRows=1)
        """
        grid.SetCellValue(0, 0, "10:10:10")
        grid.SetCellValue(0, 1, "20")
        grid.SetCellValue(0, 2, "30")
        grid.SetCellAlignment(0,0,wx.ALIGN_CENTER,wx.ALIGN_CENTER) 
        grid.SetCellAlignment(0,1,wx.ALIGN_CENTER,wx.ALIGN_CENTER) 
        grid.SetCellAlignment(0,2,wx.ALIGN_CENTER,wx.ALIGN_CENTER) 
        """
        """
        # change the row labels
        for row in range(25):
            rowNum = row + 1
            grid.SetRowLabelValue(row, "Row %s" % rowNum)
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 1, wx.EXPAND, 5)
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