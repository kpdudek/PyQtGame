#!/usr/bin/env python3

import random, sys, os, math, time
from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))

import Utils as util
import Geometry as geom


def polygon_is_collision_speed_test():
    '''
    Determine how long it takes for the concave capable polygon collision check
    call takes
    '''
    print('---------- Polygon Collision checking speed test ----------')
    poly1 = geom.Polygon()
    poly1.unit_circle(5,2,translate=[2,0])
    poly2 = geom.Polygon()
    poly2.unit_circle(8,2)

    num_players = 1.
    num_obstacles = 2.
    fps_multiplier = 1./((4*num_players)+(2*num_obstacles))

    tic = time.time()
    collis_res = geom.polygon_is_collision(poly1,poly2)
    toc = time.time()

    print(f'Collision checking took (s): {toc-tic}')
    print(f'Results: {collis_res.any()}')
    try:
        print(f'FPS: {(1./(toc-tic))*fps_multiplier}')
    except:
        print("Couldn't compute FPS...")

    geom.polygon_plot(poly1.vertices.copy(),points=poly2.vertices.copy(),title=f'Collision Result: {collis_res}')

def polygon_is_collision_vertices_test():
    '''
    Determine how long it takes for the concave capable polygon collision check
    call takes
    '''
    print('---------- Polygon Collision checking speed test ----------')
    
    poly1 = np.array([[200.,200.,225.,225.],[77.33333333,27.33333333,27.33333333,77.33333333]])
    poly2 = np.array([[0.,0.,1800.,1800.],[50.,0.,0.,50.]])

    # Vertices:
    # [[ 200.          200.          225.          225.        ]
    # [  77.33333333   27.33333333   27.33333333   77.33333333]]
    # Obstacle1:
    # [[    0.     0.  1800.  1800.]
    # [   50.     0.     0.    50.]]

    collis_res = geom.polygon_is_collision(poly2,poly1)

    print(f'Results: {collis_res.any()}')

    geom.polygon_plot(poly2,points=poly1,lim=2000,title=f'Collision Result: {collis_res}')

def proximity_check_test():
    print('---------- Proximity Checking Test ----------')

def main():
    # Run test cases

    polygon_is_collision_speed_test()
    polygon_is_collision_vertices_test()
    # proximity_check_test()

    # Show plots
    plt.show()

if __name__ == '__main__':
    main()