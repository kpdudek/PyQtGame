#!/usr/bin/env python3

import os, sys, time
import datetime as dt
from threading import Thread
from matplotlib import pyplot as plt
from matplotlib import patches
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
def edge_is_collision(edge1,edge2,endpoint_collision=False):
    p1 = edge1[:,0]
    p2 = edge1[:,1]
    p3 = edge2[:,0]
    p4 = edge2[:,1]

    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if endpoint_collision:
        if d1 == 0 and on_segment(p3, p4, p1):
            return True
        elif d2 == 0 and on_segment(p3, p4, p2):
            return True
        elif d3 == 0 and on_segment(p1, p2, p3):
            return True
        elif d4 == 0 and on_segment(p1, p2, p4):
            return True

    # Overlap collision check
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
        ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
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

def polygon_is_self_occluded(vertex,vertexPrev,vertexNext,point):
    '''
    Determines if a set of test points are Self Occluded, or non-intersecting but within a polygon 
    Inputs are three [2 x 1] vectors that represent a vertex on a polygon,
    the vertex that preceeded it, and the vertex that follows in
    construction, and a [2 x N] matrix of test points of the form [x1..xn; y1...yn].
    Function handles both counterclockwise or filled-in polygons and clockwise or
    hollow polygons. Output is [1 x N] boolean array where true is a self
    occluded test point.
    '''
    results = np.zeros(len(point[0,:]),dtype=bool)

    for iPoints in range(0,len(point[0,:])):
        angleNext = atan2(vertexNext[1]-vertex[1],vertexNext[0]-vertex[0])
        anglePrev = atan2(vertexPrev[1]-vertex[1],vertexPrev[0]-vertex[0])
        anglePoint = atan2(point[1,iPoints]-vertex[1],point[0,iPoints]-vertex[0])
        
        #maintaining the vertices gives a consistent relationship of what
        #angles constitue self-occlusion for both counterclockwise and
        #clockwise objects, but is dependent on whether the previous angle
        #was greater or less than the next angle.
        if anglePrev > angleNext:
            if anglePoint < anglePrev and anglePoint > angleNext:
                results[iPoints]=True
            else:
                results[iPoints]=False
        else:
            if anglePoint < anglePrev or anglePoint > angleNext:
                results[iPoints]=True
            else:
                results[iPoints]=False
    return results

def polygon_is_visible(vertices,indexVertex,points):
    # Determines if a set of test points are visible by a paticular vertex of a polygon
    # Inputs are a [2 x N] set of vertices that define a polygon of the form
    # [x1..xn; y1..yn], an integer index to indicate which vertex to test,
    # and a [2 x N] set of coordinates that are test points of the form [x; y].
    # The function combines the output of two helper functions, to determine 
    # if the test point is invisible to the vertex by either self-occlusion
    # or collision with an edge of the polygon. Output is a [1 x N] boolean 
    # array where true means the test point is visible.
    
    # Error handling for indexVertex
    if indexVertex > len(vertices[0,:])-1 or indexVertex < 0:
        log('IndexVertex must be a valid column index of "vertices" between 1 and size(vertices,2)')
        return
    
    #Converting inputs to inputs for polygon_isSelfOccluded() and handling
    #the roll-over cases for the indexVertex input
    vertex = vertices[:,indexVertex].reshape((2,1))
    if indexVertex == 0:
        vertexPrev = vertices[:,-1]
    else:
        vertexPrev=vertices[:,indexVertex-1]

    if indexVertex == len(vertices[0,:])-1:
        vertexNext=vertices[:,0]
    else:
        vertexNext=vertices[:,indexVertex+1]
    selfOccludedPoints = polygon_is_self_occluded(vertex,vertexPrev,vertexNext,points)
    
    # Running edge_isCollision for each test point against every edge of the
    # polygon. 'Break' is added to stop checking once the first collision is
    # found
    # edgeCollisionPoints=false(1,size(points,2))
    edgeCollisionPoints = np.zeros(len(points[0,:]),dtype=bool)
    for iPoints in range(0,len(points[0,:])): #1:size(points,2)
        # The first of the two lines to check collision for is always the
        # line from the test point to inputed vertex
        sightLine = np.concatenate((vertex,points[:,iPoints].reshape(2,1)),axis=1)
        for jEdges in range(0,len(vertices[0,:])): #=1:size(vertices,2)
            if jEdges == len(vertices[0,:])-1:
                edge = np.concatenate((vertices[:,jEdges].reshape(2,1),vertices[:,0].reshape(2,1)),axis=1)
            else:
                edge = np.concatenate((vertices[:,jEdges].reshape(2,1),vertices[:,jEdges+1].reshape(2,1)),axis=1)
            
            if edge_is_collision(sightLine,edge) == True:
                edgeCollisionPoints[iPoints]=True
                break
    # helper functions return 'is invisible'; invert results for 'visible'
    return np.logical_not(np.logical_or(selfOccludedPoints,edgeCollisionPoints))

def polygon_is_collision(vertices,points):
    '''
    Determines if a set of points lies inside or outside of a given polygon
    Inputs are a [2 X N] set of vertices of the form [x1..xn; y1...yn] and
    a [2 x N] set of test points of the same form. Uses lower level
    function polygon_isVisible to determine if test point is visible to any
    vertex of the polygon, and thus inside or outside. Note: for a hollow
    polygon, 'outside' or non-collision is inside the polygon. Output is
    a [1 X N] boolean array where true means the point is colliding. 
    '''
    results = np.ones(len(points[0,:]),dtype=bool)#flagPoints=true(1,size(points,2))
    # print(results)
    for iVertices in range(0,len(vertices[0,:])): #=1:size(vertices,2)
        flagPointVertex = polygon_is_visible(vertices,iVertices,points)
        results = np.logical_and(results, np.logical_not(flagPointVertex))
    return results

def polygon_is_filled():
    pass

def reshape_for_patch(vertices):
    '''
    This shape takes verticies of a polygon with shape [2,N]
    and returns the same vertices with shape [N,2]
    '''
    r,c = vertices.shape
    out = np.zeros(vertices.size)
    out = np.reshape(out,(c,r))
    for i in range(0,c):
        for j in range(0,r):
            out[i,j] = vertices[j,i]
    return out

def polygon_plot(vertices,color='b',points=None,point_color='g',lim=5,title='A Plot'):
    _,ax = plt.subplots(1)
    ax.set_ylim(-lim, lim)
    ax.set_xlim(-lim, lim)
    vertices = reshape_for_patch(vertices)
    patch = patches.Polygon(vertices, facecolor=color, fill=True)
    ax.add_patch(patch)
    try: 
        ax.plot(points[0,:],points[1,:],f'{point_color}o', markersize=3)
    except:
        pass # No point array passed
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(color='k', linestyle='-', linewidth=.5)
    plt.title(f'{title}')

    Thread(target=plt.show, daemon=True)
    # plt.show()