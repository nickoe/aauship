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
import Ship
import Simulator as S
import KalmanFilter as KF

'''
SIMULATION STEP 1
Read / Generate coast, initialize simulator
'''
coastlength = 200
Sim = S.Simulator()

coast = Sim.SimulateCoast(coastlength)
startpos = OL.O_PosData(0, 0, 0, 1)
Sim.SetDynamicModel(1, 1, 1, 1, 1, startpos)

'''
EMBEDDED STEP 1
Init AAUSHIP
'''
Startpos = OL.O_PosData(0, 0, 1, 0)
AAUSHIP = Ship.O_Ship(Startpos)


'''
EMBEDDED OPTIONAL STEP 2/A
Waypoint planning
'''

decimation = 20
safety = 10
coast = coast - numpy.max(coast) - 10* safety

AAUSHIP.Plan_WP(coast, decimation, safety)

'''
EMBEDDED OPTIONAL STEP 2/B
Waypoint ADDING
'''
'''
X = scipy.rand(100)*100
Y = scipy.rand(100)*100
WPC = numpy.array([X,Y])
AAUSHIP.SetWaypoints(WPC)
'''

'''
NON-CRITICAL SIMULATION STEP 2
'''
plt.plot(coast)
plt.axes().set_aspect('equal')

'''
EMBEDDED STEP 3
Set first target WP (should be 0 or 1)
'''

AAUSHIP.FlushPath(2)



'''
SIMULATION STEP 3
Control loop initializations
'''
i = 0

ni = 10000
x0 = numpy.zeros(ni)
x1 = numpy.zeros(ni)
x2 = numpy.zeros(ni)
x3 = numpy.zeros(ni)
x4 = numpy.zeros(ni)
xx1 = numpy.zeros(ni)
xx2 = numpy.zeros(ni)
xx3 = numpy.zeros(ni)

'''
EMBEDDED STEP 4
Sensor initializations
'''

AAUSHIP.ReadStates(0, 0, 0, 0, 0, 0, 0, 0, 0, numpy.matrix([[0],[0]]))
states = numpy.matrix([[0],[0],[0]])

'''
EMBEDDED STEP 5
Control loop
'''




while i < ni:
    '''Force ant torque control'''
    motor = AAUSHIP.Control_Step()
    '''Update of the simulated ship states'''
    prevstates = states
    states = Sim.UpdateStates(motor)
    '''Acquiring ship coordinates / Calculating coordinates in simulation'''
    pos = Sim.UpdatePos(states)
    '''Logging'''
    thoughtpos = AAUSHIP.Pos.get_Pos()
    x3[i] = thoughtpos[0]
    x4[i] = thoughtpos[1]
    x0[i] = pos[0]
    x1[i] = pos[1]
    x2[i] = states[0]
    xx1[i] = numpy.sum(AAUSHIP.x[0])
    xx2[i] = numpy.sum(AAUSHIP.states[1])
    xx3[i] = numpy.sum(AAUSHIP.states[0])
    i += 1
    print('SX', pos[0], 'SY', pos[1], 'SV', numpy.sum(states[0]), 'ST', numpy.sum(states[1]), 'SO', numpy.sum(states[2]))
    '''Sensor reading'''
    Theta = numpy.sum(states[1])
    Omega = numpy.sum(states[2])
    Alpha = numpy.sum(states[2]-prevstates[2])*0.1
    GPS_X = pos[0]
    GPS_Y = pos[1]
    Speed_X = math.sin(numpy.sum(states[1])) * numpy.sum(states[0])
    Speed_Y = math.cos(numpy.sum(states[1])) * numpy.sum(states[0])
    Acc_X = math.sin(numpy.sum(states[1])) * (numpy.sum(states[0])-numpy.sum(prevstates[0])) * 0.1
    Acc_Y = math.cos(numpy.sum(states[1])) * (numpy.sum(states[0])-numpy.sum(prevstates[0])) * 0.1
    
   
    #AAUSHIP.ReadStates(pos[0],numpy.sum(states[0]), numpy.sum(states[0])-numpy.sum(prevstates[0]), pos[1], 0, 0, numpy.sum(states[1])+math.pi*2, numpy.sum(states[2]), numpy.sum(states[2])-numpy.sum(prevstates[2]), motor) 
    AAUSHIP.ReadStates(GPS_X, Speed_X, Acc_X, GPS_Y, Speed_Y, Acc_Y, Theta, Omega, Alpha, motor)

'''
End of voyage
'''

plt.plot(x0,x1,'r')
plt.plot(x3,x4,'k')
plt.show()
plt.plot(x2)
plt.plot(xx1)
plt.show()
plt.plot(xx2)
plt.plot(xx3)
plt.show()

