#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, math, numpy

from Utils import *
from PaintUtils import *
from Physics import *

class Player(QWidget,Colors,FilePaths):
    key_force = 8

    mass = 1
    force = [0,0]
    drag = 2

    velocity = 0
    acceleration = 4

    prev_direction = 0

    info_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pose = [600,600]
        self.player_pixmap = None

        self.geom = 'player.svg'
        self.set_geometry(self.geom)
        self.prev_geom = self.geom

        self.physics = Physics(12.0)
        self.physics.info_signal.connect(self.send_info)
    
    def send_info(self,info):
        self.info_signal.emit(info)

    def set_geometry(self,img):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/{img}')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]
        log('Player size: {}'.format(self.size))

    def update_position(self,key_press,width,height):
        if len(key_press) != 0:
            self.force = [0,0]
            for key in key_press:
                if key == 'right':
                    self.force[0] = self.key_force
                    self.geom = 'player_right.svg'            
                elif key == 'left':
                    self.force[0] = -self.key_force
                    self.geom = 'player_left.svg'
                elif key == 'up':
                    self.force[1] = -4*self.key_force
                elif key == 'down':
                    self.force[1] = self.key_force
                else:
                    log('Player pose update. Key not recognized...',color='r')
        else:
            self.force = [0,0]
        
        self.physics.accelerate(self.force)
        self.pose[0] += self.physics.velocity[0] 
        self.pose[1] += self.physics.velocity[1] 

        ### Checking bounds of environment
        if self.pose[0]+self.size[0] > width:
            self.pose[0] = width-self.size[0]
        elif self.pose[0] < 0:
            self.pose[0] = 0
    
        if self.pose[1] < 0:
            self.pose[1] = 0
        elif self.pose[1]+self.size[1] > height:
            self.pose[1] = height-self.size[1]

        if abs(self.physics.velocity[0]) < .7:
            self.geom = 'player.svg'
        
        ### Updating player image
        if self.geom != self.prev_geom:
            self.set_geometry(self.geom)
        self.prev_geom = self.geom

    def animate(self):
        pass