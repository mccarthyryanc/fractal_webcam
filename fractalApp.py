# Image a Webcam fractal generator
# Purpose: This script with "fractalize" any image/ webcam video using
#			mapping z_n+1 = (z_n)^2 + c. Where "c" is defined by the user.
#
# Date: Sept. 2010
#
# Author: Ryan Schilt
#		  ryan.schilt@gmail.com
#
# Copyleft: feel free to share/edit/destory as you please :-)

import wx, os, math, wx.html, sys, pygame, Image, opencv
from pygame.locals import *
from opencv import highgui

MAIN_WINDOW_DEFAULT_SIZE = (640,400)
ABOUT_DIALOG_SIZE = (400,280)
CONST_DIALOG_SIZE = (300,150)
global fractal_const
fractal_const = [0,0]

class SetConstDialog(wx.Dialog):
	
	def __init__(self,parent):
		wx.Dialog.__init__(self, parent, -1, 'Define the Constant', size=CONST_DIALOG_SIZE)
		cText1 = "c = "
		cText2 = " + i "
		fractalType = ['Dendrite','Rabbit','SanMarco','Siegel']
		
		self.fractalChoices = wx.ComboBox(self, -1, pos=(20,10), size = (150,-1), choices=fractalType, style=wx.CB_READONLY)
		
		label1 = wx.StaticText(self, -1, cText1, pos=(20,50))
		self.realVal = wx.TextCtrl(self, -1, pos=(60,45))
		label2 = wx.StaticText(self, -1, cText2, pos=(140,50))
		self.imagVal = wx.TextCtrl(self, -1, pos=(180,45))
		
		self.printtext = wx.StaticText(self,-1,"Set constant's value!", pos=(20,80))

		self.btn1 = wx.Button(self, 8, 'Set', pos=(CONST_DIALOG_SIZE[0]/2 - 100, CONST_DIALOG_SIZE[1] - 40))
		self.btn2 = wx.Button(self, 9, 'Close', pos=(CONST_DIALOG_SIZE[0]/2, CONST_DIALOG_SIZE[1] - 40))
		
		self.fractalChoices.Bind(wx.EVT_COMBOBOX, self.OnSelect)
		self.btn1.Bind(wx.EVT_BUTTON, self.OnSet)
		self.btn2.Bind(wx.EVT_BUTTON, self.OnClose)

	def OnSelect(self, event):
		name = event.GetSelection()
		
		if name == 0:
			fractal_const = [0,1.0]
		elif name == 1:
			fractal_const = [-0.123,0.745]
		elif name == 2:
			fractal_const = [-0.75,0.0]
		elif name == 3:
			fractal_const = [-0.391,-0.587]


		self.realVal.SetValue(str(fractal_const[0]))
		self.imagVal.SetValue(str(fractal_const[1]))
		if fractal_const[1] >= 0 :
			self.printtext.Destroy()
			self.printtext = wx.StaticText(self,-1,"Const. Set: c = " + str(fractal_const[0]) + " + " + str(fractal_const[1]) + ' i', pos=(20,80))
		else:
			self.printtext.Destroy()
			self.printtext = wx.StaticText(self,-1,"Const. Set: c = " + str(fractal_const[0]) + " - " + str(math.fabs(fractal_const[1])) + ' i', pos=(20,80))


	def OnSet(self, event):
		print "Defining the const's value."
		tripval = True
		
		#get the raw string
		raw_real = self.realVal.GetValue().strip()
		raw_imag = self.imagVal.GetValue().strip()
		
		#check for only number in real text box
		if all(x in '0123456789.+-' for x in raw_real):
			#convert to float with only 5 decimal values
			fractal_const[0] = round(float(raw_real), 5)
			print fractal_const[0]
		else:
			self.printtext.Destroy()
			self.printtext = wx.StaticText(self,-1,"Numbers Only!", pos=(20,80))
			tripval = False

		#check for only number in imaginary text box
		if all(x in '0123456789.+-' for x in raw_imag):
			#convert to float with only 5 decimal values
			fractal_const[1] = round(float(raw_imag), 5)
			print fractal_const[1]
		else:
			self.printtext.Destroy()
			self.printtext = wx.StaticText(self,-1,"Numbers Only!", pos=(20,80))
			tripval = False

		if tripval:
			if fractal_const[1] >= 0 :
				self.printtext.Destroy()
				self.printtext = wx.StaticText(self,-1,"Const. Set: c = " + str(fractal_const[0]) + " + " + str(fractal_const[1]) + ' i', pos=(20,80))
			else:
				self.printtext.Destroy()
				self.printtext = wx.StaticText(self,-1,"Const. Set: c = " + str(fractal_const[0]) + " - " + str(math.fabs(fractal_const[1])) + ' i', pos=(20,80))

	def OnClose(self, event):
		self.Close()

