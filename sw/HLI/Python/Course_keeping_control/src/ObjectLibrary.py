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
    def __init__(self, PathCoords, sigma_max, kappa_max):
        
        #1 degree rotation
        #Rot_plus = numpy.array([[math.cos(math.pi/180), -math.sin(math.pi/180)][math.sin(math.pi/180), math.cos(math.pi/180]]));
        #Rot_minus = Rot_plus.T;
        
        R_min=1/kappa_max;
        Psi_max=kappa_max^2/2/sigma_max;
        kappa = 1.
        sigma = 1.;
        
        fi_max = math.pow(kappa,2) / (2*sigma);
        fi = fi_max*1.5;
        
        
        '''
        Calculate parameters in local base
        '''
        
        if fi > fi_max:

            tlen = 2
            
            t = numpy.linspace(0.,tlen, 1000);
            ax = numpy.linspace(0.,tlen, 1000);
            ay = numpy.linspace(0.,tlen, 1000);
            j = 0;
            
            for i in t:
                b = scipy.special.fresnel(i);
                ay[j] = b[0];
                ax[j] = b[1];
                if j > 2 and math.atan((ay[j-1]-ay[j-2])/(ax[j-1]-ax[j-2])) >= fi_max:
                    break;
                j = j+1;

            print(fi_max, math.atan((ay[j-1]-ay[j-2])/(ax[j-1]-ax[j-2])));

            xd = math.sqrt(math.pi / sigma) * ax[j];
            yd = math.sqrt(math.pi / sigma) * ay[j];
            
            xd = 1 * ax[j];
            yd = 1 * ay[j];
            
            
            '''
            XR = R_min * math.sin(fi - fi_max);
            YR = 2 * R_min * math.pow(math.sin((fi-fi_max)/2), 2);
            
            X1 = math.cos(fi-fi_max) * (xd + yd*math.tan(fi-fi_max));
            Y1 = X1 * math.tan(fi);
            
            X2 = XR;
            Y2 = math.sin(fi) * (xd + yd*math.tan(fi))-yd/math.cos(fi);
            '''
            
            XR = R_min * math.sin(fi - fi_max);
            Px = XR + yd * math.sin(fi);
            X1 = Px + xd * math.cos(fi);
            Y1 = X1 * math.tan(fi);
            Py = Y1 - xd * math.sin(fi);
            Y2 = Py + yd * math.cos(fi);
            Oy = R_min * math.cos(fi-fi_max) + Y2;
            YR = Oy - R_min;
            X2 = XR;
            
            
            A = numpy.matrix([-X1,Y1]);
            B = numpy.matrix([-X2,Y2]);
            C = numpy.matrix([0,YR]);
            D = numpy.matrix([X2,Y2]);
            E = numpy.matrix([X1,Y1]);
            
            PointStore_Y = numpy.array([Y1,Y2,YR,Y2,Y1]);
            PointStore_X = numpy.array([-X1,-X2,0,X2,X1]);
            
            
            #PointStore = numpy.matrix([numpy.transpose(A),numpy.transpose(B),numpy.transpose(C),numpy.transpose(D),numpy.transpose(E)])
            
            
            plt.plot(PointStore_X,PointStore_Y);
            
            Poly = numpy.polynomial.hermite.hermfit(PointStore_X, PointStore_Y, 4);

            X = numpy.linspace(PointStore_X[0],PointStore_X[4]);
            Pathline = numpy.polynomial.hermite.hermval(X, Poly);
            plt.plot(X,Pathline);
            
            '''
            print path
            '''
            
            line = numpy.array([-3., 0., 3.]);
            xline = numpy.array([-2., 0., 2.]);
            yline = numpy.array([0., 0., 0.]);
            
            
            xline[0] = line[0] * math.cos(fi);
            xline[2] = line[2] * math.cos(fi);
            
            yline[0] = abs(line[0]) * math.sin(fi);
            yline[2] = abs(line[2]) * math.sin(fi);
            
            
            plt.plot(xline,yline);
            
            plt.show();
            
            
            
        else:
            
            '''Itt a baj'''
            
            tlen = math.sqrt(2/math.pi) * fi;
            tlen = 2
            
            SC = scipy.special.fresnel(tlen);
            Sf = SC[0];
            Cf = SC[1];
            
            t = numpy.linspace(0.,tlen, 1000);
            ax = numpy.linspace(0.,tlen, 1000);
            ay = numpy.linspace(0.,tlen, 1000);
            j = 0;
            
            for i in t:
                b = scipy.special.fresnel(i);
                ay[j] = b[0];
                ax[j] = b[1];
                if j > 2 and math.atan((ay[j-1]-ay[j-2])/(ax[j-1]-ax[j-2])) >= fi:
                    break;
                j = j+1;

            print(fi, math.atan((ay[j-1]-ay[j-2])/(ax[j-1]-ax[j-2])));

            xd = math.sqrt(math.pi / sigma) * ax[j];
            yd = math.sqrt(math.pi / sigma) * ay[j];
            
            
            print(xd,yd);
            
            '''Innen jo'''
            
            X1 = xd * math.cos(fi) + yd * math.sin(fi);
            Y1 = (yd * math.tan(fi) + xd) * math.sin(fi);
            Y1 = X1 * math.tan(fi);
            
            #print(xd, yd)
            
            A = numpy.array([-X1,Y1]);
            C = numpy.array([0,yd/math.cos(fi)]);
            E = numpy.array([X1,Y1]);
            
            PointStore_X = numpy.array([A[0],C[0],E[0]]);
            PointStore_Y = numpy.array([A[1],C[1],E[1]]);
            
            
            plt.plot(PointStore_X,PointStore_Y);
            
            Poly = numpy.polynomial.hermite.hermfit(PointStore_X, PointStore_Y, 2);

            X = numpy.linspace(PointStore_X[0],PointStore_X[2]);
            Pathline = numpy.polynomial.hermite.hermval(X, Poly);
            plt.plot(X,Pathline);
            
            '''
            print path
            '''
            
            line = numpy.array([-3., 0., 3.]);
            xline = numpy.array([-2., 0., 2.]);
            yline = numpy.array([0., 0., 0.]);
            
            
            xline[0] = line[0] * math.cos(fi);
            xline[2] = line[2] * math.cos(fi);
            
            yline[0] = abs(line[0]) * math.sin(fi);
            yline[2] = abs(line[2]) * math.sin(fi);
            
            plt.plot(xline,yline);            
            plt.show();
        
        
