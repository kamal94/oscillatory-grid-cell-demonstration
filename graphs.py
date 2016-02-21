import pygame
import matplotlib.pyplot as plt
from numpy import *
import time
import os

#important constants
somaFreq = 6.42
dendriteStaticFrequency = 6.91
resultantFrequency = dendriteStaticFrequency - somaFreq
threshold = 0.80
#set up the figure
timeStart = 0
timeEnd = 4
# plt.ion()
plt.show(block=True)
tstart = time.time()            # for profiling
resolution = 0.01
x = arange(timeStart, timeEnd, resolution)            # x-array

#set up dendrite plot and a function to update it
plt.figure(1)
dendFig = plt.subplot(411)
dendLine, = dendFig.plot(x, sin(2*pi*x*dendriteStaticFrequency))
somaFig = plt.subplot(412)
somaLine = somaFig.plot(x,sin(2*pi*x*somaFreq))
totalFig = plt.subplot(413)
totalLine = totalFig.plot(x,sin(2*pi*x*resultantFrequency))
fireFig = plt.subplot(414)
firePointsX = arange(timeStart, timeEnd, resolution*10)
firePointsY = (sin(2*pi*firePointsX*resultantFrequency)>threshold).astype(int)
fireLine = fireFig.plot(firePointsX,firePointsY, marker='o', linestyle='')
plt.show()
