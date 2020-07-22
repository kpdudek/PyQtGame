#!/usr/bin/env python3

import os, sys, time
import datetime as dt
from threading import Thread
from math import sin,cos,atan2

from Utils import *

def edge_angle(ang_type,*argv):
    '''
    The edge angle is found using unit vectors. This function can be passed two angles defined counter clowise from 0 being horizontal, or
    a set of three verticies.
    '''
    # This function finds the signed shortest distance between two vectors
    if ang_type == 'angle':
        assert(len(argv)==2)

        ang1 = float(argv[0])
        ang2 = float(argv[1])
        vertex0 = [0.0,0.0]
        vertex1 = [cos(ang1),sin(ang1)]
        vertex2 = [cos(ang2),sin(ang2)]
    elif ang_type == 'verticies':
        assert(len(argv)==3)
        
        vertex0 = argv[0]
        vertex1 = argv[1]
        vertex2 = argv[2]
    else:
        log('Edge angle type not recognized!',color='r')
        return None

    # Dot product of the vectors
    cosine_theta = vertex1[0]*vertex2[0] + vertex1[1]*vertex2[1]
    
    # Cross product of the vectors
    sin_theta = vertex1[0]*vertex2[1] - vertex1[1]*vertex2[0]
    
    # find the angle using the relationships sin(theta)== tan(theta) = sin(theta)/cos(theta)
    edge_angle = atan2(sin_theta,cosine_theta)
    return edge_angle