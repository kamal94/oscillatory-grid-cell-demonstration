import pygame
import matplotlib.pyplot as plt
from numpy import *
import time

class Rat:
	dendriteStaticFrequency = 6.42
	speedScale = 2

	def __init__(self, X: int, Y: int, XSPEED, YSPEED, THRESHOLD: int, id: int):
		self.somaStaticFreq = 6.42
		self.x = X
		self.y = Y
		self.xSpeed = XSPEED
		self.ySpeed = YSPEED
		self.threshold = THRESHOLD
		self.id = id
		self.absSpeed = None
		self.prev_x = None
		self.prev_y = None
		self.angle = 0
		self.visitedPos = []
		self.firedPos = []
		self.fired = False
		self.BH = 0.00385

	def pos(self):
		return array([self.x, self.y])


	def displayRat(self, surface):
		# pygame.draw.circle(surface, (0,0,255), (int(self.x), int(self.y)), 3)
		# for i, j in self.visitedPos:
		# for i, j in self.firedPos:
		if self.fired:
			pygame.draw.circle(surface, red, (int(self.x), int(self.y)), 3)
		else:
			surface.set_at((int(self.x), int(self.y)), black)



	def moveRat(self, timeStep: int):
		#if rat reached a vertical edge flip the x speed
		# if((self.x > dWidth) or (self.x < 0)):
		# 	self.xSpeed = -self.xSpeed
			# crashed = True
			# print("Final firing points: " + str(ratFirePoints))
		#if rat reached a horizontal edge flip the y speed
		# if self.y < (dHeight ) or (self.y > 0):
		# 	self.ySpeed = -self.ySpeed
		self.prev_x = self.x
		self.prev_y = self.y
		self.x += self.xSpeed
		self.y -= self.ySpeed
		#calculate the speed of the rat
		self.dx = self.x - self.prev_x
		self.dy = -(self.y - self.prev_y)
		self.absSpeed = sqrt( self.xSpeed**2 + self.ySpeed**2 )
		if self.dx == 0:
			if self.dy == 0:
				self.angle = 0
			elif self.dy < 0:
				self.angle = -pi/2
			else:
				self.angle = pi/2
		elif( self.dy < 0 and self.dx < 0):
			self.angle = -arctan(self.dy/self.dx)
		else:
			self.angle = arctan( self.dy / self.dx )

		self.fire(timeStep)
		if self.fired:
			self.firedPos.append( (self.x, self.y) )
		self.visitedPos.append( (self.x, self.y) )

	def fire(self, timeStep: int):
		prefAngleZero = array([1, 0])
		prefAngleSixty = array([1/2, sqrt(3)/2])
		prefAngleOneTwenty = array([-1/2, sqrt(3)/2])
		prefAngleOneEighty = array([-1, 0])
		prefAngleTwoFourty = array([-1/2, -sqrt(3)/2])
		# prefAngleThreeTen = [-1/2, -sqrt(3)/2]
		self.functions = []
		angles = []
		angles.append(prefAngleZero)
		angles.append(prefAngleSixty)
		angles.append(prefAngleOneTwenty)
		# angles.append(prefAngleOneEighty)
		# angles.append(prefAngleTwoFourty)
		for ang in angles:
			self.BH*self.pos()
			result = cos( dot( (2*pi*self.somaStaticFreq*self.BH*self.pos()), (ang) ) )
			# result = cos(6.42*2*pi*timeStep) + cos(6.42 + 6.42*0.00385*self.absSpeed*cos(self.angle-ang))
			# Wi = self.somaStaticFreq + self.absSpeed*speedScale*cos(self.angle-ang)
			# result = cos(Wi * timeStep) + cos(self.somaStaticFreq*timeStep)
			self.functions.append(result)

		def listProduct(l: list):
			result = 1
			if len(l) == 0:
				return 0
			for i in l:
				result *= i
			return result

		answer = listProduct(self.functions)
		if all(answer > self.threshold):
			self.fired = True
		else:
			self.fired = False
		
		

def takeScreenShot(surface):
	rect = pygame.Rect(0, 0, dWidth, dHeight)
	sub = surface.subsurface(rect)
	import random
	name = str(time.time())+"screenshot.jpg"
	pygame.image.save(sub, name)

