#!/usr/bin/env python3

import random, sys, os, math, time
from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

import ctypes

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))

from Geometry import *
from Utils import *


class CollisionCheckTest(FilePaths):

    def __init__(self):
        super().__init__()

        self.poly1 = Polygon()
        self.poly1.unit_circle(4,2)
        self.poly1.translate(10,0)
        # print(f'Array is:\n{self.poly1.vertices}')

        self.poly2 = Polygon()
        self.poly2.unit_circle(4,2)

        self.c_float_p = ctypes.POINTER(ctypes.c_double)

        self.fun = ctypes.CDLL(f'{os.path.dirname(path)}/cc_lib.so')   
                    
        self.fun.polygon_is_collision.argtypes = [self.c_float_p,ctypes.c_int,ctypes.c_int,self.c_float_p,ctypes.c_int,ctypes.c_int] 
    
    def run_test(self):
        tic = time.time()

        data = self.poly1.vertices.copy() #numpy.array([[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]])
        data = data.astype(np.double)
        data_p = data.ctypes.data_as(self.c_float_p)

        data2 = self.poly2.vertices.copy() #numpy.array([[0.1, 0.1], [0.2, 0.2], [0.3, 0.3]])
        data2 = data2.astype(np.double)
        data_p2 = data2.ctypes.data_as(self.c_float_p)

        # C function call in python

        returnVale = self.fun.polygon_is_collision(data_p,2,4,data_p2,2,4)
        toc = time.time()    
        print(f'C function took: {toc-tic}')
        print(f'Collision result: {returnVale}')

        # Python function call
        tic = time.time()
        res = polygon_is_collision(self.poly1,self.poly2)
        toc = time.time()

        print(f'Python function took: {toc-tic}')
        print(f'Collision result: {res}')

def main():
    obj = CollisionCheckTest()
    obj.run_test()

if __name__ == '__main__':
    main()