'''
Created on 2012.09.25.

@author: Fodi
'''

'''
#############################################
# Object Library for ASV HLI
#
# Contains all of the lesser Objects
#############################################
'''

import math
import numpy
import scipy
import scipy.special
#import control
import matplotlib.pyplot as plt


import OsmApi as Osm

import FunctionLibrary as FL


'''
#############################################
# Local Smooth Path Object
#############################################
'''

class O_LocalPath:
    def __init__(self, gamma, sigma_max, kappa_max):
        
        '''
        Initializes the Object with the required path parameters, like
        R_min := minimum turning radius
        Kappa := Path curvature
        Sigma = Beta/v^2 := Curve proportional size, max change of angular velocity / velocity^2
        
        phi_max := maximum turning angle with Euler spirals only
        '''
        
        phi = math.pi/2 - gamma/2;
        self.phi = phi;
        R_min=1/kappa_max;
        kappa = kappa_max
        sigma = sigma_max;

        phi_max = math.pow(kappa,2) / (2*sigma);
        
        '''
        Calculate parameters in local base
        '''
        
        if phi == 0:
            '''
            If phi <= 0 the path is straight
            '''
            self.PathPoly = numpy.zeros(5);
            self.error = 'StraightPath';
            self.Range = 0;
            print('Straight path');
        
        elif phi == math.pi/2:
            '''
            If phi >= pi/2 the path is a complete turnaround
            '''
            self.PathPoly = numpy.zeros(5);
            self.error = 'TurnAround';
            self.Range = 0;
        
        elif phi > phi_max:
            '''
            The steepness of the curve requires a circular path component
            '''

            tlen = 2
            
            t = numpy.linspace(0.,tlen, 1000);
            ax = numpy.linspace(0.,tlen, 1000);
            ay = numpy.linspace(0.,tlen, 1000);
            j = 0;
            
            for i in t:
                b = scipy.special.fresnel(i);
                ay[j] = b[0];
                ax[j] = b[1];
                if j > 2 and math.atan((ay[j-1]-ay[j-2])/(ax[j-1]-ax[j-2])) >= phi_max:
                    break;
                j = j+1;
            
            '''
            Parameters of the Euler-spiral
            '''
            xd = math.sqrt(math.pi / sigma) * ax[j];
            yd = math.sqrt(math.pi / sigma) * ay[j];
            
            '''
            Calculating key points
            '''
            XR = R_min * math.sin(phi - phi_max);
            Px = XR + yd * math.sin(phi);
            X1 = Px + xd * math.cos(phi);
            Y1 = X1 * math.tan(phi);
            Py = Y1 - xd * math.sin(phi);
            Y2 = Py + yd * math.cos(phi);
            Oy = R_min * math.cos(phi-phi_max) + Y2;
            YR = Oy - R_min;
            X2 = XR;
            
            
            A = numpy.array([-X1,Y1]);
            B = numpy.array([-X2,Y2]);
            C = numpy.array([0,YR]);
            D = numpy.array([X2,Y2]);
            E = numpy.array([X1,Y1]);
            
            '''
            Point-structure
            '''
            self.PointStore_Y = numpy.array([Y1,Y2,YR,Y2,Y1]);
            self.PointStore_X = numpy.array([-X1,-X2,0,X2,X1]);
            
            '''
            The distance from the waypoint where the Euler path starts 
            '''
            self.Range = math.sqrt(math.pow(A[0], 2) + math.pow(A[1], 2));
            
            self.error = 'None';
          
            
        elif phi<=phi_max:
            '''
            The steepness of the curve doesn't requires a circular path component
            '''
            tlen = 2
            
            t = numpy.linspace(0.,tlen, 1000);
            ax = numpy.linspace(0.,tlen, 1000);
            ay = numpy.linspace(0.,tlen, 1000);
            j = 0;
            
            for i in t:
                b = scipy.special.fresnel(i);
                ay[j] = b[0];
                ax[j] = b[1];
                if j > 2 and math.atan((ay[j-1]-ay[j-2])/(ax[j-1]-ax[j-2])) >= phi:
                    break;
                j = j+1;
                
            '''
            Parameters of the Euler-spiral
            '''
            xd = math.sqrt(math.pi / sigma) * ax[j];
            yd = math.sqrt(math.pi / sigma) * ay[j];
            
            '''
            Calculating key points
            '''
            X1 = xd * math.cos(phi) + yd * math.sin(phi);
            Y1 = X1 * math.tan(phi);
            
            A = numpy.array([-X1,Y1]);
            C = numpy.array([0,yd/math.cos(phi)]);
            E = numpy.array([X1,Y1]);
            B = C;
            D = C;
            
            '''
            Point-structure
            '''
            self.PointStore_X = numpy.array([A[0],B[0],C[0],D[0],E[0]]);
            self.PointStore_Y = numpy.array([A[1],B[1],C[1],D[1],E[1]]);
            
            '''
            The distance from the waypoint where the Euler path starts 
            '''
            self.Range = math.sqrt(math.pow(A[0], 2) + math.pow(A[1], 2));
            
            
            self.error = 'None';
            
        else:
            '''
            If none of the previous conditions have been met phi has an invalid value
            '''
            self.PathPoly = numpy.zeros(5);
            self.PointStore_X = numpy.zeros(5);
            self.PointStore_X = numpy.zeros(5);
            self.error = 'NoValidPath';
            self.Range = 0;
            print('No path');
            
    def get_PathPoly(self):
        '''
        Returns the calculated Path Polynom
        '''
        return(self.PathPoly)
    
    def get_Range(self):
        '''
        Returns the Range of the turn
        The Range is the distance from the turning waypoint,
        where the path must begin to bend 
        '''
        return(self.Range)
    
    def PositionPoly(self, p_Nm, p_Nt, p_Np):
        '''
        Based on the coordinates of Start, Turn and End points,
        the method rotates and shifts of the turn-path coordinates
        to their correct positions
        '''
        Nm = p_Nm.get_Pos();
        Nt = p_Nt.get_Pos();
        Np = p_Np.get_Pos();
        '''
        Calculating the required angle of the path
        '''
        v0 = (Nm-Nt) / numpy.linalg.norm(Nt-Nm);
        v1 = (Np-Nt) / numpy.linalg.norm(Np-Nt);
        
        v = v0 + v1;
        
        rot = math.atan2(-v[0], v[1]);
        
        radius = numpy.sqrt(numpy.power(self.PathPoly[0],2) + numpy.power(self.PathPoly[1], 2));

        angle = numpy.arctan2(self.PathPoly[1], self.PathPoly[0]);

        P_X = radius * numpy.cos(angle + rot);
        P_Y = radius * numpy.sin(angle + rot);
        
        PP_Y = P_X + Nt[0];
        PP_X = P_Y + Nt[1];

        self.TurnSWP = numpy.zeros(numpy.shape(self.PathPoly));
        self.TurnSWP[0] = PP_X;
        self.TurnSWP[1] = PP_Y;
        '''
        Returns the modified points
        '''
        return self.TurnSWP;
        
    def FitPath(self, definition):
        '''
        Fits a Hermite-polynom to the
        3 or 5 key-points of the initial path.
        This step is required, because the Spiral-Arc-Spiral
        path can not be described in a closed formula.
        The method populates the line with a predefined
        (definition) number of points along the path.
        
        Returns a list of points, which will be passed to
        the PositionPoly function later.
        '''
        
        Poly_X = self.PointStore_X;
        Poly_Y = self.PointStore_Y;

        
        Poly = numpy.polynomial.hermite.hermfit(Poly_X, Poly_Y, 4);

        Path_X = numpy.linspace(Poly_X[0],Poly_X[4], definition);
        Pathline = numpy.polynomial.hermite.hermval(Path_X, Poly);
        
        self.PathPoly = numpy.zeros([2,definition])
        self.PathPoly[0] = Path_X;
        self.PathPoly[1] = Pathline;
        
        return self.PathPoly;
    
    def PlotTurn(self, color = 'k'):
        '''
        Plots the points of the turn.
        Should not be used under normal circumstances.
        '''        
        plt.plot(self.TurnSWP[0], self.TurnSWP[1], color);
    
