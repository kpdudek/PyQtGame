#!/usr/bin/env python3

import random, sys, os, math, time, numpy

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
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')

ang1 = 0.
ang2 = 7.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')

ang1 = 0.2
ang2 = 6.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')

print('/////////////////////////////////////////////////////////////////////')
print('/ Edge Collision Tests')
print('/////////////////////////////////////////////////////////////////////')
# Parallel
p1 = np.array([0,0])
p2 = np.array([1,0])
p3 = np.array([0,1])
p4 = np.array([1,1])
edge_collision = edge_is_collision(p1,p2,p3,p4)
print('\nParallel:')
print(f'Expected: False\nResults: {edge_collision}')

# Not in collision
p1 = np.array([0,0])
p2 = np.array([1,0])
p3 = np.array([0,1])
p4 = np.array([1,3])
edge_collision = edge_is_collision(p1,p2,p3,p4)
print('\nNo collision:')
print(f'Expected: False\nResults: {edge_collision}')

# In collision
p1 = np.array([0,0])
p2 = np.array([1,0])
p3 = np.array([.5,-.5])
p4 = np.array([.5,.5])
edge_collision = edge_is_collision(p1,p2,p3,p4)
print('\nIn collison:')
print(f'Expected: True\nResults: {edge_collision}')

# Edge collision
p1 = np.array([0,0])
p2 = np.array([1,0])
p3 = np.array([.5,0])
p4 = np.array([.5,2])
edge_collision = edge_is_collision(p1,p2,p3,p4)
print('\nEdge collison:')
print(f'Expected: True\nResults: {edge_collision}')