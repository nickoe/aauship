'''
Created on 2012.10.01.

@author: Fodi
'''

'''
#############################################
# Function Library for ASV HLI
#############################################
'''

import math
import numpy
import scipy
#import control

import ObjectLibrary as OL

def fcn_GenerateEuler(length = 2, l_precision = 30, d_precision = 30):
    '''
    Generate the Euler-spiral
    '''
    # Solving the fresnel-integral:
    x = 0.;

    S = scipy.zeros((length*l_precision));
    C = scipy.zeros((length*l_precision));
    O_X = scipy.zeros((length*l_precision));
    O_Y = scipy.zeros((length*l_precision));
    
    
    while x < len(S):
        
        n = 0.;
        while n < d_precision:
            
            S[x] = S[x] + pow(-1, n) * ( pow(x*math.sqrt(math.pi/2)/l_precision,(4*n+3)) / math.factorial(2*n+1) / (4*n+3));
            C[x] = C[x] + pow(-1, n) * ( pow(x*math.sqrt(math.pi/2)/l_precision,(4*n+1)) / math.factorial(2*n) / (4*n+1))
        
            n = n+1;
            
            
        if (x!=0):
            
            
            O_X[x] = (C[x] - C[x-1]) / math.sqrt((math.pow(S[x] - S[x-1], 2) + math.pow(C[x] - C[x-1], 2)));
            O_Y[x] = (S[x] - S[x-1]) / math.sqrt((math.pow(S[x] - S[x-1], 2) + math.pow(C[x] - C[x-1], 2)));
            
        else:
            
            O_X[x] = 1;
            O_Y[x] = 0;
            
        x = x+1;
    
    return OL.O_EulerSpiral(S,C,O_X,O_Y);
    
    '''
    Euler-spiral generation complete
    '''


def CosLaw(A,B,C):
    
    A = A.get_Pos();
    
    B = B.get_Pos();
    
    C = C.get_Pos();

    x = B-C
    a = numpy.sqrt(x.dot(x))
    x = A-C
    b = numpy.sqrt(x.dot(x))
    x = A-B
    c = numpy.sqrt(x.dot(x))
    
    '''
    print(a)
    print(b)
    print(c)
    '''
    try:
        gamma = math.acos((numpy.power(a,2) + numpy.power(c,2) - numpy.power(b,2))/(2 * a * c));    
    except:
        gamma = math.pi
        
    return(gamma);


def SimulateCoast(coastlength):

    '''
    Simulated coast-line:
    '''
    i = 0;
    coast = scipy.randn(coastlength) * 10;
    initial = 0;
    
    while i < coastlength:
       
        coast[i] = initial + coast[i];
        initial = coast[i];
        i = i + 1;

    return coast;

def Distance(A, B):
    
    '''
    Distance between two points
    '''
    x = A.get_Pos()-B.get_Pos()
    a = numpy.sqrt(x.dot(x))
    
    return(a);

def find_id_index(array, id):
    i = 0;
    while i < len(array):
        if array[i] == id:
            return i;
            break;
        i = i+1;
    
    return(-1);
        
