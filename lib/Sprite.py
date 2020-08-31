#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math, time
import numpy as np
from multiprocessing import Pool
import ctypes

from Utils import *
from PaintUtils import *
from Physics import *
from Geometry import *


class Sprite(QWidget,Colors,FilePaths):
    idx = 0
    pixmaps = []
    sizes = []
    polys = []
    centroid_offsets = []

    pose = np.array([ [200.] , [200.] ])

    freq = 1./8.0 #Hz

    def __init__(self,folder,scale=None):
        super().__init__()

        for png in sorted(os.listdir(f'{self.user_path}graphics/{folder}')):
            print(png)
            pix = QPixmap(f'{self.user_path}graphics/{folder}/{png}')

            pix = pix.transformed(QTransform().scale(-1, 1))
            
            if scale:
                pix = pix.scaled(scale, scale, Qt.KeepAspectRatio)
            self.pixmaps.append(pix)

            size = [pix.size().width(),pix.size().height()]
            self.sizes.append(size)

            poly = Polygon()
            bot_right = np.array([self.pose[0]+size[0],self.pose[1]+size[1]])
            poly.rectangle(self.pose,bot_right)
            self.polys.append(poly)

            self.centroid_offsets.append(self.pose - poly.sphere.pose)
            
        self.set_pixmap()

        self.time = time.time()

    def direction(self,dir):
        pass

    def set_pixmap(self):
        self.pixmap = self.pixmaps[self.idx]
    
    def animate(self):
        split_t = time.time()

        if split_t-self.time > self.freq:
            
            self.idx += 1
            if self.idx > len(self.pixmaps)-1:
                self.idx = 0
            self.time = split_t
        
        self.set_pixmap()

            