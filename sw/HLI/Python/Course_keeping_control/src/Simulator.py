'''
Created on 2012.11.12.

@author: Fodi
'''

import math
import numpy
import scipy
import control
import matplotlib.pyplot as plt

import ObjectLibrary as OL
import FunctionLibrary as FL


'''
#############################################
# Simulator Class
# Implements a simulation of the real system
#############################################
''' 

class Simulator:
    def __init__(self):
        
        '''
        A simple initialization of the simulator with empty values
        '''
        
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.x = 0
        
    def SetDynamicModel(self, A, B, C, D, x, P):
        
        '''
        Sets the dynamic model and initial conditions of the system.
        '''
        
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.x = x
        
        self.Pos = P
        
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
        
    def UpdateStates(self, N):
        '''
        Updates the system states, based on the
        system input and previous states (motor speeds)
        '''
        self.x = self.A * self.x + self.B * N
        '''
        Returns the current system states
        '''
        return(numpy.array([self.x[0],self.x[1],self.x[2]]))
    
    def UpdatePos(self, states):
        '''
        Calculates the new positions based on the previous positions
        and the current system states (speed and heading)
        '''
        curpos = self.Pos.get_Pos()
        x_next = numpy.sum(self.Ts * states[0] * math.sin(states[2]) + curpos[0])
        y_next = numpy.sum(self.Ts * states[0] * math.cos(states[2]) + curpos[1])
        self.Pos = OL.O_PosData(x_next, y_next, math.cos(self.x[2]), math.sin(self.x[2]))
        '''
        Returns the current ship position
        '''
        return(numpy.array([x_next, y_next]))
    
    def SimulateCoast(self, coastlength):

        '''
        Simulates a coast line with an X(n+1) = X(n) + W(n) random process
        where W(n) is a gaussian random process
        '''
        i = 0;
        coast = scipy.randn(coastlength) * 10;
        initial = 0;
        
        while i < coastlength:
           
            coast[i] = initial + coast[i];
            initial = coast[i];
            i = i + 1;
        '''
        The coastline is returned as a function of x (x axis)
        '''
        return coast;