class ImageFractalAbout(wx.Dialog):
	
	text = '''<html>
	<h1>Fractal Image App</h1>
	<p>Fractal Image App will turn any image file or webcam into a fractal using a simple Quadratic Mapping.</p>
	<p>More information is available at <a href="http://mathworld.wolfram.com/JuliaSet.html">Wolfram</a>.<p>
	<p>Created Sept. 2010, Copyleft ; Use it as you please :-)</p>
	</html>'''

	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, 'About Image to Fractal...', size=ABOUT_DIALOG_SIZE)
        
		html = wx.html.HtmlWindow(self)
		html.SetPage(self.text)
		# If a button has an ID of wx.ID_OK it will automatically close a wx.Dialog when pressed
		# create a 'button' object from wx.Button, give it the ID wx.ID_OK and text 'Okay'
		#button = wx.Button(self, wx.ID_OK, 'Okay')

		# Create a BoxSizer which grows in the vertical direction
		sizer = wx.BoxSizer(wx.VERTICAL)
		# Add the html window, tell it to take a 100% portion of the *available* area
		# and to EXPAND in ALL directions.  Use a border of 5 pixels around ALL sides of the button
		sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)

		# Add the button, ask it to grow by 0%
		#sizer.Add(button, 0)
		# also ask the button to align in the centre (my UK spelling!), with a 5 pixel border
		# around all sides
		#sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		# Tell our Dialog to use this new Sizer
		self.SetSizer(sizer)
		# Tell our Dialog to calculate the size of its items.  Good practice to always do this
		self.Layout()