def drawCenterOrientation(surface, width, height, color):
	for x in range(width):
		surface.set_at((x, int(height/2)), color)
	for y in range(width):
		surface.set_at((int(width/2), y), color)
#important constants
threshold = 0.80

#just for the beginning, this is true
# resultantFrequency = dendriteStaticFrequency - somaStaticFreq

#set up the figure
timeStart = 0
timeEnd = 4
plt.ion()
# plt.show(block=True)
tstart = time.time()            # for profiling
resolution = 1
x = []            				# x-array

#set up dendrite plot and a function to update it
# plt.figure(1)
# dendFig = plt.subplot(511)
# somaFig = plt.subplot(512)
# sumFig = plt.subplot(513)
# totalFig = plt.subplot(514)
# fireFig = plt.subplot(515)
# dendYdata = []
# dendLine, = dendFig.plot(x, dendYdata)
# somaYdata = []
# somaLine, = somaFig.plot(x, somaYdata)
# sumYdata = []
# sumLine, = sumFig.plot(x, sumYdata)
# totalYdata = []
# totalLine, = totalFig.plot(x, totalYdata)
# firePointsX = []
# firePointsY = []
# fireLine, = fireFig.plot(firePointsX, firePointsY, marker='o', linestyle='')
# plt.show()
# counter = 0
# def updateGraphs(currentTime, speed, angle, dendLine, somaLine, sumLine, totalLine):
# 	currentTimeStep = currentTime
# 	# print("current time step: " + str(currentTimeStep))
# 	x.append(currentTimeStep)
# 	#update the frequencies
# 	prefAngle1 = 0
# 	prefAngle2 = pi/3
# 	prefAngle3 = 2*pi/3
# 	prefAngle4 = pi
# 	prefAngle5 = 4*pi/3
# 	prefAngle6 = 5*pi/3
# 	functions = []
# 	angles = [prefAngle1]
# 	for ang in angles:
# 		Wi = somaStaticFreq + speed*speedScale*cos(angle-ang)
# 		result = cos(Wi * currentTimeStep) + cos(somaStaticFreq*currentTimeStep)
# 		functions.append(result)

# 	def listProduct(l: list):
# 		result = 1
# 		if len(l) == 0:
# 			return 0
# 		for i in l:
# 			result *= i
# 		return result

# 	answer = listProduct(functions)
# 	print("ANSWER: " + str(answer))
# 	# n1 = somaStaticFreq + speed*speedScale*cos(angle-0)
# 	# n2 = somaStaticFreq + speed*speedScale*cos(angle-(2*pi/3))
# 	# n3 = somaStaticFreq + speed*speedScale*cos(angle-(4*pi/3))
# 	dendTotalFrequency = dendriteStaticFrequency + speedScale*speed*cos(pi/3 - angle)
# 	resultantFrequency = dendTotalFrequency - somaStaticFreq
# 	# resultantFrequency = somaStaticFreq + somaStaticFreq*speed*cos(angle)
# 	print("average distance: " + str(speed * cos(angle) / resultantFrequency))
# 	# print("resultantFrequency " + str(resultantFrequency) + "   " + str(sin(2*pi*currentTimeStep*resultantFrequency)))
# 	#update figure boundaries
# 	dendFig.axis([currentTime-4, currentTimeStep, -1, 1])
# 	somaFig.axis([currentTime-4, currentTimeStep, -1, 1])
# 	sumFig.axis([currentTime-4, currentTimeStep, -2, 2])
# 	totalFig.axis([currentTime-4, currentTimeStep, -1, 1])
# 	#update dendrite figure
# 	dendYdata.append(cos(2*pi*currentTimeStep*dendTotalFrequency))
# 	dendLine.set_data(x, dendYdata)
# 	#update soma figure
# 	somaYdata.append(cos(2*pi*currentTimeStep*somaStaticFreq))
# 	somaLine.set_data(x, somaYdata)
# 	#update sum figure
# 	sumYdata.append(cos(2*pi*currentTimeStep*somaStaticFreq) + cos(2*pi*currentTimeStep*dendTotalFrequency))
# 	sumLine.set_data(x, sumYdata)
# 	#update total figure
# 	# print(sin(2*pi*currentTimeStep*resultantFrequency))
# 	print(resultantFrequency)
# 	print(cos(2*pi*currentTimeStep*resultantFrequency))
# 	totalYdata.append(cos(2*pi*currentTimeStep*resultantFrequency))
# 	totalLine.set_data(x, totalYdata)
# 	#update fire line 
# 	firePointsX.append(currentTimeStep*resolution)
# 	fire = False
# 	if cos(2*pi*currentTimeStep*resultantFrequency) > threshold:
# 		firePointsY.append(1)
# 		fire = True
# 	else:
# 		firePointsY.append(0)
# 	fireLine.set_ydata(firePointsY)
# 	fireLine.set_xdata(firePointsX)

