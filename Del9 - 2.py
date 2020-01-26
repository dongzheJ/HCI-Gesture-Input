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
import time

controller = Controller()
lines = []
programState = 0

clf = pickle.load( open('userData/classifier.p','rb') )
testData = np.zeros((1,30),dtype='f')

database = pickle.load(open('userData/database.p','rb'))

userName = raw_input('Please enter your name: ')
if userName in database:
    print 'welcome back ' + userName + '.'
    # database[userName]['logins'] += 1
else:
    database[userName] = {}
    # database[userName]['logins'] = 1
    database[userName]['digit0attempted'] = 0
    database[userName]['digit1attempted'] = 0
    database[userName]['digit2attempted'] = 0
    database[userName]['digit3attempted'] = 0
    database[userName]['digit4attempted'] = 0
    database[userName]['digit5attempted'] = 0
    database[userName]['digit6attempted'] = 0
    database[userName]['digit7attempted'] = 0
    database[userName]['digit8attempted'] = 0
    database[userName]['digit9attempted'] = 0
    print 'welcome ' + userName + '.'

matplotlib.interactive(True)
fig = plt.figure( figsize=(16,12) )
ax = fig.add_subplot ( 223, projection ='3d')
ax.set_xlim(-1000,1000)
ax.set_ylim(-1000,1000)
ax.set_zlim(0,1000)
ax.view_init(azim=90)

ax1 = fig.add_subplot (224)
ax1.axis('off')
ax2 = fig.add_subplot (222)
ax2.axis('off')
ax3 = fig.add_subplot (221)
ax3.axis('off')

num = 0
start_time = time.clock()

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

def DrawImageToHelpUserPutTheirHandOverTheDevice():
    image_file = cbook.get_sample_data('s.png')
    image = plt.imread(image_file,0)
    ax1.imshow(image)
  
def HandOverDevice():
    if len(frame.hands) > 0:
        return True
    else:
        return False
        

def DrawRandomNumber(num):
    image_file = cbook.get_sample_data(str(num) + '.png')
    image = plt.imread(image_file,0)
    ax1.imshow(image)
    ax1.axis('off')

def HandleState0():
    DrawImageToHelpUserPutTheirHandOverTheDevice()
    ax2.clear()
    ax2.axis('off')
    image_file = cbook.get_sample_data('exit.png')
    image = plt.imread(image_file,0)
    ax2.imshow(image)
    global programState
    if HandOverDevice():
        programState = 1
        
def HandleState1():
    ax1.clear()
    ax1.axis('off')
    if xTip > 100:
        image_file = cbook.get_sample_data('gl.png')
        image = plt.imread(image_file,0)
        ax1.imshow(image)
    if xTip < -100:
        image_file = cbook.get_sample_data('gr.png')
        image = plt.imread(image_file,0)
        ax1.imshow(image)
    # if zTip > 100 or zTip < -100:
    #     image_file = cbook.get_sample_data('vertical.png')
    #     image = plt.imread(image_file,0)
    #     ax1.imshow(image)
    global programState
    if not HandOverDevice():
        programState = 0
    elif -100 < xTip < 100:
        programState = 2

def HandleState2():
    ax2.clear()
    ax2.axis('off')
    global num
    if num == 0 or num == 1 or num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7 or num == 8 or num == 9:
        DrawRandomNumber(num)  
    
    global programState,start_time

    if not HandOverDevice():
        programState = 0
    elif xTip > 100 or xTip < -100:
        programState = 1
    elif predictedClass == num:
        start_time = 0
        if num == 0 or num == 1 or num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7 or num == 8 or num == 9:
            database[userName]['digit' + str(num) + 'attempted'] += 1
        programState = 3
    elif predictedClass != num:
        programState = 4
        
def HandleState3():
    # ax1.clear()
    # ax1.axis('off')
    ax2.clear()
    ax2.axis('off')
    image_file = cbook.get_sample_data('right.png')
    image = plt.imread(image_file,0)
    ax2.imshow(image)
    
    global num,start_time
    
    elapsed_time = time.clock() - start_time
    if elapsed_time < 10 and elapsed_time > 0:
        
        image_file = cbook.get_sample_data('loading.png')
        image = plt.imread(image_file,0)
        ax3.imshow(image)
        print(elapsed_time)
        
    elif int(elapsed_time) == 10:
        num += 1
        
    global programState
    if not HandOverDevice():
        programState = 0
    elif xTip > 100 or xTip < -100:
        programState = 1
    elif predictedClass != num or int(elapsed_time) == 10:
        programState = 2

def HandleState4():
    ax2.clear()
    ax2.axis('off')
    ax3.clear()
    ax3.axis('off')
    image_file = cbook.get_sample_data('wrong.png')
    image = plt.imread(image_file,0)
    ax2.imshow(image)
    global programState, num, start_time
    if not HandOverDevice():
        programState = 0
    elif xTip > 100 or xTip < -100:
        programState = 1
    elif predictedClass != num:
        ax2.clear()
        ax2.axis('off')
    elif predictedClass == num:
        if num == 0 or num == 1 or num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7 or num == 8 or num == 9:
            database[userName]['digit' + str(num) + 'attempted'] += 1
        num += 1
        programState = 3

for i in range(1,200):
    frame = controller.frame()
            
    if(len(frame.hands) >= 0): 
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
        # print predictedClass
        
        plt.pause(0.00001)
        while (len(lines) > 0 ):
            In = lines.pop()
            In.pop(0).remove()
            del In
            In = []
        if (programState == 0):
            HandleState0()
        elif (programState == 1):
            HandleState1()
        elif (programState == 2):
            HandleState2()
        elif (programState == 3):
            HandleState3()
        elif (programState == 4):
            HandleState4()
                  
pickle.dump(database,open('userData/database.p','wb'))
print database