'''        
#############################################
# Path Waypoints Object
#############################################
'''        
class O_PathWayPoints:
    def __init__(self):
        self.WayPoints = 0
        
    def SetWP(self, WPC):
        
        self.WayPoints = WPC
        
    def AddWP(self, WPC):
        
        self.WayPoints = numpy.append(self.WayPoints, WPC, 1)
        
    def PlanWP(self, coast, coastlength, decimation, safety):
        '''
        Plans the waypoints based on a known coastline
        '''
        i = 0;
        j = 2;
        self.LowerWayPoints = scipy.zeros((2, scipy.ceil(coastlength/decimation)))
        
        while j < scipy.floor(coastlength/decimation)-1:
            
            i = j;
            
            reach = numpy.max(coast[decimation * i - safety : decimation * i + decimation + safety]) + safety
            self.LowerWayPoints[0, i] = reach;
            self.LowerWayPoints[0, i+1] = reach;
            self.LowerWayPoints[1, i] = i*decimation;
            self.LowerWayPoints[1, i+1] = (i+1) * decimation;
            j = i+2;
        
        self.UpperWayPoints = self.LowerWayPoints
        #self.UpperWayPoints[0,:] = numpy.zeros(scipy.ceil(coastlength/decimation));
        self.UpperWayPoints[1,:] = self.LowerWayPoints[1, :]
        
        self.WayPoints = scipy.zeros((2, scipy.ceil(coastlength/decimation)*2))
        
        j = 0;
        
        while j < scipy.ceil(coastlength/decimation):
            i = j * 2;
            self.WayPoints[0, i] = 0
            self.WayPoints[0, i+1] = self.LowerWayPoints[0, j];
            self.WayPoints[0, i+2] = self.LowerWayPoints[0, j+1];
            self.WayPoints[0, i+3] = 0
            self.WayPoints[1, i] = self.UpperWayPoints[1, j]
            self.WayPoints[1, i+1] = self.LowerWayPoints[1, j];
            self.WayPoints[1, i+2] = self.LowerWayPoints[1, j+1];
            self.WayPoints[1, i+3] = self.UpperWayPoints[1, j+1]
            j = j+2;
        
    def get_WayPoints(self):
        return self.WayPoints;
    
    def get_SingleWayPoint(self, no):
        
        return O_PosData(self.WayPoints[0, no], self.WayPoints[1, no], float('NaN'), float('NAN'));

            