# 	fireFig.axis([currentTime-4, currentTimeStep, 0, 2])
# 	# if counter % 100 == 0:
# 		# print("x: " +  str(x))
# 		# print("dend freq: " + str(dendYdata))
# 	return fire
# 	# dendFig.clear()
# 	# plt.draw()
	

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
red = (139,0,0)
green = (0, 250, 0)
pygame.init()
FPS = 60
dWidth = 800
dHeight = 400
dDimensions = (dWidth, dHeight)
gameDisplay = pygame.display.set_mode(dDimensions)
pygame.display.set_caption('Rat Grid Cell Simulation')
clock = pygame.time.Clock()

#define rat properties and simple function(s)
# ratImage = pygame.image.load('rat.gif')
# ratImageHeight = ratImage.get_rect().height
# ratImageWidth = ratImage.get_rect().width
# 
# make rats in each colum in the cell
rats = []
j = 300
for i in range(j):
	rats.append( Rat(dWidth/2, dHeight/2, i/(j), (j-i)/(j), 0.8, i))
	rats.append( Rat(dWidth/2, dHeight/2, -i/(j), (j-i)/(j), 0.8, i))
	rats.append( Rat(dWidth/2, dHeight/2, i/(j), -(j-i)/(j), 0.8, i))
	rats.append( Rat(dWidth/2, dHeight/2, -i/(j), -(j-i)/(j), 0.8, i))


#define game control mechanism properties
crashed = False
isKeyPressed = False
pressedKey = None
gameTime = 0
dt = 1/FPS


gameDisplay.fill(white)
#the game loop
while not crashed:
	# counter += 1
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
			for rat in rats:
				rat.xSpeed += 1
		elif pressedKey == pygame.K_LEFT:
			for rat in rats:
				rat.xSpeed -= 1
		elif pressedKey == pygame.K_UP:
			for rat in rats:
				rat.ySpeed += 1
		elif pressedKey == pygame.K_DOWN:
			for rat in rats:
				rat.ySpeed -= 1
		elif pressedKey == pygame.K_RETURN:
			takeScreenShot(gameDisplay)
		elif pressedKey == pygame.K_d:
			drawCenterOrientation(gameDisplay, dWidth, dHeight, green)


	for rat in rats:
		rat.moveRat(gameTime)
		# print("rat at: " + str( (rat.x, rat.y)) )
		# update the display and print the event
		# print(event)

	#if rat reached a vertical edge flip the x speed
	# if((ratX >= dWidth - ratImageWidth) or (ratX <= 0)):
	# 	xSpeed = -xSpeed
	# 	# crashed = True
	# 	print("Final firing points: " + str(ratFirePoints))
	# #if rat reached a horizontal edge flip the y speed
	# if( (ratY <= (-dHeight + ratImageHeight)) or (ratY >= 0)) :
	# 	ySpeed = -ySpeed

	#testing triangular movement of rat
	# if(ratX > 600):
	# 	xSpeed = -xSpeed
	# 	ySpeed = 1
	# if(ratX < 200):
	# 	xSpeed = -xSpeed
	# 	ySpeed = 0
	# if ratY > -200:
	# 	ySpeed = - ySpeed
	#calculate the new position of the rat
	# (ratX, ratY) = calculateRatPosition(xSpeed, ratX, ySpeed, ratY)
	gameTime += 0.01
	
	# fired = updateGraphs(gameTime, speed, angle, dendLine, somaLine, sumLine, totalLine)
	# if fired:
	# 	ratFirePoints.append(pos)
	# ratTrackPoints.append(pos)

	#update the display
	# gameDisplay.fill(white)
	for rat in rats:
		rat.displayRat(gameDisplay)
	

	
	pygame.display.update()
	#run the next game step
	clock.tick(FPS)
