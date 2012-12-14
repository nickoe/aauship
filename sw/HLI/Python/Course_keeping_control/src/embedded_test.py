'''
Created on 2012.12.13.

@author: Fodi
'''

'''
Created on 2012.09.20.

@author: Fodi
'''

'''
#############################################
# Main Course-keeping Control
#############################################
'''

import math
import numpy
import scipy
import matplotlib.pyplot as plt

import ObjectLibrary as OL
import FunctionLibrary as FL
import Ship_nofilter as Ship
import Simulator as S
import KalmanFilter as KF
import Queue

'''
EMBEDDED STEP 1
Init AAUSHIP
'''
Startpos = OL.O_PosData(0, 0, 0, 1)
AAUSHIP = Ship.O_Ship(Startpos)

'''
EMBEDDED OPTIONAL STEP 2/B
Waypoint ADDING
'''

X = numpy.array[0,1,2,3,4,5,6,7]
Y = numpy.array[10,11,12,13,14,15,16,17]
WPC = numpy.array([X,Y])
AAUSHIP.SetWaypoints(WPC)

Q = Queue.Queue()

'''
EMBEDDED STEP 3
Set first target WP (should be 0 or 1)
'''
AAUSHIP.FlushPath(1)

'''
EMBEDDED STEP 5
Control loop
'''
while 1:
    
    '''Force ant torque control'''
    motor = AAUSHIP.Control_Step()
    AAUSHIP.ReadStates(measurement_matrix, motor)
    tosend = AAUSHIP.FtoM(motor)

'''
End of voyage
'''

