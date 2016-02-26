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
x = []          # x-array
freq = 0.0

#set up dendrite plot and a function to update it
plt.figure(1)
dendFig = plt.subplot(511)
somaFig = plt.subplot(512)
sumFig = plt.subplot(513)
totalFig = plt.subplot(514)
fireFig = plt.subplot(515)
dendYdata = []
dendLine, = dendFig.plot(x, dendYdata)
somaYdata = []
somaLine, = somaFig.plot(x, somaYdata)
sumYdata = []
sumLine, = sumFig.plot(x, sumYdata)
totalYdata = []
totalLine, = totalFig.plot(x, totalYdata)
firePointsX = []
firePointsY = []
fireLine, = fireFig.plot(firePointsX, firePointsY, marker='o', linestyle='')
plt.show()
counter = 0
def updateGraphs(currentTime, speed, angle, dendLine, somaLine, sumLine, totalLine):
	currentTimeStep = currentTime
	# print("current time step: " + str(currentTimeStep))
	x.append(currentTimeStep)
	dendTotalFrequency = dendriteStaticFrequency + speedScale*speed*cos(angle)
	resultantFrequency = dendTotalFrequency - somaStaticFreq
	# resultantFrequency = somaStaticFreq + somaStaticFreq*speed*cos(angle)
	# print("average distance: " + str(speed * cos(angle) / resultantFrequency))
	# print("resultantFrequency " + str(resultantFrequency) + "   " + str(sin(2*pi*currentTimeStep*resultantFrequency)))
	#update figure boundaries
	dendFig.axis([currentTime-4, currentTimeStep, -1, 1])
	somaFig.axis([currentTime-4, currentTimeStep, -1, 1])
	sumFig.axis([currentTime-4, currentTimeStep, -2, 2])
	totalFig.axis([currentTime-4, currentTimeStep, -1, 1])
	#update dendrite figure
	dendYdata.append(sin(2*pi*currentTimeStep*dendTotalFrequency))
	dendLine.set_data(x, dendYdata)
	#update soma figure
	somaYdata.append(sin(2*pi*currentTimeStep*somaStaticFreq))
	somaLine.set_data(x, somaYdata)
	#update sum figure
	sumYdata.append(sin(2*pi*currentTimeStep*somaStaticFreq) + sin(2*pi*currentTimeStep*dendTotalFrequency))
	sumLine.set_data(x, sumYdata)
	#update total figure
	# print(sin(2*pi*currentTimeStep*resultantFrequency))
	# print(resultantFrequency)
	# print(cos(2*pi*currentTimeStep*resultantFrequency))
	totalYdata.append(sin(2*pi*currentTimeStep*resultantFrequency))
	totalLine.set_data(x, totalYdata)
	#update fire line 
	firePointsX.append(currentTimeStep*resolution)
	fire = False
	if sin(2*pi*currentTimeStep*resultantFrequency) > threshold:
		firePointsY.append(1)
		fire = True
	else:
		firePointsY.append(0)
	fireLine.set_ydata(firePointsY)
	fireLine.set_xdata(firePointsX)

	fireFig.axis([currentTime-4, currentTimeStep, 0, 2])
	return fire
	

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

	#calculate the position and speed of 
	prev_x = ratX
	prev_y = ratY
	#calculate the position of the rat and display it
	(ratX, ratY) = calculateRatPosition(xSpeed, ratX, ySpeed, ratY)
	dy = ratY - prev_y
	dx = ratX - prev_x

	#calculate the angle
	if dx == 0:
		if dy == 0:
			angle = 0
		elif dy < 0:
			angle = -pi/2
		else:
			angle = pi/2
	elif( dy < 0 and dx < 0):
		angle = -arctan(dy/dx)
	else:
		angle = arctan( dy / dx )
	gameDisplay.fill(white)
	displayRat(ratY, ratY)
	time += 0.01
	speed = sqrt(ySpeed**2 + xSpeed**2)
	updateGraphs(time, speed, angle, dendLine, somaLine, sumLine, totalLine)
	# print("frequsency: " + str(freq))
	pygame.display.update()
	#run the next game step
	clock.tick(FPS)