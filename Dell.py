import globalVariables as gv
from Leap import *
from pylab import *
import random
controller = Controller()
ion()
show()
xPt = 0
yPt = 0
pt, = plot(xPt, yPt, 'ko', markersize = 20)

xlim(-600,600)
ylim(-600,600)

for i in range(1,200):
    frame = controller.frame()
    # print(len(frame.hands))
    if(len(frame.hands) > -1):     
        hand = frame.hands[0]
        fingers = hand.fingers
        indexFinger = fingers.finger_type(3)
        distalPhalanx = indexFinger[0].bone(3)
        distalPhalanxPosition = distalPhalanx.next_joint
        # print distalPhalanxPosition.x
        
        x = distalPhalanxPosition.x
        if ( x < gv.xMin ):
            gv.xMin = x
        if ( x > gv.xMax ):
            gv.xMax = x
            
        y = distalPhalanxPosition.y
        if ( y < gv.yMin ):
            gv.yMin = x
        if ( y > gv.yMax ):
            gv.yMax = y
        print gv.xMin , gv.xMax , gv.yMin , gv.yMax
        
        if(distalPhalanxPosition.x != 0):
            pt.set_xdata(distalPhalanxPosition.x)
            pt.set_ydata(distalPhalanxPosition.y)
            pause(0.00001)