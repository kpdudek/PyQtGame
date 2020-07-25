#!/usr/bin/env python3

import random, sys, os, math, time, numpy
from matplotlib import pyplot as plt
from matplotlib import patches

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))

from Utils import *
from Geometry import *

print('/////////////////////////////////////////////////////////////////////')
print('/ Edge Angle Tests')
print('/////////////////////////////////////////////////////////////////////')
ang1 = 0.
ang2 = 0.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'Angles: {ang1} & {ang2}\nResults: {same_edges_angle}')

ang1 = 0.
ang2 = 7.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')

ang1 = 0.2
ang2 = 6.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')

print('\n/////////////////////////////////////////////////////////////////////')
print('/ Edge Collision Tests')
print('/////////////////////////////////////////////////////////////////////')
edge1 = np.array([ [0.,1.] , [0.,0.]])
edge2 = np.array([ [0.,1.] , [1.,1.]])
edge_collision = edge_is_collision(edge1,edge2)
print('Parallel:')
print(f'Expected: False\nResults: {edge_collision}')

edge1 = np.array([ [0.,1.] , [0.,0.]])
edge2 = np.array([ [0.5,0.5] , [-0.5,1.]])
edge_collision = edge_is_collision(edge1,edge2)
print('\nCollision')
print(f'Expected: True\nResults: {edge_collision}')

edge1 = np.array([ [0.,1.] , [0.,0.]])
edge2 = np.array([ [0.5,0.5] , [0.,1.]])
edge_collision = edge_is_collision(edge1,edge2)
print('\nOn Edge')
print(f'Expected: False\nResults: {edge_collision}')

edge1 = np.array([ [0.,-1.] , [-1.,1.]])
edge2 = np.array([ [0.,-1.] , [5.,-0.5]])
edge_collision = edge_is_collision(edge1,edge2)
print('\nSharing One Vertex')
print(f'Expected: False\nResults: {edge_collision}')

print('\n/////////////////////////////////////////////////////////////////////')
print('/ Polygon is Self Occluded')
print('/////////////////////////////////////////////////////////////////////')
# Clockwise ordering aka hollow
# Point in polygon
vertex = np.array([0.,0.])
vertexPrev = np.array([-1.,-1.])
vertexNext = np.array([1.,-1.])
point = np.array([ [0.] , [1.] ])
self_occluded = polygon_is_self_occluded(vertex,vertexPrev,vertexNext,point)
print(f'Expected: True\nResults: {self_occluded}')

# Clockwise ordering aka hollow
# Point outside polygon
vertex = np.array([0.,0.])
vertexPrev = np.array([-1.,-1.])
vertexNext = np.array([1.,-1.])
point = np.array([ [0.] , [-1.] ])
self_occluded = polygon_is_self_occluded(vertex,vertexPrev,vertexNext,point)
print(f'\nExpected: False\nResults: {self_occluded}')

# Counter-Clockwise ordering aka filled
# Point outside polygon
vertex = np.array([0.,0.])
vertexPrev = np.array([1.,-1.])
vertexNext = np.array([-1.,-1.])
point = np.array([ [0.] , [1.] ])
self_occluded = polygon_is_self_occluded(vertex,vertexPrev,vertexNext,point)
print(f'\nExpected: False\nResults: {self_occluded}')

print('\n/////////////////////////////////////////////////////////////////////')
print('/ Polygon is Visible')
print('/////////////////////////////////////////////////////////////////////')
####### Visible Test #########
print('VISIBLE TEST')
vertices = np.array([ [0.,5.,5.,0.] , [-1.,-0.5,0.5,1.] ])
points = np.array([ [-1.] , [1.] ])

is_visible = polygon_is_visible(vertices,0,points)
print(f'\nExpected: True\nResults: {is_visible}')

# Plot values
_,ax = plt.subplots(1)
ax.set_ylim(-10, 10)
ax.set_xlim(-10, 10)
vertices = reshape_for_patch(vertices)
patch = patches.Polygon(vertices, facecolor='g', fill=True)
ax.add_patch(patch)
ax.plot(points[0],points[1],'bo', markersize=3)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(color='k', linestyle='-', linewidth=.5)

####### InVisible Test #########
print('\nINVISIBLE TEST')
vertices = np.array([ [0.,5.,5.,0.] , [-1.,-0.5,0.5,1.] ])
points = np.array([ [1.] , [0.2] ])

is_visible = polygon_is_visible(vertices,0,points)
print(f'\nExpected: False\nResults: {is_visible}')
# Plot values
_,ax = plt.subplots(1)
ax.set_ylim(-10, 10)
ax.set_xlim(-10, 10)
vertices = reshape_for_patch(vertices)
patch = patches.Polygon(vertices, facecolor='g', fill=True)
ax.add_patch(patch)
ax.plot(points[0],points[1],'bo', markersize=3)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(color='k', linestyle='-', linewidth=.5)

####### InVisible Test - On Edge #########
print('\nINVISIBLE TEST')
vertices = np.array([ [0.,5.,5.,0.] , [-1.,-0.5,0.5,1.] ])
points = np.array([ [0.] , [0.] ])

is_visible = polygon_is_visible(vertices,0,points)
print(f'\nExpected: True\nResults: {is_visible}')
# Plot values
_,ax = plt.subplots(1)
ax.set_ylim(-10, 10)
ax.set_xlim(-10, 10)
vertices = reshape_for_patch(vertices)
patch = patches.Polygon(vertices, facecolor='g', fill=True)
ax.add_patch(patch)
ax.plot(points[0],points[1],'bo', markersize=3)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(color='k', linestyle='-', linewidth=.5)

# Display plot
plt.show()

    
