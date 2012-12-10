# Purpose: Generate a Sierpinski Triangle with a webcam! Simply aim the webcam at the computer monitor!
#
# Date: Nov. 5, 2010
#
# Author: Ryan Schilt
#
# Note: You need a webcam that isn't attached to the monitor, i.e. a USB webcam. This was hacked together quickly
#		so use and manipulate this code in anyway you want :-)

import pygame, Image, wx, math
from pygame.locals import *
import sys, opencv
from opencv import highgui 
from sympy import *

#set resolution
res = (640,480)
#set frame rate
fps = 30.0

#-------------------define functions------------------------------------
fun_names = ["z", "2z","-z","iz","(1 + i) z","z^2","z^3","1/z","bipole","Polynomial1","Polynomial2","Fraction","Spiral"];
fun_text = ["z", "2*z","-z","i*z","(1 + i)*z","z**2","z**3","1/z","1/(4*z**2-1)","-5*(z**3/3-z/4)/2","2*z**4+4*(1-i)*z**3/3-(1+i)*z**2-z","((z-0.5)/(z+0.5))**2","log(z)*(240/320-4*i)/(2*Pi)"]; 

#define sympy function for webcam
f = Function('f', complex=True)
z = symbols('z')
f = sympify(fun_text[0])

#grab system camera info
camera = highgui.cvCreateCameraCapture(0)

#function for mapping webcam dimensions to unit square
def pix2complex(x,y,res):
	tempx = (2*x)/res[0] - 1
	tempy = -(2*y)/res[1] + 1
	z = tempx + I*tempy
	return z

#function for mapping from unit square to webcam dimensions
def complex2pix(z, res):
	tempx =res[0]*(re(z) + 1)/2
	tempy = -1*res[1]*(im(z) - 1)/2
	return int(round(tempx)),int(round(tempy))

#function to build pullback image
def buildPullback(im,res,f):
	#load image to get access to 
	oldIm = im.load()
	newbmp = Image.new("RGB", res, "Black")
	tempbmp = newbmp.load()
	
	#loop through pixels
	for x in range(0, res[0]):
		for y in range(0,res[1]):
			#map from pixel to unit square
			currpix = pix2complex(x,y,res)
			#map from z -> f(z)
			newpix = N(f.subs({z:currpix}))
			#performs mapping on torus
			newpix = ((re(newpix) % 2)-1) + I*((im(newpix) % 2)-1)
			#map from f(z) to pixel value
			finpix = complex2pix(newpix,res)
			tempbmp[x,y] = oldIm[finpix[0],finpix[1]]
			
	return newbmp

#function to grab current image from camera
def get_image():
    im = highgui.cvQueryFrame(camera)
    # Add the line below if you need it (Ubuntu 8.04+)
    #im = opencv.cvGetMat(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im) 

pygame.init()
window = pygame.display.set_mode((res[0]*2,res[1]))
pygame.display.set_caption("Conformal Webcam")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)
    im = get_image()
    
    #prepare camera image
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    
    #prepare mapped image
    mapped_im = buildPullback(im,res,f)

	#place images
    screen.blit(pg_img, (0,0))
    screen.blit(mapped_im, (res[0],0))
    
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
