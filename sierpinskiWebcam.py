# Purpose: Generate a Sierpinski Triangle with a webcam! Simply aim the webcam at the computer monitor!
#
# Date: Nov. 5, 2010
#
# Author: Ryan Schilt
#
# Note: You need a webcam that isn't attached to the monitor, i.e. a USB webcam. This was hacked together quickly
#		so use and manipulate this code in anyway you want :-)

import pygame, Image, wx, math, random
from pygame.locals import *
import sys, cv
from cv import highgui 

#set resolution
res = (640,480)
#set frame rate
fps = 30.0

#set rectangles size
red_size = (random.randint(0,res[0]),random.randint(0,res[1]))
green_size = (random.randint(0,res[0]),random.randint(0,res[1]))
blue_size = (random.randint(0,res[0]),random.randint(0,res[1]))

#set transparency
alphaValue = 50

#difine rectangles size and color
blueRect = pygame.Surface(blue_size)
blueRect.fill((0,0,255))
redRect = pygame.Surface(red_size)
redRect.fill((255,0,0))
greenRect = pygame.Surface(green_size)
greenRect.fill((0,255,0))

#set rectangles position
red_pos = (random.randint(0,res[0]),random.randint(0,res[1]))
green_pos = (random.randint(0,res[0]),random.randint(0,res[1]))
blue_pos = (random.randint(0,res[0]),random.randint(0,res[1]))

#set alpha value
redRect.set_alpha(alphaValue)
greenRect.set_alpha(alphaValue)
blueRect.set_alpha(alphaValue)

#grab system camera info
camera = highgui.cvCreateCameraCapture(0)

#function to change rectangle position
def set_rectPos():
	newpos = (random.randint(0,res[0]),random.randint(0,res[0]),random.randint(0,res[0]),random.randint(0,res[1]),random.randint(0,res[1]),random.randint(0,res[1]))
	return newpos

#function to change rectangle size
def set_rectSize():
	newsize = (random.randint(0,res[0]),random.randint(0,res[0]),random.randint(0,res[0]),random.randint(0,res[1]),random.randint(0,res[1]),random.randint(0,res[1]))
	return newsize

#function to grab current image from camera
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im) 

pygame.init()
window = pygame.display.set_mode((res[0]*2,res[1]*2))
pygame.display.set_caption("Sierpinski Webcam")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    
    #place color rectangles
    if event.type == MOUSEBUTTONDOWN:
		newpos = set_rectPos()
		newsize = set_rectSize()
		
		red_pos = (newpos[0],newpos[3])
		green_pos = (newpos[1],newpos[4])
		blue_pos = (newpos[2],newpos[5])

		red_size = (newsize[0],newsize[3])
		green_size = (newsize[1],newsize[4])
		blue_size = (newsize[2],newsize[5])
		
		blueRect = pygame.Surface(blue_size)
		blueRect.fill((0,0,255))
		redRect = pygame.Surface(red_size)
		redRect.fill((255,0,0))
		greenRect = pygame.Surface(green_size)
		greenRect.fill((0,255,0))
		
		redRect.set_alpha(alphaValue)
		greenRect.set_alpha(alphaValue)
		blueRect.set_alpha(alphaValue)
		
		screen.fill((0,0,0))

	#place camera images
    screen.blit(pg_img, (0,0))
    screen.blit(pg_img, res)
    screen.blit(pg_img, (0,res[1]))
		
    screen.blit(redRect, red_pos)
    screen.blit(greenRect, green_pos)
    screen.blit(blueRect, blue_pos)
    
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