''' Beautiful but obsolete 
class O_LocalPath:
    def __init__(self, PathWayPoints, NextWaypointNo, Spiraldata, PosData):
        
        #1: determine the length of the Euler-spiral
        
        WP = PathWayPoints.get_WayPoints();
        
        # Destination orientation
        req_Ori_S = WP[0, NextWaypointNo+1] - WP[0, NextWaypointNo];
        req_Ori_C = WP[1, NextWaypointNo+1] - WP[1, NextWaypointNo];
        
        req_Ori_S = -1;
        req_Ori_C = 0;
       
        # Normalized orientation of destination
        norm_req_Ori_S =  req_Ori_S / math.sqrt(math.pow(req_Ori_S,2) + math.pow(req_Ori_C,2));
        norm_req_Ori_C =  req_Ori_C / math.sqrt(math.pow(req_Ori_S,2) + math.pow(req_Ori_C,2));
        
        # Current orientation
        PosOri_X = PosData.get_Ori_X();
        PosOri_Y = PosData.get_Ori_Y();
        
        # Scalar product for vector mirroring
        dotproduct = norm_req_Ori_C * PosOri_X + norm_req_Ori_S * PosOri_Y;
        
        #Irany! -0.5 pi-t ne +3/2 pi-vel forduljon...
        
        
        # Vector mirroring
        diff_v_X = -numpy.abs(PosOri_X - norm_req_Ori_C * dotproduct);
        diff_v_Y = -numpy.abs(PosOri_Y - norm_req_Ori_S * dotproduct);
        # Vector mirroring 2: turn vectors
        Turn_X = PosOri_X - 2 * diff_v_X;
        Turn_Y = PosOri_Y - 2 * diff_v_Y;

        i = 0;
        

        Data_X = Spiraldata.get_EulerO_X();
        Data_Y = Spiraldata.get_EulerO_Y();
        self.corr = scipy.zeros(scipy.size(Data_X));
        print(norm_req_Ori_C);
        while i < int(scipy.size(self.corr)):
            self.corr[i] = Data_X[i] * Turn_X + Data_Y[i] * Turn_Y;
            i = i + 1;
        
        turn_length = 0;
        while self.corr[turn_length] != numpy.max(self.corr):
            turn_length = turn_length+1;
        
        turn_length = turn_length+1;
        
        #2: determine the size coefficient of the Euler-spiral
        
        
        Dest_X = (WP[1, NextWaypointNo+1] + WP[1, NextWaypointNo]) / 2;
        Dest_Y = (WP[0, NextWaypointNo+1] + WP[0, NextWaypointNo]) / 2;
        Pos_X = PosData.get_Pos_X();
        Pos_Y = PosData.get_Pos_Y();
        
        V_X = Dest_X - Pos_X;
        V_Y = Dest_Y - Pos_Y;
        
        E_X = Data_X[turn_length];
        E_Y = Data_Y[turn_length];
        
        k_X = V_X / E_X;
        k_Y = V_Y / E_Y;
        
        turnpath_X = Data_X[0:turn_length];
        turnpath_Y = Data_Y[0:turn_length];
        
        plt.plot(turnpath_X, turnpath_Y);
        plt.show()
        '''
        
        
    
        

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


        