'''
#############################################
# Euler Spiral Data Object - to save CPU time
#############################################
''' 
class O_EulerSpiral:
    '''
    An implementation of the Euler-spiral generation, but numpy has
    a better function for it.
    This class is not used anymore
    ''' 
    def __init__(self, S, C, O_X, O_Y):
        self.S = S;
        self.C = C;
        self.O_X = O_X;
        self.O_Y = O_Y;
        
    def get_Euler_Y(self):
        return self.S;
    
    def get_Euler_X(self):
        return self.C;
    
    def get_EulerO_X(self):
        return self.O_X;
    
    def get_EulerO_Y(self):
        return self.O_Y;
    
    def draw_Euler_Spiral(self):
        plt.plot(self.C,self.S);
        plt.show();
        plt.plot(self.O_X);
        plt.plot(self.O_Y);
        plt.show();

'''
#############################################
# System Position Object - Easy handling
#############################################
'''    
class O_PosData:
    """
    Contains a position and an orientation (optional)
    The purpose is to have all the points in an object type
    so methods that expect Positions will not accept anything else
    """
    def __init__(self, X, Y, O_X, O_Y):

        self.X = X;
        self.Y = Y;
        self.O_X = O_X / math.sqrt(math.pow(O_X,2) + math.pow(O_Y,2));
        self.O_Y = O_Y / math.sqrt(math.pow(O_X,2) + math.pow(O_Y,2));
        
    def get_Pos_X(self):
        return self.X;
    
    def get_Pos_Y(self):
        return self.Y;
    
    def get_Ori_X(self):
        return self.O_X;
    
    def get_Ori_Y(self):
        return self.O_Y;
    
    def get_Pos(self):
        return numpy.array([self.X, self.Y])
    '''
    The Extend function returns a point further in the direction of the orientation
    '''
    def Extend(self):
        return(O_PosData(self.X + 100 * self.O_X, self.Y + 100 * self.O_Y, float('NaN'), float('NaN')));
    '''
    The Extend_Zero function returns a point further in the direction of the Y axis
    '''
    def Extend_Zero(self):
        return(O_PosData(self.X + 0 , self.Y + 1, float('NaN'), float('NaN')));


