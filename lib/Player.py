#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math

from Utils import *
from PaintUtils import *

class Player(QWidget,Colors,FilePaths):
    speed = 8
    gravity_accel = 6

    mass = 1
    force = 1
    drag = 2

    velocity = 0
    acceleration = 4

    prev_direction = 0

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pose = [600,600]
        self.player_pixmap = None

        self.geom = 'player.svg'
        self.set_geometry(self.geom)
        self.prev_geom = self.geom

    def set_geometry(self,img):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/{img}')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]
        log('Player size: {}'.format(self.size))

    def update_position(self,key_press,width,height):
        if len(key_press) == 0:
            return
        
        # self.pose[1] += 10
        for key in key_press:
            if key == 'right':
                self.pose[0] += 1*self.speed
                if self.pose[0]+self.size[0] > width:
                    self.pose[0] = width-self.size[0]
                self.geom = 'player_right.svg'
                
            elif key == 'left':
                self.pose[0] -= 1*self.speed
                if self.pose[0] < 0:
                    self.pose[0] = 0
                self.geom = 'player_left.svg'

            elif key == 'up':
                self.pose[1] -= 2*self.speed
                if self.pose[1] < 0:
                    self.pose[1] = 0

            elif key == 'down':
                self.pose[1] += 2*self.speed
                if self.pose[1]+self.size[1] > height:
                    self.pose[1] = height-self.size[1]

            else:
                log('Player pose update. Key not recognized...',color='r')
            
            if self.geom != self.prev_geom:
                self.set_geometry(self.geom)
            self.prev_geom = self.geom

    def gravity(self):
        self.pose[1] += 1*self.gravity_accel
        pass

    def animate(self):
        pass