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

# somaFreq = 6.42
# dendriteStaticFrequency = 6.91

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

#define rat properties and simple function(s)
ratImage = pygame.image.load('rat.gif')
ratX = 50
ratY = -50
ySpeed = 0
xSpeed = 0
speedScale = 0.01

def displayRat(x, y):
	gameDisplay.blit(ratImage, (ratX, -ratY))
	print("displaying rat at (" + str(ratX) + ", " + str(ratY)+ ")")

def calculateRatPosition(xSpe, xLoc, ySpe, yLoc):
	xLoc += xSpe * FPS * speedScale
	yLoc += ySpe * FPS * speedScale
	return (xLoc,yLoc)

#define game control mechanism properties
crashed = False
isKeyPressed = False
pressedKey = None

#the game loop
while not crashed:

	#event handler
	for event in pygame.event.get():

		#if used hit the exit button
		if event.type == pygame.QUIT:
			crashed = True

		#check if keydown or keyup events happened
		if event.type == pygame.KEYDOWN:
			isKeyPressed = True
			pressedKey = event.key

		#if user takes their hands off
		if event.type == pygame.KEYUP:
			isKeyPressed = False

	#if the user has a key pressed
	if isKeyPressed:
		# if right or left, move the rat's position
		# and adjust the frequence
		if pressedKey == pygame.K_RIGHT:
			xSpeed += 1
			freq += 0.01
		elif pressedKey == pygame.K_LEFT:
			xSpeed -= 1
			freq -= 0.01
		elif pressedKey == pygame.K_UP:
			ySpeed += 1
			# freq -= 0.01
		elif pressedKey == pygame.K_DOWN:
			ySpeed -= 1
			# freq -= 0.01

		#update the display and print the event
		print(event)

	#if rat reached a vertical edge flip the x speed
	if(ratX > dWidth or ratX < 0):
		xSpeed = -xSpeed
	#if rat reached a horizontal edge flip the y speed
	if(ratY < -dHeight or ratY > 0):
		ySpeed = -ySpeed

	#calculate the position of the rat and display it
	(ratX, ratY) = calculateRatPosition(xSpeed, ratX, ySpeed, ratY)
	gameDisplay.fill(white)
	displayRat(ratY, ratY)
	updateGraph(freq)
	# print("frequsency: " + str(freq))
	pygame.display.update()
	#run the next game step
	clock.tick(FPS)