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
Waypoint planning
'''

decimation = 50;
safety = 10;
coast = coast - numpy.max(coast) - 80* safety;

Waypoints = OL.O_PathWayPoints(coast, coastlength, decimation, safety);

data = Waypoints.get_WayPoints();


plt.plot(coast)
plt.plot(data[1], data[0]);
'''
plt.show();
'''


'''
Local pathplanning
'''

NextWaypointNo = 4;

while NextWaypointNo<len(data[0])-1:

    CurPos = OL.O_PosData(0,0, 0,1);
    gamma = 0;
    i = -1;
    
    while gamma <= 0 or gamma >= math.pi:
        
        i = i + 1;
        
        '''Turning waypoint''' 
        n = NextWaypointNo + i; 
        
        '''Nm is to become Position in the embedded system'''
        Nm = Waypoints.get_SingleWayPoint(n - 1);
        Nt = Waypoints.get_SingleWayPoint(n);
        Np = Waypoints.get_SingleWayPoint(n + 1);
        
        gamma = FL.CosLaw(Nm, Nt, Np);
        print("gamma:");
        print(gamma/math.pi*180);
    
    
    
    Path = OL.O_LocalPath(gamma, 0.1,0.1);
    
    definition = 20;
    PathPoly = Path.FitPath(definition);
    
    
    
    P = Path.PositionPoly(Nm, Nt, Np);

    NextWaypointNo = n + 1;

plt.show();

'''
Control Procedure:
    Receive system states
    Receive path object
    Calculate necessary control signal
^---repeat
'''

