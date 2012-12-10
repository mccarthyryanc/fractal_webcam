#!/usr/bin/env python
# File test.py

# Import image stuff
from PIL import Image, ImageTk

import pygtk
pygtk.require('2.0')
import gtk, os, math

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print "PyGtk 2.3.90 or later required for this example"
   raise SystemExit

# Create dialog
dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
dialog.set_default_response(gtk.RESPONSE_OK)

filter = gtk.FileFilter()
filter.set_name("All files")
filter.add_pattern("*")
dialog.add_filter(filter)

filter = gtk.FileFilter()
filter.set_name("Images")
filter.add_mime_type("image/png")
filter.add_mime_type("image/jpeg")
filter.add_mime_type("image/gif")
filter.add_pattern("*.png")
filter.add_pattern("*.jpg")
filter.add_pattern("*.gif")
filter.add_pattern("*.tif")
filter.add_pattern("*.xpm")
dialog.add_filter(filter)

# Run dialog
response = dialog.run()
if response == gtk.RESPONSE_OK:
    print dialog.get_filename(), 'selected'
elif response == gtk.RESPONSE_CANCEL:
    print 'Closed, no files selected'

filename = dialog.get_filename()

# Get ride of dialog 
dialog.destroy()

#here you load the image you are going to use
Logo_IMG = Image.open(filename)
#here you use Photoimage to assign the image to ImageTk
Logo_TK = ImageTk.PhotoImage(Logo_IMG)
#here you create a simple canvas widget -I assume you have already a frame to put it
Canv_logo = Canvas(your_canvas_frame, width=50, height=50, bg="white", bd=0)
#here you show the image in the canvas
Canv_logo.create_image(36, 36, image=Logo_TK)
Canv_logo.grid()
#here you reference at the image again -without this you won't see the image-
Canv_logo.image = Logo_TK
