# -*- coding: utf-8 -*-
import globalVariables as gv
from Leap import *
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import pickle
import numpy as np
from sklearn import neighbors, datasets


clf = pickle.load( open('userData/classifier.p','rb') )
testData = np.zeros((1,30),dtype='f')

controller = Controller()
lines = []

matplotlib.interactive(True)
fig = plt.figure( figsize=(8,6) )
ax = fig.add_subplot ( 111, projection ='3d')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000)
ax.set_zlim(0,1000)
ax.view_init(azim=90)

def CenterData(testData):
    alltestDataCoordinates = testData[0,::3]
    meanValue = alltestDataCoordinates.mean()
    testData[0,::3] = alltestDataCoordinates - meanValue
    
    allyCoordinates = testData[0,1::3]
    meanValue = allyCoordinates.mean()
    testData[0,1::3] = allyCoordinates - meanValue
    
    allzCoordinates = testData[0,2::3]
    meanValue = allzCoordinates.mean()
    testData[0,2::3] = allzCoordinates - meanValue
    
    return testData


for i in range(1,200):
    frame = controller.frame()
    if(len(frame.hands) > 0): 
        k = 0 
        hand = frame.hands[0]
        
        for i in range(0,5):
            finger = hand.fingers[i]
            for j in range(0,4):
                bone = finger.bone(j)
                boneBase = bone.prev_joint
                boneTip = bone.next_joint 

                xBase = boneBase[0]
                yBase = boneBase[1]
                zBase = boneBase[2]
                xTip = boneTip[0]
                yTip = boneTip[1]
                zTip = boneTip[2]       
                
                lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r',color = 'r'))
                
                if((j==0)|(j==3)):
                    testData[0,k] = xTip
                    testData[0,k+1] = yTip
                    testData[0,k+2] = zTip
                    k = k + 3
        # print testData
        testData = CenterData(testData)
        predictedClass = clf.predict(testData)
        print predictedClass
        
        plt.pause(0.00001)
        while (len(lines) > 0 ):
            In = lines.pop()
            In.pop(0).remove()
            del In
            In = []
            

