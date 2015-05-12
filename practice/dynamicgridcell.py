import wx
import wx.grid as grid
#
class Button(wx.Frame):
    def __init__(self, parent, source):
        wx.Frame.__init__(self, parent, -1, size=(100,100))
        self.source = source
        self.pos = 0 
        self.button = wx.Button(self, label='0')
        self.Bind(wx.EVT_BUTTON, self.onbutton, self.button)
        self.Show()

    def onbutton(self, evt):
        self.pos += 1
        self.source.grid.Scroll(self.pos, self.pos) 
        self.button.SetLabel(str(self.pos))  

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Grid", size=(350,250))
        self.grid = grid.Grid(self)
        self.grid.CreateGrid(20, 20)
        self.but = Button(None, self)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame(None)
    frame.Show()
    app.MainLoop()