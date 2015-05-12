
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
        self.axes = self.figure.add_axes([0.082,0.1,0.8,0.8])
        self.axes.grid(True)

        #self.axes.yaxis.tick_right()
        t = [0, 5, 15, 20, 25, 30, 35, 50, 70, 90]
        s = [0] 
        self.s1 = [100, 400, 1000, 1000, 600, 400, 300, 300, 200]
        s = s + self.s1
        self.data1 = s
        self.data2 = [0]
        #self.y_max = 10

        self.plot_data = self.axes.plot(
            self.data1, 
            linewidth=1,
            color='blue',
            )[0]

        self.plot_data.set_xdata(np.arange(len(self.data1)))
        self.plot_data.set_ydata(np.array(self.data1))
        self.axes.set_xlabel('Reletive Time (s)', color = 'b')
        self.axes.set_ylabel('Preset temprature (C)', color='b')
        ymax = max(s) + max(s)*0.15
        ymin = 0
        self.axes.set_ybound(lower=ymin, upper=ymax)
        for tl in self.axes.get_yticklabels():
            tl.set_color('blue')



        self.ax2 = self.axes.twinx()
        self.plot_data2 = self.ax2.plot(
            self.data2, 
            linewidth=2,
            color='green',
            )[0]
        self.plot_data2.set_xdata(np.arange(len(self.data2)))
        self.plot_data2.set_ydata(np.array(self.data2))
        self.ax2.set_xlabel('Real Time', color='g')
        self.ax2.set_ylabel('Real-time temprature(C)', color='g')
        self.ax2.set_ybound(lower=ymin, upper=ymax)

        


        self.canvas = FigureCanvas(self, -1, self.figure)
        
        sizer.Add(self.canvas)

        self.SetSizer(sizer)
        self.canvas.draw()

    
        
        
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


