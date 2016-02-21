import pygame
import matplotlib.pyplot as plt
from numpy import *
import time

#important constants
somaStaticFreq = 6.42
dendriteStaticFrequency = 6.91
threshold = 0.80

#just for the beginning, this is true
resultantFrequency = dendriteStaticFrequency - somaStaticFreq

#set up the figure
timeStart = 0
timeEnd = 4
plt.ion()
# plt.show(block=True)
tstart = time.time()            # for profiling
resolution = 0.01
x = arange(timeStart, timeEnd, resolution)            # x-array
freq = 0.0

#set up dendrite plot and a function to update it
plt.figure(1)
dendFig = plt.subplot(411)
somaFig = plt.subplot(412)
totalFig = plt.subplot(413)
fireFig = plt.subplot(414)
dendLine, = dendFig.plot(x, cos(2*pi*x*(dendriteStaticFrequency+freq)))
somaLine, = somaFig.plot(x, cos(2*pi*x*somaStaticFreq))
totalLine, = totalFig.plot(x, cos(2*pi*x*resultantFrequency))
firePointsX = arange(timeStart, timeEnd, resolution*10)
firePointsY = (cos(2*pi*firePointsX*resultantFrequency)>threshold).astype(int)
fireLine, = fireFig.plot(firePointsX, firePointsY, marker='o', linestyle='')
plt.show()

def updateGraphs(currentTime, dendSpeedFreq, dendLine, somaLine, totalLine):
	x = arange(currentTime - 4, currentTime, resolution)
	#update the frequencies
	dendTotalFrequency = dendriteStaticFrequency+dendSpeedFreq
	resultantFrequency = dendTotalFrequency - somaStaticFreq
	#update dendrite figure
	dendLine.set_ydata(cos(2*pi*x*dendTotalFrequency))
	# dendLine.set_xdata(x)
	#update soma figure
	somaLine.set_ydata(cos(2*pi*x*somaStaticFreq))
	# somaLine.set_xdata(x)
	#update total figure
	totalLine.set_ydata(cos(2*pi*x*resultantFrequency))
	# totalLine.set_xdata(x)
	#update fire line 
	firePointsX = arange(currentTime-4, currentTime, resolution*10)
	firePointsY = (cos(2*pi*firePointsX*resultantFrequency)>threshold).astype(int)
	fireLine.set_ydata(firePointsY)
	fireLine.set_xdata(firePointsX)
	

# def updateDend(frequencey):
# 	dendLine.set_ydata(x, cos(x*dendriteStaticFrequency))
# 	plt.draw()
    # dendrline.set_ydata(cos(x*dendriteStaticFrequency))  # update the data
    # plt.draw()

#draw static soma frequency
# somaline, = plt.plot(x,sin(x))
# dendrline.set_ydata(cos(x*somaFreq))  # update the data
# plt.draw()


#define simple colors
white = (255, 255, 255)
black = (0, 0, 0)
pygame.init()
FPS = 60
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
time = 0

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
	time += 0.01
	updateGraphs(time, freq, dendLine, somaLine, totalLine)
	# print("frequsency: " + str(freq))
	pygame.display.update()
	#run the next game step
	clock.tick(FPS)