#!/usr/bin/env python3

import os, sys, time
import datetime as dt
from threading import Thread
from math import sin,cos,atan2
import numpy as np

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

def subtract(a,b):
    return np.array([ [a[0]-b[0]] , [a[1]-b[1]] ])

# calculates the cross product of vector p1 and p2
# if p1 is clockwise from p2 wrt origin then it returns +ve value
# if p2 is anti-clockwise from p2 wrt origin then it returns -ve value
# if p1 p2 and origin are collinear then it returs 0
def cross_product(p1, p2):
	return p1[0] * p2[1] - p2[0] * p1[1]

# returns the cross product of vector p1p3 and p1p2
# if p1p3 is clockwise from p1p2 it returns +ve value
# if p1p3 is anti-clockwise from p1p2 it returns -ve value
# if p1 p2 and p3 are collinear it returns 0
def direction(p1, p2, p3):
	return  cross_product(subtract(p3,p1), subtract(p2,p1))

# checks if p lies on the segment p1p2
def on_segment(p1, p2, p):
    return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])

# checks if line segment p1p2 and p3p4 intersect
def edge_is_collision(p1, p2, p3, p4):
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
        ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    elif d1 == 0 and on_segment(p3, p4, p1):
        return True
    elif d2 == 0 and on_segment(p3, p4, p2):
        return True
    elif d3 == 0 and on_segment(p1, p2, p3):
        return True
    elif d4 == 0 and on_segment(p1, p2, p4):
        return True
    else:
        return False


class Polygon(object):
    def __init__(self,poly_type=None,*argv):
        self.verticies = []

        if poly_type == 'rect':
            assert(len(argv)==2)
            self.rectangle(argv[0],argv[1])

    def rectangle(self,top_left,bottom_right):
        top_right = np.array([ [bottom_right[0]] , [top_left[1]] ])
        bottom_left = np.array([ top_left[0],bottom_right[1] ])
        self.verticies = [top_left,top_right,bottom_right,bottom_left]

def polygon_is_filled(polygon):
    vec_sec = np.zeros((2,len(polygon.verticies)))
    sub_vec = np.zeros((2,len(polygon.verticies)))

    vec_set[:,0]
    for point in polygon.verticies:
        pass