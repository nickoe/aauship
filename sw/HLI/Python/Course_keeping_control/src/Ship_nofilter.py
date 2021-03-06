'''
Created on 2012.11.12.

@author: Fodi
'''

import math
import numpy
import scipy
import matplotlib.pyplot as plt
import FunctionLibrary as FL
import ObjectLibrary as OL
import KalmanFilter as KF

'''
#############################################
# General Ship class
#############################################
'''   
class O_Ship:
    def __init__(self, init_position,log):
        '''
        Initializes the parameters of the ship
        - Parameters to calculate proper turn paths
        - Initial sensor parameters for the control
        - Initial start waypoint
        - Navigation parameters (FollowDistance)
        '''
        self.Pos = init_position
        
        self.retpos = self.Pos
        
        self.NextSWP = self.Pos
        
        self.Speed = 0;
        self.Sigma_max = 0.5;
        self.Kappa_max = 0.5;
        
        self.counter1 = 0;
        
        self.LastWP = 3;
        self.SWP = 0;
        self.SegmentCoords = 0;
        self.Current_SWP = 0;
        
        self.NextSWP_No = 0;
        self.NextSWP_validity = 0;
        
        self.FollowDistance = 2
        
        self.v = 0
        self.omega = 0
        self.Theta = 0
        
        self.x = numpy.matrix([[0],[0],[0]])
        
        self.mark = 0
        self.EndPath = 0
        self.WPsEnded = 0
        
        self.Filter = KF.Filter()
        
        self.correction = 0
        
        self.log = log
        
        '''
        The control matrices
        '''
        
        self.N = numpy.matrix([[1.2196566e+001, -2.2165773e-016], [ 2.9639884e-017, 9.6263068e-001]])
        
        self.F = numpy.matrix([[6.8421661e+000, -2.2165773e-016, -9.5435368e-017], [2.9639884e-017, 9.6263068e-001, 1.4310741e+000]])
        
        self.states = numpy.matrix([[0],[0],[0],[0],[0]])
        
    def SetWaypoints(self, WPC):
        '''
        A method to hand-set the required waypoints
        
        Accepts a 2*n shaped numpy array
        where A[0,n] is the X, A[1,n] is the Y coordinate
        '''
        WP_Planner = OL.O_PathWayPoints();
        WP_Planner.SetWP(WPC)
        self.Waypoints = WP_Planner
        
        self.EndPath = 0
    
    def Plan_WP(self, coastline, decimation, safety):
        
        '''
        Plans Waypoints in a snake-way if the coastline parameter is known
        '''
        
        WP_Planner = OL.O_PathWayPoints();
        WP_Planner.PlanWP(coastline, len(coastline), decimation, safety);
        self.Waypoints = WP_Planner
        self.AddRelativeCourse(self.retpos)
        
    def Plan_FullPath(self, plotit = 0):
        
        '''
        # Plans and plots all of the Sub-WayPoints of the system.
        # Should not be used under normal circumstances
        '''
        
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
        
        '''
        Plans the local course over the next waypoint
        Contains a straight path and the required turn
        Outputs a list of SWP-s
        '''
        
        self.Current_SWP = self.SegmentCoords;
            
        self.NextSWP_No = 0;
        self.NextSWP_validity = 0;
        
        gamma = 0;
        i = 0;
        
        while gamma <= 0 or gamma >= math.pi:
        
            i = i + 1;
            
            '''Turning waypoint''' 
            n = self.LastWP + 1 + i; 
            
            wpnum = len(self.Waypoints.get_WayPoints()[0])
            print (wpnum,n)
            
            try:
                
                if n+1 >= wpnum:
                    
                    Nm = self.Waypoints.get_SingleWayPoint(n - i);
                    Nt = self.Waypoints.get_SingleWayPoint(n);
                    Np = self.retpos;
                    
                elif n-i < 0:
                    
                    Nm = self.Pos
                    Nt = self.Waypoints.get_SingleWayPoint(n);
                    Np = self.Waypoints.get_SingleWayPoint(n + 1);
                    
                else:
                    
                    Nm = self.Waypoints.get_SingleWayPoint(n - i);
                    Nt = self.Waypoints.get_SingleWayPoint(n);
                    Np = self.Waypoints.get_SingleWayPoint(n + 1);
                
            except IndexError:
                #print 'szopo'
                return(-1);

            
            
            gamma = FL.CosLaw(Nm, Nt, Np);
            
        
        
        self.Path = OL.O_LocalPath(gamma, self.Sigma_max, self.Kappa_max);
        
        definition = 30;
        self.Path.FitPath(definition/8);
        self.Path.PositionPoly(Nm, Nt, Np);

        '''fitline'''
        Range = self.Path.get_Range();
        self.Straight = OL.O_StraightPath(Nt, Nm, Range, PrevRange);
        self.Straight.FitLine(definition);
        
        return i;
    
    def get_PathSegment(self):
        
        '''
        Forms the calculates Straight path and Turn path into an ordered list of points
        If WPsEnded == 1 the only SWP is the starting point
        '''
        
        
        
            
        try:
            LS = OL.O_PosData(self.Straight.SubWP[0,0], self.Straight.SubWP[1,0], float('NaN'), float('NaN'))
            LF = OL.O_PosData(self.Straight.SubWP[0,len(self.Straight.SubWP)-1], self.Straight.SubWP[1,len(self.Straight.SubWP)-1], float('NaN'), float('NaN'))
            CS = OL.O_PosData(self.Path.TurnSWP[0,0], self.Path.TurnSWP[1,0], float('NaN'), float('NaN'))
            CF = OL.O_PosData(self.Path.TurnSWP[0,len(self.Path.TurnSWP)-1], self.Straight.SubWP[1,len(self.Path.TurnSWP)-1], float('NaN'), float('NaN'))
            '''
            The Turn and Straight is received as a list of points.
            The method checks, whether the start or end point of the Straight is closer to the
            position of the Ship. If required, the order of the Straight is mirrored.
            '''
            if FL.Distance(self.Pos, LS) > FL.Distance(self.Pos, LF):
                line = numpy.fliplr(self.Straight.SubWP);
                LF = LS
            else:
                line = self.Straight.SubWP
            '''
            Then the method checks the relation of the Turn path Start and End points
            to the (new) End point of the Straight. If required, the Turn is mirrored as well.
            ''' 
            if FL.Distance(LF, CS) > FL.Distance(LF, CF):
                curve = numpy.fliplr(self.Path.TurnSWP)
            else:
                curve = self.Path.TurnSWP
        except:
            line = self.Straight.SubWP
            curve = self.Path.TurnSWP
        '''
        Last, the method joins the two ordered array of points to a single list of points
        '''
        self.SegmentCoords = numpy.append(line, curve, 1)

    def PlotPath(self, color):
        '''
        Plotting current path. Should not be used under normal circumstances
        '''
        self.Path.PlotTurn(color);
        self.Straight.PlotLine(color);
        
    def FlushPath(self, restart):
        '''
        Flushes all the current SWP data and resets the path to the specified WP
        Should be initialized by operator only
        '''
        self.SegmentCoords = []
        self.LastWP = restart
        self.Plan_LocalPath(0)
        self.get_PathSegment()
        
    def Control_Step(self):
        
        '''
        Outputs the calculated motor speeds based on the sensor inputs
        '''

        
        while 1:
            '''
            Gets the current destination point
            '''
            if self.WPsEnded == 0:
            
                if len(self.SegmentCoords)>0 and self.NextSWP_No < len(self.SegmentCoords[0]):
                    self.NextSWP = OL.O_PosData(self.SegmentCoords[0, self.NextSWP_No], self.SegmentCoords[1, self.NextSWP_No], float('NaN'), float('NaN'))
                    if self.mark == 0:
						self.log.write(str(self.NextSWP.get_Pos_X()) + ", " + str(self.NextSWP.get_Pos_Y()) + "\r\n")
						plt.plot(self.NextSWP.get_Pos_X(), self.NextSWP.get_Pos_Y(), 'b', marker = 'o') 
						self.mark = 1
                
                else:
                    '''
                    If there is no current destination point, the method requests a new path
                    '''
                    self.LastWP = self.LastWP + 1
                    
                    ret = self.Plan_LocalPath(self.Path.Range)
                    if ret == -1:
                        self.WPsEnded = 1
                        self.NextSWP_No = 100000
                        
                        #self.NextSWP = self.Waypoints.get_SingleWayPoint(self.LastWP + 1)
                        self.NextSWP = self.retpos
                    self.get_PathSegment()
                    
            else:
                self.NextSWP = self.retpos
                
                
            '''
            Calculation of the required heading
            and the current deviation from required heading
            '''
            
            Theta_r = self.get_Thera_r()
            delta = self.get_Delta(Theta_r)
            
            '''
            Checks the validity of the current destination point.
            If the Distance < FollowDistance the
            navigation procedure jumps to the next Sub-Waypoint
            '''
            valid = (FL.Distance(self.Pos, self.NextSWP) > self.FollowDistance);
            
            if valid == 0 and self.WPsEnded == 1:
                self.EndPath = 1
                break

            if valid == 1:
                break
            if self.WPsEnded == 0:
                self.NextSWP_No = self.NextSWP_No + 1
                self.mark = 0
                
            
        
            
        '''
        #############################################
        # RUN CONTROL ALGORITHM HERE
        '''
       
        Ref = numpy.matrix([[6], [self.x[1]-delta]])

        
        N = -self.F * self.x + self.N * Ref

        
        '''
        #############################################
        '''
            
        '''
        Results of the control step in the following format:
        Vertical(!) numpy Matrix(!)
        '''
        
        if self.EndPath == 0:
            return N;
        else:
            return numpy.matrix([[0], [0]])
    
    def ReadStates(self, input_m, input_f):
        
        '''
        Reads systems states from sensors (processed data)
        '''
        
        x = numpy.sum(input_m[0,0])
        xd = numpy.sum(input_m[1,0])
        xdd = numpy.sum(input_m[2,0])
        y = numpy.sum(input_m[3,0])
        yd = numpy.sum(input_m[4,0])
        ydd = numpy.sum(input_m[5,0])
        theta = numpy.sum(input_m[6,0])
        omega = numpy.sum(input_m[7,0])
        angacc = numpy.sum(input_m[8,0])
        
        '''No Kalman'''

        self.Ts = 0.1
        self.v = xd
        self.omega = omega
        self.Theta = math.atan2(math.sin(theta), math.cos(theta))
         
        self.x = numpy.matrix([[self.v],[self.Theta],[omega]])
        
        self.Pos.get_Pos_X()
        
        if numpy.sum(input_m[0,1]):
            
            x_next = 0.7 * x + 0.3 * self.Pos.get_Pos_X()
            y_next = 0.7 * y + 0.3 * self.Pos.get_Pos_Y()
            
        else:
        
            x_next = xd * 0.1 * math.sin(theta) + self.Pos.get_Pos_X()
            y_next = yd * 0.1 * math.cos(theta) + self.Pos.get_Pos_Y()
            
        #print('FX', x_next, 'FY', y_next, 'FV', numpy.sum(self.states[2]), 'FT', numpy.sum(self.states[3]), 'FO', numpy.sum(self.states[4]))
        
        self.Pos = OL.O_PosData(x_next, y_next, math.cos(self.x[1]), math.sin(self.x[1]))
        
    def get_Thera_r(self):
        
        '''
        Calculates the required heading
        '''
        Theta_r = FL.CosLaw(self.Pos.Extend_Zero(), self.Pos, self.NextSWP)
        '''
        The CosLaw function returns a positive angle
        If the ship must turn left, the X coordinate of the Next SWP < X coordinate of Ship
        In that case, Theta_r is in the negative angle-space, therefore must be negated
        '''
        if self.NextSWP.get_Pos_X() < self.Pos.get_Pos_X():
            Theta_r *= -1
        return Theta_r
        
    def get_Delta(self, Theta_r):
        
        '''
        Calculates the current deviation from heading
        '''
        
        delta = self.Theta-Theta_r
        '''
        Until this point, nothing ensures, that -pi < Theta-Theta_r < pi.
        With this method we make sure, that -pi < delta < pi
        IF later the control is based on Theta_r and Theta, the same
        adjustment of values must be implemented!
        '''
        delta = math.atan2(math.sin(delta), math.cos(delta))
        return delta
         
    def AddRelativeCourse(self, WPC):
        '''
        Sets a 
        '''
        #Parameters: self, list of WP-s
        '''
        R = 6371080
        
        lon = math.degrees(WPC.get_Pos_X() / R)
        lat = math.degrees(WPC.get_Pos_Y() / R)
        
        
        
        xy = numpy.array([[lon],[lat]])
        self.Waypoints.AddWP(xy)
        self.WPsEnded = 0
        self.EndPath = 0
        '''
        X = self.Pos.get_Pos_X() + WPC.get_Pos_X()
        Y = self.Pos.get_Pos_Y() + WPC.get_Pos_Y()
        xy = numpy.array([[X],[Y]])
        self.Waypoints.AddWP(xy)
        self.WPsEnded = 0
        self.EndPath = 0
        
    def AddCourse(self, WPC):
        
        '''
        Sets a 
        '''
        #Parameters: self, list of WP-s
        xy = numpy.array([[WPC.get_Pos_X()],[WPC.get_Pos_Y()]])
        self.Waypoints.AddWP(xy)
        self.WPsEnded = 0
        self.EndPath = 0
        
    def FtoM(self, motor):
        '''
        Linear transformation from the general
        Force and Torque controller output
        to obtain the necessary engine PWMs.
        '''

        K = math.pow(0.05,4)*0.5*1000;
        theta = math.pi/16;
        C1 = 0.5*math.sin(theta);
        C2 = 0.5*math.sin(-theta);
        
        L = numpy.matrix([[K, K],[K*C1, K*C2]])
        L_inv = numpy.linalg.inv(L)
        temp = numpy.array(L_inv*motor)
        N = numpy.sqrt(numpy.abs(temp))*numpy.sign(temp)
        
        return list([N[0], N[1]])
    
    def Return(self, retpos):
        '''
        Sets the GPS posizion of default return,
        after the navigation ran out of waypoints.
        '''
        
        self.retpos = retpos
    
    def Set_SteadyG(self, x, y, z):
        '''
        Sets the reference accelerometer
        data in steady position
        '''
        
        self.RefG = numpy.linalg.norm([x, y, z])
