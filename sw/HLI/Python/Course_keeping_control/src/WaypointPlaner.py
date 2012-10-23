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
Object-oriented control based on pre-calculated controller parametes

Inputs:
    System states
    Boat position
    Path object
    
Outputs:
    Ship handling signals
'''

'''
Simulated coast-line:
'''
coastlength = 10000;
i = 0;
coast = scipy.randn(coastlength);
initial = 0;

while i < coastlength:
   
    coast[i] = initial + coast[i];
    initial = coast[i];
    i = i + 1;
    


'''
Transformations will be necessary...
'''
    

decimation = 200;
safety = 10;
coast = coast - numpy.max(coast) - 2* safety;

Waypoints = OL.O_PathWayPoints(coast, coastlength, decimation, safety);

data = Waypoints.get_WayPoints();
'''
plt.plot(coast)
plt.plot(data[1], data[0]);
plt.show();
'''

Euler = FL.fcn_GenerateEuler(2);
#Euler.draw_Euler_Spiral();

NextWaypointNo = 63;

PosData = OL.O_PosData(0,0, 0,1);

#P = OL.O_LocalPath(Waypoints, NextWaypointNo, Euler, PosData)
OL.O_LocalPath(Waypoints, 1,1)
#corr = P.get_PathPoly();

#Euler.draw_Euler_Spiral();
'''
plt.plot(corr)
plt.show()
'''

'''
Control Procedure:
    Receive system states
    Receive path object
    Calculate necessary control signal
^---repeat
'''

