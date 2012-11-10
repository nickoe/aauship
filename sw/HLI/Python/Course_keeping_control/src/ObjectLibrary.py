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
import xml.etree.ElementTree as xml
import pickle


import OsmApi as Osm

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
        return(O_PosData(self.X + 100 * self.O_X, self.Y + 100 * self.O_Y, float('NaN'), float('NaN')));

    def Extend_Zero(self):
        return(O_PosData(self.X , self.Y + 5, float('NaN'), float('NaN')));


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
        
        SubWP_No = numpy.linalg.norm(numpy.array([Ax-Bx,Ay-By])) * definition;
        
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
        
        self.NextSWP = self.Pos
        
        self.Speed = 0;
        self.Sigma_max = 0.1;
        self.Kappa_max = 0.1;
        
        self.counter1 = 0;
        
        self.LastWP = 3;
        self.SWP = 0;
        self.SegmentCoords = 0;
        self.Current_SWP = 0;
        
        self.NextSWP_No = 0;
        self.NextSWP_validity = 0;
        
        self.FollowDistance = 6
        
        self.mark = 0;
        
    def SetDynamicModel(self, A, B, C, D, x):
        
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.x = x
        
        self.x = numpy.matrix([[0.],[0.],[0.]])
        
        alpha_v = 1
        alpha_w = 10
        
        self.Ts = 0.05
        
        K1 = 1 * self.Ts
        K2 = 1 * self.Ts
        K3 = 1 * self.Ts
        K4 = 1 * self.Ts
        
        self.A = numpy.matrix([[self.Ts * -alpha_v + 1., 0., 0.],[0., self.Ts * -alpha_w + 1., 0.],[0., self.Ts, 1.]])
        self.B = numpy.matrix([[K1, K2],[K3, -K4],[0., 0.]])
        
    def SetWaypoints(self, WPC):
        
        self.Waypoints = list()
        for i in range(WPC):
            self.Waypoints[i] = O_PosData(WPC[0,i], WPC[1,i], float('NaN'), float('NaN'))
        
    def UpdateStates(self, N):
        '''
        print(self.A)
        print(self.x)
        print(self.B)
        print(N)
        '''
        self.x = self.A * self.x + self.B * N
        #self.x[2] = numpy.arctan(numpy.sin(self.x[2]),numpy.cos(self.x[2]))
        return(numpy.array([self.x[0],self.x[1],self.x[2]]))
    
    def UpdatePos(self):
        curpos = self.Pos.get_Pos()
        x_next = numpy.sum(self.Ts * self.x[0] * math.sin(self.x[2]) + curpos[0])
        y_next = numpy.sum(self.Ts * self.x[0] * math.cos(self.x[2]) + curpos[1])
        #print(x_next, y_next)
        #print(numpy.sum(self.x[1]))
        self.Pos = O_PosData(x_next, y_next, math.cos(self.x[2]), math.sin(self.x[2]))
        return(numpy.array([x_next, y_next]))
    
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
        
        #if self.SegmentCoords:
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
        self.Straight.FitLine(0.07);
        
        return i;
    
    def get_PathSegment(self):
        
        LS = O_PosData(self.Straight.SubWP[0,0], self.Straight.SubWP[1,0], float('NaN'), float('NaN'))
        LF = O_PosData(self.Straight.SubWP[0,len(self.Straight.SubWP)-1], self.Straight.SubWP[1,len(self.Straight.SubWP)-1], float('NaN'), float('NaN'))
        CS = O_PosData(self.Path.TurnSWP[0,0], self.Path.TurnSWP[1,0], float('NaN'), float('NaN'))
        CF = O_PosData(self.Path.TurnSWP[0,len(self.Path.TurnSWP)-1], self.Straight.SubWP[1,len(self.Path.TurnSWP)-1], float('NaN'), float('NaN'))
        print(FL.Distance(self.NextSWP, CS), FL.Distance(self.NextSWP, CF))
        if FL.Distance(self.NextSWP, LS) > FL.Distance(self.NextSWP, LF):
            line = numpy.fliplr(self.Straight.SubWP);
            LF = LS
        else:
            line = self.Straight.SubWP
            
        if FL.Distance(LF, CS) > FL.Distance(LF, CF):
            curve = numpy.fliplr(self.Path.TurnSWP)
            #curve = self.Path.TurnSWP
        else:
            curve = self.Path.TurnSWP
        self.SegmentCoords = numpy.append(line, curve, 1)
        #plt.plot(self.SegmentCoords[0], self.SegmentCoords[1], 'r')
        #plt.show();
        
    def get_Line(self):
        return(self.Straight);
    
    def get_Turn(self):
        return(self.Path);
    
    def PlotPath(self, color):
        self.Path.PlotTurn(color);
        self.Straight.PlotLine(color);
        
    def FlushPath(self):
        self.SegmentCoords = []
        self.LastWP = 4
        
    def Control_Step(self):
        
        while 1:    
            try:
                self.NextSWP = O_PosData(self.SegmentCoords[0, self.NextSWP_No], self.SegmentCoords[1, self.NextSWP_No], float('NaN'), float('NaN'))
                if self.mark == 0:
                    plt.plot(self.NextSWP.get_Pos_X(), self.NextSWP.get_Pos_Y(), marker = 'o')
                    #print('Aim:')
                    #print(self.NextSWP.get_Pos())
                    #print(self.NextSWP_No)
                    self.mark = 1;
                '''
                print('Ship ori')
                print(180/math.pi * math.atan2(self.Pos.get_Ori_Y(), self.Pos.get_Ori_X()))
                print('Ship pos')
                print(self.Pos.get_Pos())
                '''
            except:
                print('End of LocalPath')
                self.LastWP = self.LastWP + 1;
                self.Plan_LocalPath(self.Path.Range);
                plt.plot(self.Pos.get_Pos_X(), self.Pos.get_Pos_Y(), marker = 'D')
                self.get_PathSegment()
                
                self.NextSWP = O_PosData(self.SegmentCoords[0, self.NextSWP_No], self.SegmentCoords[1, self.NextSWP_No], float('NaN'), float('NaN'))
                if self.mark == 0:
                    plt.plot(self.NextSWP.get_Pos_X(), self.NextSWP.get_Pos_Y(), marker = 'o')
                    self.mark = 1;
                
            Theta_r = self.get_Thera_r()
            delta = self.get_Delta(Theta_r)
            #print('delta')
            #print(delta*180/math.pi)
            valid = self.CheckReach(delta, self.NextSWP) and (FL.Distance(self.Pos, self.NextSWP) > self.FollowDistance);
            #print(delta*180/math.pi)
            #print('valid:', valid)
            if valid == 1:
                break
            self.NextSWP_No = self.NextSWP_No + 1
            #print(self.NextSWP.get_Pos())
            #print('Next SWP')
            self.mark = 0
            
            
        '''
        #############################################
        # RUN CONTROL ALGORITHM FOR DELTA HERE
        '''
        if delta < 0:
            N = numpy.matrix([[abs(delta)*10 + 8],[-abs(delta)*10 + 8]])
            #print('R')
        elif delta > 0:
            N = numpy.matrix([[-abs(delta)*10 + 8],[abs(delta)*10 + 8]])
            #print('L')
        else:
            N = numpy.matrix([[5],[5]])
            #print('S')
        '''
        #############################################
        '''
        #print('Run Control')
        
        results = self.UpdateStates(N)
        results = self.UpdatePos()
            
        '''Results of the control step'''
        
        return results;
    
    def get_Thera_r(self):
        
        Theta_r = FL.CosLaw(self.Pos.Extend_Zero(), self.Pos, self.NextSWP)
        if self.NextSWP.get_Pos_X() < self.Pos.get_Pos_X():
            Theta_r *= -1
        return Theta_r
        
    def get_Delta(self, Theta_r):
        
        Theta = numpy.sum(self.x[2])
        #Theta = math.atan2(math.sin(Theta), math.cos(Theta))
        
        delta = Theta-Theta_r
        delta = math.atan2(math.sin(delta), math.cos(delta))
        #print(Theta*180/math.pi,Theta_r*180/math.pi, delta*180/math.pi)
        return delta

    def CheckReach(self, delta, P):
        
        beta = math.pi/2 - delta;
        alpha = 2* delta;
        dist = FL.Distance(self.Pos, P);
        R_min = 1/self.Kappa_max;
        
        #return(dist * math.sin(beta) > R_min * math.sin(alpha));
        return(1)
    
