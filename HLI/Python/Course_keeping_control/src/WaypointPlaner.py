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
import ObjectLibrary as OL
import matplotlib.pyplot as plt



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
coastlength = 1000;
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
coast = coast - numpy.max(coast) - 10;
decimation = 20;
safety = 2
waypoints = OL.O_PathWayPoints(coast, coastlength, decimation, safety)


plt.plot(coast)
data = waypoints.get_WayPoints();
plt.plot(data[1], data[0]);

plt.show()
print(data[0])

'''
Control Procedure:
    Receive system states
    Receive path object
    Calculate necessary control signal
^---repeat
'''

