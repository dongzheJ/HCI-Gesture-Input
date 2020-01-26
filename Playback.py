import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
class Reader:
    def __init__(self):
        self.numberOfGesturesSaved = 5

        self.lines = []
        matplotlib.interactive(True)
        self.fig = plt.figure(figsize=(8,6))
        self.ax = self.fig.add_subplot ( 111, projection ='3d')
        self.ax.set_xlim(-1000,1000)
        self.ax.set_ylim(-1000,1000)
        self.ax.set_zlim(0,1000)
        self.ax.view_init(azim=90)

        
        # fileName = 'userData/gesture.dat'
        # f = open(fileName,'r')
        # self.gestureData = np.load(f)
        # f.close()
        
        #self.numberOfGesturesSaved = np.fromfile('userData/numOfGestures.dat',dtype = float)
        # userData/gesture'+ str(i) + '.dat
    
    def PrintGesture(self,i):
        fileName = 'userData/gesture'+ str(i) + '.dat'
        f = open(fileName,'rb')
        gestureData = np.load(f)
        f.close()
        
        # gestureData = np.fromfile('userData/gesture'+ str(i) + '.dat')
        # print gestureData
        
        for i in range(0,5):
            for j in range(0,4):
                xBase = gestureData[i,j,0]
                yBase = gestureData[i,j,1]
                zBase = gestureData[i,j,2]
                xTip = gestureData[i,j,3]
                yTip = gestureData[i,j,4]
                zTip = gestureData[i,j,5]
                self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'b'))
        plt.pause(0.5)
        while (len(self.lines) > 0 ):
            In = self.lines.pop()
            In.pop(0).remove()
            del In
            In = []
    def PrintData(self):
        for i in range(1,self.numberOfGesturesSaved):
            self.PrintGesture(i)
            
    def RunForever(self):
        while(True):
            self.PrintData()
reader = Reader()
reader.RunForever()
