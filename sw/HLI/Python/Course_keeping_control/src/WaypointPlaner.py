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
#import control
#import slycot
import matplotlib.pyplot as plt

import ObjectLibrary as OL
import FunctionLibrary as FL

'''
Read / Generate coast
'''
coastlength = 10000;
coast = FL.SimulateCoast(coastlength);

'''
Init AAUSHIP
'''

AAUSHIP = OL.O_Ship(OL.O_PosData(0, 0, 1, 0));


'''
Waypoint planning
'''

decimation = 50;
safety = 10;
coast = coast - numpy.max(coast) - 10* safety;

AAUSHIP.Plan_WP(coast, decimation, safety);

plt.plot(coast);
plt.axes().set_aspect('equal');

'''
Local pathplanning
'''

NextWaypointNo = 4;
PrevRange = 0;
Range = 0;

AAUSHIP.Plan_FullPath('Plot');
#plt.show();

AAUSHIP.PlotPath('k');
plt.show()

#plt.show();
'''
AAUSHIP.LastWP = 4;
AAUSHIP.Plan_LocalPath(0)
'''
AAUSHIP.get_PathSegment()


AAUSHIP.FlushPath()

AAUSHIP.SetDynamicModel(1, 1, 1, 1, 1)
i = 0

ni = 10000
x0 = numpy.zeros(ni)
x1 = numpy.zeros(ni)
x2 = numpy.zeros(ni)


while i < ni:
    results = AAUSHIP.Control_Step()
    
    
    x0[i] = results[0]
    x1[i] = results[1]
    #x2[i] = results[2]
    #print(i)
    i += 1
    print('i:', i)

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