class Frame(wx.Frame):

	def __init__(self, parent, id, title):
		style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER) # XOR to remove the resizeable border        
		wx.Frame.__init__(self, parent, id, title=title, size=MAIN_WINDOW_DEFAULT_SIZE, style=style)
		self.Center() # open in the centre of the screen
		self.panel = wx.Panel(self)
		self.panel.SetBackgroundColour('Black') # make the background of the window white

		self.CreateMenuBar()

		# create a StatusBar and give it 2 columns
		self.statusBar = self.CreateStatusBar()
		self.statusBar.SetFieldsCount(2)
		self.statusBar.SetStatusText('No image specified', 1)

		# set to None as we refer to it in ShowBitmap before we instantiate it
		self.bitmap = None

	def CreateMenuBar(self):
		"Create a menu bar"
		menuBar = wx.MenuBar()
		# Put MenuBar on Frame
		self.SetMenuBar(menuBar)
		menuFile = wx.Menu()
		menuBar.Append(menuFile, '&File')
		fileOpenMenuItem = menuFile.Append(-1, '&Open Image', 'Open a picture')
		self.Bind(wx.EVT_MENU, self.OnOpen, fileOpenMenuItem)
		
		#menu item for starting webcam
		webcamMenuItem = menuFile.Append(-1, '&Webcam', 'Start Webcam')
		self.Bind(wx.EVT_MENU, self.OnWebcam, webcamMenuItem)
		
		#menu item for Exit    
		exitMenuItem = menuFile.Append(-1, 'E&xit', 'Exit the viewer')        
		self.Bind(wx.EVT_MENU, self.OnExit, exitMenuItem)
		
		#Tools menu with Make Fractal and Set C items
		menuTools = wx.Menu()
		menuBar.Append(menuTools, '&Tools')
		toolsFractalItem = menuTools.Append(-1, '&Make Fractal', 'Make Fractal')
		self.Bind(wx.EVT_MENU, self.OnMakeFractal, toolsFractalItem)
		
		toolsConstItem = menuTools.Append(-1, '&Set Const.', 'Set Constant')
		self.Bind(wx.EVT_MENU, self.OnSetConst, toolsConstItem)
		
		#Help menu with an About item
		menuHelp = wx.Menu()
		menuBar.Append(menuHelp, '&Help')
		helpMenuItem = menuHelp.Append(-1, '&About', 'About screen')
		self.Bind(wx.EVT_MENU, self.OnAbout, helpMenuItem)
		
	def OnWebcam(self,event):
		print "This should start up the webcam..."
		res = (640,480)
		fps = 15.0
		webcamLoop = True
		
		# Delete image if it is there
		if self.bitmap is not None:
			self.bitmap.Destroy()
		window_list = self.panel.GetChildren()

		camera = highgui.cvCreateCameraCapture(0)
		def get_image():
			im = highgui.cvQueryFrame(camera)
			#convert Ipl image to PIL image
			return opencv.adaptors.Ipl2PIL(im) 

		pygame.init()
		window = pygame.display.set_mode(res)
		pygame.display.set_caption("Fractal Webcam")
		screen = pygame.display.get_surface()

		while webcamLoop:
			events = pygame.event.get()
			for event in events:
				if event.type == QUIT:
					webcamLoop = False
				
			im = get_image()
			pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
			screen.blit(pg_img, (0,0))
			pygame.display.flip()
			pygame.time.delay(int(1000 * 1.0/fps))
			
		if not(webcamLoop):
			highgui.cvDestroyAllWindows()
			pygame.quit()
			self.Destroy()
		
	def OnMakeFractal(self,event):
		print "Called the make fractal function"
		print "should remove the current image and replace it with the fractal bitmap."
		
	def OnSetConst(self, event):
		#print "Should open a dialog to enter real and imaginary values for constant."
		dlg = SetConstDialog(self)
		dlg.ShowModal()
		dlg.Destroy()
        
	def OnAbout(self, event):
		dlg = ImageFractalAbout(self)
		dlg.ShowModal()
		dlg.Destroy()

	def OnOpen(self, event):
		"Open an image file, set title if successful"
		# Create a file-open dialog in the current directory
		#Optional: Use this to only show image files
		#filters = 'Image files (*.gif;*.png;*.jpg)|*.gif;*.png;*.jpg'
		#dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(), defaultFile="", wildcard=filters, style=wx.OPEN)
		dlg = wx.FileDialog(self, message="Open an Image...", defaultDir=os.getcwd(), defaultFile="", style=wx.OPEN)
		
		# Call the dialog as a model-dialog so we're required to choose Ok or Cancel
		if dlg.ShowModal() == wx.ID_OK:
			# User has selected something, get the path, set the window's title to the path
			filename = dlg.GetPath()
			self.SetTitle(filename)
			wx.BeginBusyCursor()
			self.image = wx.Image(filename, wx.BITMAP_TYPE_ANY, -1) # auto-detect file type        
			self.statusBar.SetStatusText('Size = %s' % (str(self.image.GetSize())), 1)
			self.ShowBitmap()            
			wx.EndBusyCursor()
		
		dlg.Destroy()
    
	def ShowBitmap(self):
		window_list = self.panel.GetChildren()
		# Delete image if it is there
		if self.bitmap is not None:
			self.bitmap.Destroy()
		window_list = self.panel.GetChildren()

		# Convert to Bitmap for wxPython to draw it to screen
		self.bitmap = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.image))       
		# Make the application's window as large as the image
		self.SetClientSize(self.bitmap.GetSize())
		self.Center()

	def OnExit(self, event):
		self.Destroy()
		

class App(wx.App):
	
	def OnInit(self):
		self.frame = Frame(parent=None, id=-1, title='Fractal Image App')
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

if __name__ == "__main__":       
	# make an App object, set stdout to the console so we can see errors
	app = App(redirect=False)
	app.MainLoop()
