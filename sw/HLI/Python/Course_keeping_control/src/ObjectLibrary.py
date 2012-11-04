'''
Created on 2012.09.25.

@author: Fodi
'''

'''
#############################################
# Object Library for ASV HLI
#############################################
'''

import math
import numpy
import scipy
import control
import matplotlib.pyplot as plt

import FunctionLibrary as FL


'''
#############################################
# Local Smooth Path Object
#############################################
'''

class O_LocalPath:
    def __init__(self, gamma, sigma_max, kappa_max):
        
        
        
        phi = math.pi/2 - gamma/2;
        self.phi = phi;
        R_min=1/kappa_max;
        Psi_max=math.pow(kappa_max,2)/2/sigma_max;
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
        
        return(self.PathPoly)
    
    def get_Range(self):
        
        return(self.Range)
    
    def PositionPoly(self, p_Nm, p_Nt, p_Np):
        
        Nm = p_Nm.get_Pos();
        Nt = p_Nt.get_Pos();
        Np = p_Np.get_Pos();
        
        v0 = (Nm-Nt) / numpy.linalg.norm(Nt-Nm);
        v1 = (Np-Nt) / numpy.linalg.norm(Np-Nt);
        
        v = v0 + v1;
        
        
        
        rot = math.atan2(-v[0], v[1]);

        print('Path rotation:');
        #print(rot/math.pi * 180);
        print(scipy.sign(v[1]));
        
        radius = numpy.sqrt(numpy.power(self.PathPoly[0],2) + numpy.power(self.PathPoly[1], 2));

        angle = numpy.arctan2(self.PathPoly[1], self.PathPoly[0]);

        P_X = radius * numpy.cos(angle + rot);
        P_Y = radius * numpy.sin(angle + rot);
        
        PP_Y = P_X + Nt[0];
        PP_X = P_Y + Nt[1];

        self.TurnSWP = numpy.zeros(numpy.shape(self.PathPoly));
        self.TurnSWP[0] = PP_X;
        self.TurnSWP[1] = PP_Y;
        
        return self.TurnSWP;
        
    def FitPath(self, definition):
        
        Poly_X = self.PointStore_X;
        Poly_Y = self.PointStore_Y;

        
        Poly = numpy.polynomial.hermite.hermfit(Poly_X, Poly_Y, 4);

        Path_X = numpy.linspace(Poly_X[0],Poly_X[4], definition);
        Pathline = numpy.polynomial.hermite.hermval(Path_X, Poly);
        
        self.PathPoly = numpy.zeros([2,definition])
        self.PathPoly[0] = Path_X;
        self.PathPoly[1] = Pathline;
        
        return self.PathPoly;
 
       
        plt.show();
        

        return self.TurnSWP;
    
    def PlotTurn(self, color = 'k'):
        
        plt.plot(self.TurnSWP[0], self.TurnSWP[1], color);
    
'''        
#############################################
# Path Waypoints Object
#############################################
'''        
class O_PathWayPoints:
    def __init__(self, coast, coastlength, decimation, safety):
        
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
        
        self.UpperWayPoints = self.LowerWayPoints;
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
            self.WayPoints[1, i] = self.UpperWayPoints[1, j];
            self.WayPoints[1, i+1] = self.LowerWayPoints[1, j];
            self.WayPoints[1, i+2] = self.LowerWayPoints[1, j+1];
            self.WayPoints[1, i+3] = self.UpperWayPoints[1, j+1];
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
    
    def Extend(self):
        return(O_PosData(self.X + self.O_X, self.Y + self.O_Y));


'''
#############################################
# Straight line and Sub-Waypoints object
#############################################
''' 
class O_StraightPath:
    
    def __init__(self, N, Np, r, rp):
        
        self.v = N.get_Pos() - Np.get_Pos();
        self.eps = math.atan2(self.v[1], self.v[0]);
        
        
        A = N.get_Pos() - r * numpy.array([math.cos(self.eps), math.sin(self.eps)]);
        B = Np.get_Pos() + rp * numpy.array([math.cos(self.eps), math.sin(self.eps)]);
        
        self.A = O_PosData(A[0], A[1], float('NaN'), float('NaN'));
        self.B = O_PosData(B[0], B[1], float('NaN'), float('NaN'));
        
        
    def FitLine(self, definition):
    
        Ax = self.A.get_Pos_X();
        Ay = self.A.get_Pos_Y();
        
        Bx = self.B.get_Pos_X();
        By = self.B.get_Pos_Y();
        
        SubWP_No = numpy.linalg.norm(numpy.array([Ax-Bx,Bx-By])) * definition;
        
        if Ax == Bx:
            self.poly = numpy.polyfit([Ay, By], [Ax, Bx], 1);
            prange = numpy.linspace(Ay, By, SubWP_No);
            values = numpy.polyval(self.poly, prange);
            self.SubWP = numpy.array([prange, values]);
            
        else:
            self.poly = numpy.polyfit([Ax, Bx], [Ay, By], 1);
            prange = numpy.linspace(Ax, Bx, SubWP_No);
            values = numpy.polyval(self.poly, prange);
            self.SubWP = numpy.array([values, prange]);
        
        return self.SubWP;
    
    def PlotLine(self, color):
        
        plt.plot(self.SubWP[0], self.SubWP[1], color = 'k');

