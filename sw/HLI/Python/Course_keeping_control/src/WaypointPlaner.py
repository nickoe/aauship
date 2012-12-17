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

f = open('log', 'w')

'''
SIMULATION STEP 1
Read / Generate coast, initialize simulator
'''
coastlength = 600
Sim = S.Simulator()

coast = Sim.SimulateCoast(coastlength)
startpos = OL.O_PosData(-80, -80, 1, 0)
Sim.SetDynamicModel(1, 1, 1, 1, 1, startpos)

'''
EMBEDDED STEP 1
Init AAUSHIP
'''
Startpos = OL.O_PosData(-80, -80, 0, 1)
AAUSHIP = Ship.O_Ship(Startpos, f)


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
Y = numpy.array([0,35.0543, 35.5730, 58.8078])
X = numpy.array([0, -0.5753, 26.0082, 25.5482])
plt.plot(Y,X)
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

AAUSHIP.FlushPath(-1)



'''
SIMULATION STEP 3
Control loop initializations and logging
'''
i = 0

ni = 100000
x0 = numpy.zeros(ni)
x1 = numpy.zeros(ni)
x2 = numpy.zeros(ni)
x3 = numpy.zeros(ni)
x4 = numpy.zeros(ni)
xx1 = numpy.zeros(ni+1)
xx2 = numpy.zeros(ni+1)
xx3 = numpy.zeros(ni+1)

'''
EMBEDDED STEP 4
Sensor initializations
Set return position!!!
'''

#AAUSHIP.Return(startpos)

states = numpy.matrix([[0],[0],[0]])

'''
EMBEDDED STEP 5
Control loop
'''




while i < ni:
    
    if i == 14000:
        AAUSHIP.AddCourse(OL.O_PosData(200,100,1,1))
        AAUSHIP.AddCourse(OL.O_PosData(100,100,1,1))
        #AAUSHIP.AddRelativeCourse(OL.O_PosData(0,0,1,1))
        
    if i == 24000:
        AAUSHIP.AddRelativeCourse(OL.O_PosData(10000000,0,1,1))
        AAUSHIP.AddRelativeCourse(OL.O_PosData(10000000,20000000,1,1))
        #AAUSHIP.AddRelativeCourse(OL.O_PosData(0,0,1,1))
    
    '''Force ant torque control'''
    motor = AAUSHIP.Control_Step()
    
    '''Update of the simulated ship states'''
    prevstates = states
    states = Sim.UpdateStates(motor)
    
    '''Acquiring ship coordinates / Calculating coordinates in simulation'''
    pos = Sim.UpdatePos(states)
    
    
    '''Sensor reading'''
    Theta = numpy.sum(states[1])
    Omega = numpy.sum(states[2])
    Alpha = numpy.sum(states[2]-prevstates[2])/0.1
    GPS_X = pos[0] + numpy.sum(2* scipy.randn(1))
    GPS_Y = pos[1] + numpy.sum(2* scipy.randn(1))
    Speed_X = math.sin(numpy.sum(states[1])) * numpy.sum(states[0]) + numpy.sum(0.01* scipy.randn(1))
    Speed_Y = math.cos(numpy.sum(states[1])) * numpy.sum(states[0]) + numpy.sum(0.01* scipy.randn(1))
    Acc_X = math.sin(numpy.sum(states[1])) * (numpy.sum(states[0])-numpy.sum(prevstates[0])) / 0.1
    Acc_Y = math.cos(numpy.sum(states[1])) * (numpy.sum(states[0])-numpy.sum(prevstates[0])) / 0.1
    
    
    Measured_Acc = OL.O_PosData(Acc_X, Acc_Y, 1, 1)
    BodyAcc = FL.NEDtoBody(Measured_Acc, OL.O_PosData(0,0,1,1), Theta)
    measurement_matrix = numpy.transpose(numpy.matrix(numpy.array([[GPS_X, numpy.sum(states[0]), BodyAcc[0], GPS_Y, 0, BodyAcc[1], Theta, Omega, Alpha],[1, 1, 0, 1, 1, 0, 1, 1, 1]])))
    AAUSHIP.ReadStates(measurement_matrix, motor)
    
    AAUSHIP.FtoM(motor)
    
    #print AAUSHIP.FtoM(motor)
    
    '''Logging'''
    thoughtpos = AAUSHIP.Pos.get_Pos()
    x3[i] = thoughtpos[0]
    x4[i] = thoughtpos[1]
    x0[i] = pos[0]
    x1[i] = pos[1]
    x2[i] = states[0]
    i += 1
    #print('SX', pos[0], 'SY', pos[1], 'SV', numpy.sum(states[0]), 'ST', numpy.sum(states[1]), 'SO', numpy.sum(states[2]))
    xx1[i] = numpy.sum(motor[0])/5
    xx2[i] = numpy.sum(AAUSHIP.states[2])
    xx3[i] = numpy.sum(states[0])

'''
End of voyage
'''
#plt.plot(x3,x4,'k')
plt.plot(x0,x1,'r')
plt.show()
#plt.plot(x2)


#plt.show()


plt.plot(xx3)
plt.plot(xx2)
plt.plot(xx1)
plt.show()



