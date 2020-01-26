# # -*- coding: utf-8 -*-
# 
import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
import pickle
# 
# controller = Controller()
# lines = []
# 
# matplotlib.interactive(True)
# fig = plt.figure( figsize=(8,6) )
# ax = fig.add_subplot ( 111, projection ='3d')
# ax.set_xlim(-1000,1000)
# ax.set_ylim(-1000,1000)
# ax.set_zlim(0,1000)
# ax.view_init(azim=90)

class Deliverable:
    def __init__(self):
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0 
        self.numberOfGesturesSaved = 0
        self.numberOfGestures = 1000
        self.gestureIndex = 0
        
        self.controller = Leap.Controller()
        self.lines = []
        matplotlib.interactive(True)
        self.fig = plt.figure(figsize=(8,6))
        self.ax = self.fig.add_subplot ( 111, projection ='3d')
        self.ax.set_xlim(-1000,1000)
        self.ax.set_ylim(-1000,1000)
        self.ax.set_zlim(0,1000)
        self.ax.view_init(azim=90)
        
        self.gestureData = np.zeros((5,4,6,self.numberOfGestures),dtype='f')
    
    def HandleBone(self,i,j):
        self.bones = self.finger.bone(j)
        self.boneBase = self.bones.prev_joint
        self.boneTip = self.bones.next_joint
        xBase = self.boneBase[0]
        yBase = self.boneBase[1]
        zBase = self.boneBase[2]
        xTip = self.boneTip[0]
        yTip = self.boneTip[1]
        zTip = self.boneTip[2]
        
        if ( self.currentNumberOfHands == 1 ):
            self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r',color = 'g'))
        else:
            self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))
        if ( self.currentNumberOfHands == 2 ):
            self.gestureData[i,j,0,self.gestureIndex] = xBase
            self.gestureData[i,j,1,self.gestureIndex] = yBase
            self.gestureData[i,j,2,self.gestureIndex] = zBase
            self.gestureData[i,j,3,self.gestureIndex] = xTip
            self.gestureData[i,j,4,self.gestureIndex] = yTip
            self.gestureData[i,j,5,self.gestureIndex] = zTip
            
        if(self.RecordingIsEnding()):
            self.gestureData[i,j,0] = xBase
            self.gestureData[i,j,1] = yBase
            self.gestureData[i,j,2] = zBase
            self.gestureData[i,j,3] = xTip
            self.gestureData[i,j,4] = yTip
            self.gestureData[i,j,5] = zTip
            
    def HandleFinger(self,i):
        self.finger = self.hand.fingers[i]
        for j in range(0,4):
            self.HandleBone(i,j)
    
    def RecordingIsEnding(self):
        return (self.previousNumberOfHands==2) & (self.currentNumberOfHands==1)
         
    def SaveGesture(self):
        # self.numberOfGesturesSaved = self.numberOfGesturesSaved + 1          
        fileName = 'userData/gesture.dat'
        f = open(fileName,'wb')
        pickle.dump(self.gestureData, f)
        f.close()
        # fileName = 'userData/numOfGestures.dat'
        # f = open(fileName,'w')
        # f.write(str(self.numberOfGesturesSaved))
        # f.close()
      
    def HandleHands(self):
        self.previousNumberOfHands = self.currentNumberOfHands
        self.currentNumberOfHands = len(self.frame.hands)
        
        self.hand = self.frame.hands[0]
        for i in range(0,5):
            self.HandleFinger(i)
        plt.pause(0.00001)
        while (len(self.lines) > 0 ):
            In = self.lines.pop()
            In.pop(0).remove()
            del In
            In = []
        if ( self.RecordingIsEnding() ):
            print self.gestureData[:,:,:]
            # self.SaveGesture()
        if ( self.currentNumberOfHands == 2 ):
            print 'gesture ' + str(self.gestureIndex) + ' stored.'
            self.gestureIndex = self.gestureIndex + 1
            if ( self.gestureIndex == self.numberOfGestures ):
                print self.gestureData[:,:,:,0]
                print self.gestureData[:,:,:,99]
                self.SaveGesture()
                sys.exit(0)
                
    def RunOnce(self):
        self.frame = self.controller.frame()
        if(len(self.frame.hands) > 0):  
            self.HandleHands()    

    def RunForever(self):
        while (True):
            self.RunOnce()
                    
deliverable = Deliverable()
deliverable.RunForever()