'''
#############################################
# General Ship class
# Contains all the known information
#############################################
'''   
class O_Ship:
    def __init__(self, init_position):
        self.Pos = init_position;
        self.Speed = 0;
        self.Sigma_max = 0.1;
        self.Kappa_max = 0.1;
        
        self.LastWP = 3;
        self.SWP = 0;
        self.SegmentCoords = 0;
        self.Current_SWP = 0;
        
        self.NextSWP_No = 0;
        self.NextSWP_validity = 0;
    
    def Plan_WP(self, coastline, decimation, safety):
        
        self.Waypoints = O_PathWayPoints(coastline, len(coastline), decimation, safety);
        
    def Plan_FullPath(self, plotit = 0):
        
        PrevRange = 0;
        i = 0;
        data = self.Waypoints.get_WayPoints();
        FullPathLength = len(data[0]) - self.LastWP;
        self.Lines = numpy.zeros(FullPathLength);
        self.Turns = numpy.zeros(FullPathLength);
        
        while i < FullPathLength:
            skip = self.Plan_LocalPath(PrevRange);
            
            if skip == 'Path ended':
                print('The coast-information is missing, no further path can be calculated');
                break;
            
            if plotit == 'Plot':
                self.PlotPath('k');
        
            PrevRange = self.Path.Range;
            i = i + 1;
            self.LastWP = self.LastWP + skip;
        
    def Plan_LocalPath(self, PrevRange):
        
        if self.SegmentCoords:
            self.Current_SWP = self.SegmentCoords;
            
        self.NextSWP_No = 0;
        self.NextSWP_validity = 0;
        
        gamma = 0;
        i = 0;
        
        while gamma <= 0 or gamma >= math.pi:
        
            i = i + 1;
            
            '''Turning waypoint''' 
            n = self.LastWP + 1 + i; 
            
            try:
                Nm = self.Waypoints.get_SingleWayPoint(n - i);
                Nt = self.Waypoints.get_SingleWayPoint(n);
                Np = self.Waypoints.get_SingleWayPoint(n + 1);
            except IndexError:
                return('Path ended');
            
            
            
            gamma = FL.CosLaw(Nm, Nt, Np);
            
        print(n);
        
        self.Path = O_LocalPath(gamma, self.Sigma_max, self.Kappa_max);
        
        definition = 20;
        self.Path.FitPath(definition);
        self.Path.PositionPoly(Nm, Nt, Np);

        '''fitline'''
        Range = self.Path.get_Range();
        self.Straight = O_StraightPath(Nt, Nm, Range, PrevRange);
        self.Straight.FitLine(0.1);
        
        return i;
    
    def get_PathSegment(self):
        self.SegmentCoords = numpy.append(self.Path.TurnSWP, self.Straight.SubWP, 1);
        plt.plot(self.SegmentCoords[0], self.SegmentCoords[1], 'r')
        
        plt.show();
        
    def get_Line(self):
        return(self.Straight);
    
    def get_Turn(self):
        return(self.Path);
    
    def PlotPath(self, color):
        self.Path.PlotTurn(color);
        self.Straight.PlotLine(color);
        
    def Control_Step(self):
        
        
        while self.NextSWP_validity == 0:
            
            try:
                NextSWP = O_PosData(self.SegmentCoords[0, self.NextSWP_No], self.SegmentCoords[0, self.NextSWP_No]);
            except IndexError:
                '''End of LocalPath'''
                self.LastWP = self.LastWP + 1;
                self.Plan_LocalPath(self.Path.Range);
                
            delta = FL.CosLaw(self.Pos.Extend, self.Pos, NextSWP);
            valid = self.CheckReach(delta, NextSWP) and (FL.Distance(self.Pos, NextSWP) > self.FollowDistance);
            self.NextSWP_No = self.NextSWP_No + 1;
            
        '''
        #############################################
        # RUN CONTROL ALGORITHM FOR DELTA HERE
        #############################################
        '''
            
        results = 1; '''Results of the control step'''
        
        return results;

    def CheckReach(self, delta, P):
        
        beta = math.pi/2 - delta;
        alpha = 2* delta;
        dist = FL.Distance(self.Pos, P);
        R_min = 1/self.Kappa_max;
        
        return(dist * math.sin(beta) > R_min * math.sin(alpha));
            
        
        