'''
#############################################
# Straight line and Sub-Waypoints object
#############################################
''' 
class O_StraightPath:
    
    def __init__(self, N, Np, r, rp):
        '''
        This init method calculates the straight path
        start and end point between two turns
        '''
        self.v = N.get_Pos() - Np.get_Pos();
        self.eps = math.atan2(self.v[1], self.v[0]);
               
        A = N.get_Pos() - r * numpy.array([math.cos(self.eps), math.sin(self.eps)]);
        B = Np.get_Pos() + rp * numpy.array([math.cos(self.eps), math.sin(self.eps)]);

        self.A = O_PosData(A[0], A[1], float('NaN'), float('NaN'));
        self.B = O_PosData(B[0], B[1], float('NaN'), float('NaN'));
        
        
    def FitLine(self, definition):
        '''
        Fits a 1st order polynom (line) to the
        start and end points of a straight path,
        then populates the line with equally spaced
        points, and returns the list of points
        '''
    
        Ax = self.A.get_Pos_X();
        Ay = self.A.get_Pos_Y();
        
        Bx = self.B.get_Pos_X();
        By = self.B.get_Pos_Y();
        
        SubWP_No = numpy.linalg.norm(numpy.array([Ax-Bx,Ay-By])) * definition * 10;
        '''
        If the path is vertical, the X and Y axes must be swapped before the
        polynom fitting and populating, then switched back to return the
        proper point coordinates
        ''' 
        if abs(Ax - Bx) < 1:

            self.poly = numpy.polyfit([Ay, By], [Ax, Bx], 1);
            prange = numpy.linspace(Ay, By, SubWP_No);

            values = numpy.polyval(self.poly, prange);
            self.SubWP = numpy.array([prange, values]);
            
        else:            
            self.poly = numpy.polyfit([Ax, Bx], [Ay, By], 1);
            prange = numpy.linspace(Ax, Bx, SubWP_No);
            values = numpy.polyval(self.poly, prange);
            self.SubWP = numpy.array([values, prange]);
    
    def PlotLine(self, color):
        '''
        Plots the points of the straight path.
        Should not be used under normal circumstances.
        '''  
        plt.plot(self.SubWP[0], self.SubWP[1], color = 'k');



'''
#############################################
# OSM Way Object
# Contains a collection of points, Way ID, point coordinates
#############################################
'''  
class O_OSM_Way_Object:
    def __init__(self, node_ids, ID):
        self.node_ids = list(numpy.zeros(numpy.shape(node_ids)))
        for i in range(len(node_ids)):
            self.node_ids[i] = node_ids[i]
        self.Api = Osm.OsmApi();
        self.longitudes = numpy.zeros(numpy.shape(node_ids))
        self.latitudes = numpy.zeros(numpy.shape(node_ids))
        self.ID = ID
        
    def download_nodes(self):
        
        
        
        try:
            
            self.nodes = list(numpy.zeros(numpy.shape(self.node_ids)))
            self.nodes = self.Api.NodesGet(self.node_ids)  
            
            i = 0
            for n in range(len(self.node_ids)):
                self.longitudes[i] = self.nodes[self.node_ids[n]]['lon']
                self.latitudes[i] = self.nodes[self.node_ids[n]]['lat']
                i = i+1;
                
        
            print('Collection download')
            
        except:
            
            self.nodes = list(numpy.zeros(numpy.shape(self.node_ids)))
            i = 0
            for n in self.node_ids:
                a = self.Api.NodeGet(self.node_ids[i])
                
                self.nodes[i] = a;
                i = i+1
        
            i = 0
            while i < len(self.nodes):
                self.longitudes[i] = self.nodes[i]['lon']
                self.latitudes[i] = self.nodes[i]['lat']
                i = i+1;
                
        plt.plot(self.longitudes, self.latitudes, 'k')
        
    def get_longitudes(self):
        return self.longitudes
    
    def get_latitudes(self):
        return self.latitudes
    
    def get_ID(self):
        return self.ID;
    
    def get_NodeIDs(self):
        return(self.node_ids)
            
            
'''
#############################################
# Way breaker class
# Breaks up the OSM-defined ways to an appropriately
# sized and ordered collection of node IDs

# Returns a list of O_OSM_Way_Object Objects
#############################################
''' 
class O_WayBreaker:
    def __init__(self, length):
        self.waylength = length
        self.buffer = list();
        
    def LoadBuffer(self, NextWay):
        
        self.buffer = list()
        IDs = NextWay.nodes
        self.buffer = numpy.append(self.buffer, IDs)
        self.WayID = NextWay.id
        
        return(1)
         
    def ReturnWays(self):
        
        self.Ways = list()

        if len(self.buffer) < self.waylength:
            
            self.Ways = numpy.append(self.Ways, O_OSM_Way_Object(self.buffer, self.WayID))
            print(self.Ways)
            return(self.Ways)
        
        else:
            
            i = 0;
            while i < numpy.floor(len(self.buffer)/self.waylength):
                slice_from = i * self.waylength
                slice_to = (i+1) * self.waylength - 1
                self.Ways = numpy.append(self.Ways, O_OSM_Way_Object(self.buffer[slice_from:slice_to:1], self.WayID))

                i += 1
            
            self.buffer = list()
            
            print(self.Ways)
            
            return(self.Ways)
