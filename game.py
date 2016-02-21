import pygame
import matplotlib.pyplot as plt
from numpy import *
import time

#important constants
somaStaticFreq = 6.42
dendriteStaticFrequency = 6.42
threshold = 0.80

#just for the beginning, this is true
resultantFrequency = dendriteStaticFrequency - somaStaticFreq

#set up the figure
timeStart = 0
timeEnd = 4
plt.ion()
# plt.show(block=True)
tstart = time.time()            # for profiling
resolution = 1
x = []            				# x-array

#set up dendrite plot and a function to update it
plt.figure(1)
dendFig = plt.subplot(411)
somaFig = plt.subplot(412)
totalFig = plt.subplot(413)
fireFig = plt.subplot(414)
dendYdata = []
dendLine, = dendFig.plot(x, dendYdata)
somaYdata = []
somaLine, = somaFig.plot(x, somaYdata)
totalYdata = []
totalLine, = totalFig.plot(x, totalYdata)
firePointsX = []
firePointsY = []
fireLine, = fireFig.plot(firePointsX, firePointsY, marker='o', linestyle='')
plt.show()
counter = 0
def updateGraphs(currentTime, speed, dendLine, somaLine, totalLine):
	currentTimeStep = currentTime*resolution
	x.append(currentTimeStep)
	#update the frequencies
	dendTotalFrequency = dendriteStaticFrequency+speed
	resultantFrequency = dendTotalFrequency - somaStaticFreq
	#update figure boundaries
	dendFig.axis([currentTime-4, currentTimeStep, -1, 1])
	somaFig.axis([currentTime-4, currentTimeStep, -1, 1])
	totalFig.axis([currentTime-4, currentTimeStep, -1, 1])
	#update dendrite figure
	dendYdata.append(sin(2*pi*currentTimeStep*dendTotalFrequency))
	dendLine.set_data(x, dendYdata)
	#update soma figure
	somaYdata.append(sin(2*pi*currentTimeStep*somaStaticFreq))
	somaLine.set_data(x, somaYdata)
	#update total figure
	totalYdata.append(sin(2*pi*currentTimeStep*resultantFrequency))
	totalLine.set_data(x, totalYdata)
	# totalLine.set_xdata(x)
	#update fire line 
	# if counter % 10 == 0:
	firePointsX.append(currentTimeStep*resolution)
	if sin(2*pi*currentTimeStep*resultantFrequency) > threshold:
		firePointsY.append(1)
	else:
		firePointsY.append(0)
	fireLine.set_ydata(firePointsY)
	fireLine.set_xdata(firePointsX)

	fireFig.axis([currentTime-4, currentTimeStep, 0, 2])
	# dendFig.clear()
	# plt.draw()
	

# def updateDend(frequencey):
# 	dendLine.set_ydata(x, sin(x*dendriteStaticFrequency))
# 	plt.draw()
    # dendrline.set_ydata(sin(x*dendriteStaticFrequency))  # update the data
    # plt.draw()

#draw static soma frequency
# somaline, = plt.plot(x,sin(x))
# dendrline.set_ydata(sin(x*somaFreq))  # update the data
# plt.draw()


#define simple colors
white = (255, 255, 255)
black = (0, 0, 0)
pygame.init()
FPS = 10
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
	# print("displaying rat at (" + str(ratX) + ", " + str(ratY)+ ")")

def calculateRatPosition(xSpe, xLoc, ySpe, yLoc):
	xLoc += xSpe * FPS * speedScale
	yLoc += ySpe * FPS * speedScale
	return (xLoc,yLoc)

#define game control mechanism properties
crashed = False
isKeyPressed = False
pressedKey = None
time = 0
dt = 1/FPS
prev_x = ratX
prev_y = ratY

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
		elif pressedKey == pygame.K_LEFT:
			xSpeed -= 1
		elif pressedKey == pygame.K_UP:
			ySpeed += 1
		elif pressedKey == pygame.K_DOWN:
			ySpeed -= 1

		# update the display and print the event
		# print(event)

	#if rat reached a vertical edge flip the x speed
	if(ratX > dWidth or ratX < 0):
		xSpeed = -xSpeed
	#if rat reached a horizontal edge flip the y speed
	if(ratY < -dHeight or ratY > 0):
		ySpeed = -ySpeed

	#calculate the position of the rat and display it
	prev_x = ratX
	prev_y = ratY
	(ratX, ratY) = calculateRatPosition(xSpeed, ratX, ySpeed, ratY)

	gameDisplay.fill(white)
	displayRat(ratY, ratY)

	#calculate the speed of the rat
	
	dx = ratX - prev_x
	dy = ratY - prev_y
	speed = sqrt( xSpeed**2 + ySpeed**2 ) / 100
	angle = arctan( (dy/dt) / (dx/dt + 0.0001) )
	print("speed: " + str(speed))
	print("angle: " + str(angle))
	time += 0.01
	updateGraphs(time, speed, dendLine, somaLine, totalLine)
	pygame.display.update()
	#run the next game step
	clock.tick(FPS)