'''
#############################################
# General Ship class
# Contains all the known information
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
        
        '''
        sublength = 100
        subarrays = numpy.floor(len(self.node_ids) / sublength)
        m = 0
        self.nodes = list(numpy.zeros(numpy.shape(self.node_ids)))
        while m < subarrays:
            self.nodes[m*sublength:(m+1)*sublength:1] = self.Api.NodesGet(self.node_ids[m*sublength:(m+1)*sublength:1])
            m += 1
            
        a1 = int(subarrays*sublength)
        a2 = len(self.nodes)
        print(a1,a2)
        
        #self.nodes[subarrays*sublength:len(self.nodes):1] = self.Api.NodesGet(self.node_ids[subarrays*sublength:len(self.nodes):1])
        self.nodes[a1:a2:1] = self.Api.NodesGet(self.node_ids[a1:a2:1])
        print(self.nodes)
        i = 0
        for n in self.nodes:
            print(self.nodes[i])
            self.longitudes[i] = self.nodes[i]['lon']
            self.latitudes[i] = self.nodes[i]['lat']
            i = i+1;
        '''
        
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
                
            #self.buffer = self.buffer[i * self.waylength:len(self.buffer)-1:1]
            self.buffer = list()
            
            print(self.Ways)
            
            return(self.Ways)
'''       
class O_Way_Collection:
    def __init__(self):
        self.waylist = list()
        self.Hashlist = list()
        
    def AddWay(self, Way):
        self.waylist.append(Way)
        self.Hashlist.append(hash(O_Listobject(Way.get_NodeIDs)))
        print(hash(O_Listobject(Way.get_NodeIDs)))
        print(self.Hashlist)
        
    def CheckWay(self, CandidateWay):
        if hash(O_Listobject(CandidateWay.node_ids)) in self.Hashlist:
            print('van')
            return 1
        else:
            print('nincs')
            return 0
        
    def __getstate__(self):
        return
        
    def Validate(self):
        return ('Valid')

     
class O_Pickler:
    def __init__(self, name):
            
            self.name = name
            
    def Save(self, Object):
        
        f = open(self.name, 'w')
        pickle.dump(Object, f, pickle.HIGHEST_PROTOCOL)
        
    def Load(self):
        try:
            
            f = open(self.name, 'r')
            print('picklerload')
            return O_Way_Collection();
            #return pickle.load(f)
            f.close();
            
            
        except:
            print('picklercreate')
            return O_Way_Collection();
            
                
class O_Listobject:
    def __init__(self, list):
        self.data = list
'''