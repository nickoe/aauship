'''
Created on 2012.12.05.

@author: Fodi based on Kalman.m from Lunde
'''

import numpy
import math


class Filter:
    
    def __init__(self):
    
        ''' Number of Samples:'''
        ts = 0.05; ''' Sampling time'''
        
        ''' System Parameters:'''
        m = 12.; ''' The ships mass'''
        I = (1./12.)*m*(0.25*0.25+1.05*1.05); ''' The ships inertia'''
        
        
        betaX = 8.9/m;
        betaY = 84/m;
        betaW = 3.77/I;
        #self.GPS_freq = 20;
        
        ''' System Definition:'''
        '''
        Hn = [1 ts (ts^2)/2 0 0 0 0 0 0;... % The X position
              0 1 ts 0 0 0 0 0 0;... % The X velocity
              0 -betaX 0 0 0 0 0 0 0;... % The X acceleration is a sum of forward motion (F_forward - F_drag)
              0 0 0 1 ts (ts^2)/2 0 0 0;... % The Y Position
              0 0 0 0 1 ts 0 0 0;... % The Y Velocity
              0 0 0 0 -betaY 0 0 0 0;... % The Y acceleration is a sum of the sideways motion (F_ymotion (wind?) - F_dragY)
              0 0 0 0 0 0 1 ts (ts^2)/2;... % The angle
              0 0 0 0 0 0 0 1 ts;... % The angular velocity
              0 0 0 0 0 0 0 -betaW 0]; % The angular acceleration is a sum of the drag an induced torque!
        '''
        
        self.Hn = numpy.matrix([[1, ts, (math.pow(ts,2))/2, 0, 0, 0, 0, 0, 0], [0, 1, ts, 0, 0, 0, 0, 0, 0], [0, -betaX, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, ts, (math.pow(ts,2))/2, 0, 0, 0], [0, 0, 0, 0, 1, ts, 0, 0, 0], [0, 0, 0, 0, -betaY, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, ts, (math.pow(ts,2))/2], [0, 0, 0, 0, 0, 0, 0, 1, ts], [0, 0, 0, 0, 0, 0, 0, -betaW, 0]])
              
        self.An = numpy.eye(9); ''' An eye matrix, as all the outputs scales equally - everything is in metric units!'''
        
        # Noise Terms (Input and Measurement Noise):
        # The Z(n) is the "driving noise" - as the system input is a forward force
        # and a torque, these are input here as well. The "input" matrix for the
        # driving noise Z(n) is then equal to: 
        
        '''Bn = [0 0;...
             0 0;...
             1/m 0;... % From force to input acceleration
             0 0;...
             0 0;...
             0 0;...
             0 0;...
             0 0;...
             0 1/I]; % From torque to angular acceleration
        '''
        print(I)
        self.Bn = numpy.matrix([[0, 0], [0, 0], [1/m, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1/I]])
        
        
        
        
        # W is the measurement noise on the system, this can be estimated to be
        # white gaussian noise, with zero mean (for most cases) and with a
        # variance, that are estimated in Appendix #XX. 
        self.varXpos = 0.979 * 1
        self.varXvel = 0.00262 * 1
        self.varXacc = 4.9451e-5 #  m/s^2 or 5.045*10^-6 G 
        
        self.varYpos = 1.12 * 1
        self.varYvel = 0.0001 * 1
        self.varYacc = 4.8815e-5 # m/s^2; or 4.9801*10^-6 G
        
        self.varWpos = 8.23332e-5 # computed from the conversion found in HoneyWell datasheet
        self.varWvel = 2e-6
        self.varWacc = 2.3559e-5 # m/s^2 or 2.4035*10^-6 G
        
        self.varYWacc = 2.4496*math.pow(10,-6); # rad/s^2
        
        # Random number at each iteration with a given variance. 
        
        ''' System initiation:'''
        # The system is initialized, the parameters are: 
        Wn = numpy.matrix(numpy.zeros([9,1]))
        self.Qz = numpy.matrix(numpy.zeros([9,9]))
        self.Qw = numpy.matrix(numpy.zeros([9,9]))

        ''' Resetting the parameters:'''
        self.YD = numpy.matrix(numpy.zeros([9,1]))
        self.YD_prev = numpy.matrix(numpy.zeros([9,1]))
        self.XD = numpy.matrix(numpy.zeros([9,1]))
        self.YpredD = numpy.matrix(numpy.zeros([9,1]))
        self.XpredD = numpy.matrix(numpy.zeros([9,1]))
        self.RpredD = numpy.matrix(numpy.zeros([9,9]))
        self.BD = numpy.matrix(numpy.zeros([9,9]))
        self.YupdateD = numpy.matrix(numpy.zeros([9,1]))
        self.YupdateD_prev = numpy.matrix(numpy.zeros([9,1]))
        self.RupdateD = numpy.matrix(numpy.zeros([9,9]))
        self.RupdateD_prev = numpy.matrix(numpy.zeros([9,9]))
        
        3self.sC = 0; ''' Sample counter - used to only include the 10th GPS sample.'''
        
        self.Qz = numpy.diag([0, 0, 55, 0, 0, 0, 0, 0, 20])
        
    
    def FilterStep(self, inputD, Wn, inputV):
        '''
        %% Running Computation of the Multirate Kalman filter (Negating the GPS input when no new sample is present):
        % As not all of the measurements are sampled at the same time (some are
        % slower, as the GPS for instance) - the samples where no GPS reading is
        % available will have to increase the level of the noise. Below is a list
        % of the sampling speeds of the sensors mounted on the ship:
        % GPS = 1Hz;
        % IMU = 20Hz;
        % This calls for attention to the GPS measurements, as these are not
        % sampled as often as the IMU! When this is done, the computation of the
        % Kalman filter becomes: 
        ''' 
        #print Wn
        
        self.YD_prev = self.YD
        self.YupdateD_prev = self.YupdateD
        self.RupdateD_prev = self.RupdateD
        
        self.Z = self.Bn*inputD
            
        self.Qw = numpy.matrix(numpy.diag([self.varXpos, self.varXvel, self.varXacc, self.varYpos, self.varYvel, self.varYacc, self.varWpos, self.varWvel, self.varWacc]))*ts;
        
        ''' self.YD = self.Hn*self.YD_prev+self.Z '''
        self.XD = Wn
        self.YpredD = self.Hn*self.YupdateD_prev
        self.XpredD = self.YpredD
        self.RpredD = self.Hn*self.RupdateD_prev*numpy.transpose(self.Hn)+self.Qz
        
        self.BD = (self.RpredD*numpy.transpose(self.An))*numpy.linalg.inv(self.An*self.RpredD*numpy.transpose(self.An)+self.Qw);
        Validity_M = numpy.diag([numpy.sum(inputV[0]), numpy.sum(inputV[1]), numpy.sum(inputV[2]), numpy.sum(inputV[3]), numpy.sum(inputV[4]), numpy.sum(inputV[5]), numpy.sum(inputV[6]), numpy.sum(inputV[7]), numpy.sum(inputV[8])])
        self.BD = self.BD*Validity_M
        self.YupdateD = self.YpredD+self.BD*(self.XD-self.XpredD);        
        self.RupdateD = (numpy.eye(9)-self.BD*self.An)*self.RpredD;
 #      self.sC = self.sC + 1;
        
        return numpy.matrix([[1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0]]) * self.YupdateD
        

