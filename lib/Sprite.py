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


class Sprite(FilePaths):
    idx = 0
    pixmaps = []
    sizes = []
    polys = []
    centroid_offsets = []

    pose = np.array([ [200.] , [200.] ])

    freq = 1./8.0 #Hz

    ang = 180. # Degrees from 0 at horizontal right

    def __init__(self,folder,scale=None,physics=None):
        super().__init__()

        for png in sorted(os.listdir(f'{self.user_path}graphics/{folder}')):
            pix = QPixmap(f'{self.user_path}graphics/{folder}/{png}')
            if scale:
                pix = pix.scaled(scale, scale, Qt.KeepAspectRatio)
            
            size = [pix.size().width(),pix.size().height()]
            self.sizes.append(size)
            self.pixmaps.append(pix.copy(self.pose[0],self.pose[1],size[0],size[1]))

            poly = Polygon()
            bot_right = np.array([self.pose[0]+size[0],self.pose[1]+size[1]])
            poly.rectangle(self.pose,bot_right)
            self.polys.append(poly)

            self.centroid_offsets.append(self.pose - poly.sphere.pose)
        
        if physics:
            self.physics = Physics(physics['mass'],physics['max_vel'])

        self.set_pixmap()
        self.time = time.time()

    def direction(self,ang):
        if ang == self.ang:
            return
        
        elif (ang < 90.) or (ang > 270.): # Right half
            if not (self.ang < 90.) or (self.ang > 270.):
                for idx,pix in enumerate(self.pixmaps):
                    self.pixmaps[idx] = pix.transformed(QTransform().scale(-1, 1))

        elif (ang > 90.) and (ang < 270.): # Left half
            if not (self.ang > 90.) and (self.ang < 270.):
                for idx,pix in enumerate(self.pixmaps):
                    self.pixmaps[idx] = pix.transformed(QTransform().scale(-1, 1))

        elif (ang == 90.): # Facing up
            pass

        elif (ang == 270.): # Facing forwards
            pass

        self.ang = ang

    def set_pixmap(self):
        self.pixmap = self.pixmaps[self.idx]
    
    def animate(self,vel):
        split_t = time.time()

        if vel > 0.08:
            self.freq = 1./(30*abs(vel))
        else:
            self.freq = 1./(6.)
        
        if split_t-self.time > self.freq:
            
            self.idx += 1
            if self.idx > len(self.pixmaps)-1:
                self.idx = 0
            self.time = split_t
        
            self.set_pixmap()
            
class OBSSprite(FilePaths):
    idx = 0
    pixmaps = []
    sizes = []
    polys = []
    centroid_offsets = []

    pose = np.array([ [200.] , [200.] ])

    freq = 1./8.0 #Hz

    ang = 180. # Degrees from 0 at horizontal right

    def __init__(self,folder,scale=None,physics=None):
        super().__init__()

        for png in sorted(os.listdir(f'{self.user_path}graphics/{folder}')):
            pix = QPixmap(f'{self.user_path}graphics/{folder}/{png}')
            if scale:
                pix = pix.scaled(scale, scale, Qt.KeepAspectRatio)
            
            size = [pix.size().width(),pix.size().height()]
            self.sizes.append(size)
            self.pixmaps.append(pix.copy(self.pose[0],self.pose[1],size[0],size[1]))

            poly = Polygon()
            bot_right = np.array([self.pose[0]+size[0],self.pose[1]+size[1]])
            poly.rectangle(self.pose,bot_right)
            self.polys.append(poly)

            self.centroid_offsets.append(self.pose - poly.sphere.pose)
        
        if physics:
            self.physics = Physics(physics['mass'],physics['max_vel'])

        self.set_pixmap()
        self.time = time.time()

    def direction(self,ang):
        if ang == self.ang:
            return
        
        elif (ang < 90.) or (ang > 270.): # Right half
            if not (self.ang < 90.) or (self.ang > 270.):
                for idx,pix in enumerate(self.pixmaps):
                    self.pixmaps[idx] = pix.transformed(QTransform().scale(-1, 1))

        elif (ang > 90.) and (ang < 270.): # Left half
            if not (self.ang > 90.) and (self.ang < 270.):
                for idx,pix in enumerate(self.pixmaps):
                    self.pixmaps[idx] = pix.transformed(QTransform().scale(-1, 1))

        elif (ang == 90.): # Facing up
            pass

        elif (ang == 270.): # Facing forwards
            pass

        self.ang = ang

    def set_pixmap(self):
        self.pixmap = self.pixmaps[self.idx]
    
    def animate(self,vel):
        split_t = time.time()

        if vel > 0.08:
            self.freq = 1./(30*abs(vel))
        else:
            self.freq = 1./(6.)
        
        if split_t-self.time > self.freq:
            
            self.idx += 1
            if self.idx > len(self.pixmaps)-1:
                self.idx = 0
            self.time = split_t
        
            self.set_pixmap()