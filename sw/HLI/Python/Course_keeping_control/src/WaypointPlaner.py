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
Read / Generate coast
'''
coastlength = 1000
Sim = S.Simulator()

coast = Sim.SimulateCoast(coastlength)
startpos = OL.O_PosData(0, 0, 0, 1)
Sim.SetDynamicModel(1, 1, 1, 1, 1, startpos)

'''
Init AAUSHIP
'''

AAUSHIP = Ship.O_Ship(OL.O_PosData(0, 0, 1, 0))


'''
Waypoint planning
'''

decimation = 50
safety = 10
coast = coast - numpy.max(coast) - 10* safety

AAUSHIP.Plan_WP(coast, decimation, safety)

X = scipy.rand(100)*100
Y = scipy.rand(100)*100
WPC = numpy.array([X,Y])

AAUSHIP.SetWaypoints(WPC)

plt.plot(coast)
plt.axes().set_aspect('equal')

AAUSHIP.FlushPath(6)

i = 0

ni = 10000
x0 = numpy.zeros(ni)
x1 = numpy.zeros(ni)
x2 = numpy.zeros(ni)


while i < ni:
    
    motor = AAUSHIP.Control_Step()
    states = Sim.UpdateStates(motor)
    pos = Sim.UpdatePos(states)
    x0[i] = pos[0]
    x1[i] = pos[1]
    #x2[i] = results[2]
    #print(i)
    i += 1
    #print('i:', i)
    AAUSHIP.ReadStates(numpy.sum(states[0]), numpy.sum(states[1]), numpy.sum(states[2]), pos)
    
plt.plot(x0,x1)


#plt.plot(x2)
#plt.axes().set_aspect('equal');
plt.show()

'''
Control Procedure:
    Receive system states
    Receive path object
    Calculate necessary control signal
^---repeat
'''

