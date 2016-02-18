import pygame
from pylab import *
import time

#set up the figure
ion()
tstart = time.time()               # for profiling
x = arange(0,2*pi,0.01)            # x-array
line, = plot(x,cos(x))
freq = 0.00
def updateGraph(frequencey):
    line.set_ydata(cos(x*2*pi*frequencey))  # update the data
    draw()


#define simple colors
white = (255, 255, 255)
black = (0, 0, 0)
pygame.init()
FPS = 30
dWidth = 600
dHeight = 400
dDimensions = (dWidth, dHeight)
gameDisplay = pygame.display.set_mode(dDimensions)
pygame.display.set_caption('Rat Grid Cell Simulation')
clock = pygame.time.Clock()

ratImage = pygame.image.load('rat.gif')

ratX = 50
ratY = 50
def rat(x, y):
	gameDisplay.blit(ratImage, (ratX, ratY))

crashed = False
isKeyPressed = False
pressedKey = pygame.K_DOWN

while not crashed:

	for event in pygame.event.get():

		#if used hit the exit button
		if event.type == pygame.QUIT:
			crashed = True

		#check if keydown or keyup events happened
		if event.type == pygame.KEYDOWN:
			isKeyPressed = True
			pressedKey = event.key

		if event.type == pygame.KEYUP:
			isKeyPressed = False

	if isKeyPressed:
		if pressedKey == pygame.K_RIGHT:
			ratX += 1
			freq += 0.01
		elif pressedKey == pygame.K_LEFT:
			ratX -= 1
			freq -= 0.01

		print(event)
		gameDisplay.fill(white)
		rat(ratY, ratY)
		updateGraph(freq)
		print("frequency: " + str(freq))
		pygame.display.update()
	clock.tick(FPS)