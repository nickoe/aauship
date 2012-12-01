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

'''
SIMULATION STEP 1
Read / Generate coast, initialize simulator
'''
coastlength = 1000
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

AAUSHIP.FlushPath(3)


'''
SIMULATION STEP 3
Control loop initializations
'''
i = 0

ni = 10000
x0 = numpy.zeros(ni)
x1 = numpy.zeros(ni)
x2 = numpy.zeros(ni)

'''
EMBEDDED STEP 4
Sensor initializations
'''

AAUSHIP.ReadStates(0, 0, 0, Startpos.get_Pos())

'''
EMBEDDED STEP 5
Control loop
'''

while i < ni:
    '''Force ant torque control'''
    motor = AAUSHIP.Control_Step()
    '''Update of the simulated ship states'''
    states = Sim.UpdateStates(motor)
    '''Acquiring ship coordinates / Calculating coordinates in simulation'''
    pos = Sim.UpdatePos(states)
    '''Logging'''
    x0[i] = pos[0]
    x1[i] = pos[1]
    x2[i] = states[0]
    i += 1
    '''Sensor reading'''
    AAUSHIP.ReadStates(numpy.sum(states[0]), numpy.sum(states[1]), numpy.sum(states[2]), pos)
    
'''
End of voyage
'''
    
plt.plot(x0,x1)
plt.show()
plt.plot(x2)
plt.show()

