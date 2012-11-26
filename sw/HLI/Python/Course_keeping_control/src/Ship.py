'''
Created on 2012.11.12.

@author: Fodi
'''

import math
import numpy
import scipy
#import control
import matplotlib.pyplot as plt

import FunctionLibrary as FL
import ObjectLibrary as OL
#import CommUnit as CU

'''
#############################################
# General Ship class
#############################################
'''   
class O_Ship:
    def __init__(self, init_position):
        '''
        Initializes the parameters of the ship
        - Parameters to calculate proper turn paths
        - Initial sensor parameters for the control
        - Initial start waypoint
        - Navigation parameters (FollowDistance)
        '''
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
        
        self.v = 0
        self.omega = 0
        self.Theta = 0
        
        self.mark = 0;
        
    def SetWaypoints(self, WPC):
        '''
        A method to hand-set the required waypoints
        
        Accepts a 2*n shaped numpy array
        where A[0,n] is the X, A[1,n] is the Y coordinate
        '''
        WP_Planner = OL.O_PathWayPoints();
        WP_Planner.AddWP(WPC)
        self.Waypoints = WP_Planner
    
    def Plan_WP(self, coastline, decimation, safety):
        
        '''
        Plans Waypoints in a snake-way if the coastline parameter is known
        '''
        
        WP_Planner = OL.O_PathWayPoints();
        WP_Planner.PlanWP(coastline, len(coastline), decimation, safety);
        self.Waypoints = WP_Planner
        
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
            
            try:
                Nm = self.Waypoints.get_SingleWayPoint(n - i);
                Nt = self.Waypoints.get_SingleWayPoint(n);
                Np = self.Waypoints.get_SingleWayPoint(n + 1);
            except IndexError:
                return('Path ended');
            
            
            
            gamma = FL.CosLaw(Nm, Nt, Np);
            
        print(n);
        
        self.Path = OL.O_LocalPath(gamma, self.Sigma_max, self.Kappa_max);
        
        definition = 20;
        self.Path.FitPath(definition);
        self.Path.PositionPoly(Nm, Nt, Np);

        '''fitline'''
        Range = self.Path.get_Range();
        self.Straight = OL.O_StraightPath(Nt, Nm, Range, PrevRange);
        self.Straight.FitLine(0.07);
        
        return i;
    
    def get_PathSegment(self):
        
        '''
        Forms the calculates Straight path and Turn path into an ordered list of points
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
            if len(self.SegmentCoords)>0 and self.NextSWP_No < len(self.SegmentCoords[0]):
                self.NextSWP = OL.O_PosData(self.SegmentCoords[0, self.NextSWP_No], self.SegmentCoords[1, self.NextSWP_No], float('NaN'), float('NaN'))
                if self.mark == 0:
                    plt.plot(self.NextSWP.get_Pos_X(), self.NextSWP.get_Pos_Y(), marker = 'o')
                    self.mark = 1
            
            else:
                '''
                If there is no current destination point, the method requests a new path
                '''
                self.LastWP = self.LastWP + 1
                self.Plan_LocalPath(self.Path.Range)
                self.get_PathSegment()
                
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

            if valid == 1:
                break
            self.NextSWP_No = self.NextSWP_No + 1
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
            
        '''
        Results of the control step in the following format:
        Vertical(!) numpy Matrix(!)
        '''
        
        return N;
    
    def ReadStates(self, v, omega, theta, Pos):
        
        '''
        Reads systems states from sensors (processed data already)
        '''
        
        self.v = v
        self.omega = omega
        
        self.Theta = theta
        self.Pos = OL.O_PosData(Pos[0], Pos[1], math.cos(theta), math.sin(theta))
    
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
    
    def SendData(self, data):
        
        Stream = CU.Streamer()
        
