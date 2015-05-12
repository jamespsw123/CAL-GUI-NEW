#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx


class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        
        self.InitUI()
        
    def InitUI(self):   

        pnl = wx.Panel(self)

        sld = wx.Slider(pnl, value=200, minValue=150, maxValue=500, pos=(20, 20), 
            size=(250, -1), style=wx.SL_HORIZONTAL)
        
        sld.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
        
        self.txt = wx.StaticText(pnl, label='200', pos=(20, 90))               
        
        self.SetSize((290, 200))
        self.SetTitle('wx.Slider')
        self.Centre()
        self.Show(True)    

    def OnSliderScroll(self, e):
        
        obj = e.GetEventObject()
        val = obj.GetValue()
        
        self.txt.SetLabel(str(val))        

                      
def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()   