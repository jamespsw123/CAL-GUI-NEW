# !/usr/laopeng/Google Drive/opt project/CAL_GUI

# wxpython_4.py


import wx

class windowClass(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(windowClass, self).__init__(*args, **kwargs)
		self.basicGUI()

	def basicGUI(self):

		#panel
		panel = wx.Panel(self)

		#menu bar
		menuBar = wx.MenuBar()
		
		#menubar buttons
		fileButton = wx.Menu()
		editButton = wx.Menu()
		importItem = wx.Menu()

		importItem.Append(wx.ID_ANY, 'Import Document...')
		importItem.Append(wx.ID_ANY, 'Import Picture...')
		importItem.Append(wx.ID_ANY, 'Import Video...')

		fileButton.AppendMenu(wx.ID_ANY, 'Import', importItem)


		exitItem = wx.MenuItem(fileButton, wx.ID_EXIT, 'Quit')
		exitItem.SetBitmap(wx.Bitmap('Fire.bmp'))
		fileButton.AppendItem(exitItem)

		menuBar.Append(fileButton, 'File')
		menuBar.Append(editButton, 'Edit')

		self.SetMenuBar(menuBar)
		self.Bind(wx.EVT_MENU, self.Quit, exitItem)


		nameBox = wx.TextEntryDialog(None, 'What is your name?', 'Welcome','name')

		if nameBox.ShowModal() == wx.ID_OK:
			userName = nameBox.GetValue()
		
		#yes or no pop up box
		yesNoBox = wx.MessageDialog(None, 'Are you sure?', 'Question', wx.YES_NO)
		yesNoAnswer = yesNoBox.ShowModal()
		yesNoBox.Destroy()








		if yesNoAnswer == wx.ID_NO:
			userName = 'Loser!'

		chooseOneBox = wx.SingleChoiceDialog(None, 'What\'s your favorite color?',
													'Color Question',
													['Green','Red','Blue','Yellow'])
		if chooseOneBox.ShowModal() == wx.ID_OK:
			favColor = chooseOneBox.GetStringSelection()

		#text editor
		wx.TextCtrl(panel, pos = (3,100), size=(150, 50))

		aweText = wx.StaticText(panel, -1, 'Awesome Text', (3, 3 ))
		aweText.SetForegroundColour('#67cddc')
		aweText.SetBackgroundColour('black')

		rlyAweText = wx.StaticText(panel, -1, 'Customized Awesomeness', (3, 30))
		rlyAweText.SetForegroundColour(favColor)
		rlyAweText.SetBackgroundColour('black')		

		

		#display window
		self.SetTitle('welcome ' + userName) 
		self.Show(True)

	#Quit def
	def Quit(self,e):
		self.Close()




def main():
	app = wx.App()
	windowClass(None)

	app.MainLoop()

if __name__=='__main__':
	main()
