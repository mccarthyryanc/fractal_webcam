# Purpose: Subprocess called my webcamMain.py to open multiple webcam windows
#
# Date: Nov. 5, 2010
#
# Author: Ryan Schilt
#
# Note: Hacked together quickly so use and manipulate in anyway you want :-)

import pygame, Image
from pygame.locals import *
import sys, opencv
from opencv import highgui 

#resolution of windows
res = (640,480)

camera = highgui.cvCreateCameraCapture(0)
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im) 


fps = 30.0
pygame.init()
window = pygame.display.set_mode(res)
pygame.display.set_caption("WebCam Demo")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
