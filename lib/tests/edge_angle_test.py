#!/usr/bin/env python3

import random, sys, os, math, time, numpy
import pathlib

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))

try:
    from Utils import *
    from Geometry import *
except:
    print('Could not run test! Are you running from the tests/ folder?')


ang1 = 0.
ang2 = 0.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')

ang1 = 0.
ang2 = 7.
same_edges_angle = edge_angle('angle',ang1,ang2)
print(f'\nAngles: {ang1} & {ang2}\nResults: {same_edges_angle}')