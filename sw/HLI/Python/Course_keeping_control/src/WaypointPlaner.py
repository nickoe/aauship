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

AAUSHIP = OL.O_Ship(OL.O_PosData(0, 0, 0, 1));


'''
Waypoint planning
'''

decimation = 50;
safety = 10;
coast = coast - numpy.max(coast) - 10* safety;

AAUSHIP.Plan_WP(coast, decimation, safety);

plt.plot(coast);

'''
Local pathplanning
'''

NextWaypointNo = 4;
PrevRange = 0;
Range = 0;

AAUSHIP.Plan_FullPath('Plot');
#plt.show();

AAUSHIP.PlotPath('k');

#plt.show();

AAUSHIP.get_PathSegment();

'''
Control Procedure:
    Receive system states
    Receive path object
    Calculate necessary control signal
^---repeat
'''

