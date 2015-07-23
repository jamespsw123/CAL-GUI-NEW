
import wx
import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class TabPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.figure = matplotlib.figure.Figure(figsize=(10,5), dpi=None)
        self.figure.patch.set_facecolor('white')
        #self.axes = self.figure.add_axes([0,0,1,1])
        #self.axes = self.figure.add_subplot(111)
        self.axes = self.figure.add_axes([0.082,0.1,0.8,0.8])
        self.axes.grid(True)

        #self.axes.yaxis.tick_right()
        t = [0, 5, 15, 20, 25, 30, 35, 50, 70, 90]
        s = [0] 
        self.s1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        s = s + self.s1
        self.data1 = s
        #self.y_max = 10

        self.plot_data = self.axes.plot(
            self.data1, 
            linewidth=1,
            color='blue',
            )[0]

        self.plot_data.set_xdata(np.arange(len(self.data1)))
        self.plot_data.set_ydata(np.array(self.data1))

    

        
        self.axes.set_xlabel('time (s)')
        self.axes.set_ylabel('Real-time temprature(C)', color='g')
        ymax = max(s) + max(s)*0.15
        ymin = 0
        self.axes.set_ybound(lower=ymin, upper=ymax)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas.draw()
        sizer.Add(self.canvas)

        self.SetSizer(sizer)
        #self.Center()

    
        
        
class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Panel One")
        panel = TabPanel(self)
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = DemoFrame()
    app.MainLoop()


