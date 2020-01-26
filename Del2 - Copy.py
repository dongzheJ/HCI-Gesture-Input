# -*- coding: utf-8 -*-
# import globalVariables as gv
# from Leap import *
# import random
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib

import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

controller = Leap.Controller()
lines = []

matplotlib.interactive(True)
fig = plt.figure( figsize=(8,6) )
ax = fig.add_subplot ( 111, projection ='3d')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000)
ax.set_zlim(0,1000)
ax.view_init(azim=90)

for i in range(1,200):
    frame = controller.frame()
    if(len(frame.hands) > 0):  
        hand = frame.hands[0]
                
        for i in range(0,5):
            finger = hand.fingers[i]
            for j in range(0,3):
                bone = finger.bone(j)
                boneBase = bone.prev_joint
                boneTip = bone.next_joint 

                xBase = boneBase.x
                yBase = boneBase.y
                zBase = boneBase.z
                xTip = boneTip.x
                yTip = boneTip.y
                zTip = boneTip.z       
                
                lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r',color = 'g'))
        plt.pause(0.00001)
        while (len(lines) > 0 ):
            In = lines.pop()
            In.pop(0).remove()
            del In
            In = []