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
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

controller = Controller()
lines = []
programState = 0

# clf = pickle.load( open('userData/classifier.p','rb') )
# testData = np.zeros((1,30),dtype='f')


matplotlib.interactive(True)
fig = plt.figure( figsize=(16,6) )
ax = fig.add_subplot ( 121, projection ='3d')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000)
ax.set_zlim(0,1000)
ax.view_init(azim=90)
# image_file = cbook.get_sample_data('s.png')
# image = plt.imread(image_file,0)
# ax1 = fig.add_subplot (122)
# ax1.imshow(image)
# ax1.axis('off')


# def CenterData(testData):
#     alltestDataCoordinates = testData[0,::3]
#     meanValue = alltestDataCoordinates.mean()
#     testData[0,::3] = alltestDataCoordinates - meanValue
#     
#     allyCoordinates = testData[0,1::3]
#     meanValue = allyCoordinates.mean()
#     testData[0,1::3] = allyCoordinates - meanValue
#     
#     allzCoordinates = testData[0,2::3]
#     meanValue = allzCoordinates.mean()
#     testData[0,2::3] = allzCoordinates - meanValue
#     
#     return testData

def DrawImageToHelpUserPutTheirHandOverTheDevice():
    image_file = cbook.get_sample_data('s.png')
    image = plt.imread(image_file,0)
    # fig, ax = plt.subplots()
    ax1 = fig.add_subplot (122)
    ax1.imshow(image)
    ax1.axis('off')
  
# def HandOverDevice():
#     if len(frame.hands) > 0:
#         return True
#     else:
#         return False
# 
# def HandleState0():
#     DrawImageToHelpUserPutTheirHandOverTheDevice()
#     global programState
#     if HandOverDevice():
#         programState = 1
#         
# def HandleState1():
#     global programState     
#     if not HandOverDevice():
#         programState = 0

# num = random.randint(0,9)
# print num

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
                
                
                # if((j==0)|(j==3)):
                #     testData[0,k] = xTip
                #     testData[0,k+1] = yTip
                #     testData[0,k+2] = zTip
                #     k = k + 3
        # print testData
        # testData = CenterData(testData)
        # predictedClass = clf.predict(testData)
        # print predictedClass
        plt.pause(0.00001)
        while (len(lines) > 0 ):
            In = lines.pop()
            In.pop(0).remove()
            del In
            In = []
        # while(True):
        #     if programState == 0:
        #         HandleState0()
        #     elif programState == 0:
        #         HandleState1()
        while(True):
            if len(frame.hands) == 0:
                DrawImageToHelpUserPutTheirHandOverTheDevice()

