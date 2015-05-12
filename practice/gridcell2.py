import wx
import wx.grid

class GridFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent)

        # Create a wxGrid object
        self.grid = wx.grid.Grid(self, -1)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        self.grid.CreateGrid(100, 10)

        # We can set the sizes of individual rows and columns
        # in pixels
        self.grid.SetRowSize(0, 60)
        self.grid.SetColSize(0, 120)

        # And set grid cell contents as strings
        self.grid.SetCellValue(0, 0, 'wxGrid is good')

        # We can specify that some cells are read.only
        self.grid.SetCellValue(0, 3, 'This is read.only')
        self.grid.SetReadOnly(0, 3)

        # Colours can be specified for grid cell contents
        self.grid.SetCellValue(3, 3, 'green on grey')
        self.grid.SetCellTextColour(3, 3, wx.GREEN)
        self.grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

        # We can specify the some cells will store numeric
        # values rather than strings. Here we set grid column 5
        # to hold floating point values displayed with width of 6
        # and precision of 2
        self.grid.SetColFormatFloat(5, 6, 2)
        self.grid.SetCellValue(0, 6, '3.1415')
        self.grid.AutoSize()
        self.Show()


if __name__ == '__main__':

    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()