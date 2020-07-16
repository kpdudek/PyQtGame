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
    speed = 8
    grav_accel = 2

    mass = 1
    force = [0,0]
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

        self.physics = Physics(15.0)

    def set_geometry(self,img):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/{img}')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]
        log('Player size: {}'.format(self.size))

    def update_position(self,key_press,width,height):
        if len(key_press) == 0:
            self.force = [0,self.grav_accel]
            # pass
            # return
        else:
            for key in key_press:
                if key == 'right':
                    # self.pose[0] += 1*self.speed
                    self.force[0] += 1
                    self.geom = 'player_right.svg'            
                elif key == 'left':
                    # self.pose[0] -= 1*self.speed
                    self.force[0] -= 1
                    self.geom = 'player_left.svg'
                elif key == 'up':
                    # self.pose[1] -= 2*self.speed
                    self.force[1] -= 4
                elif key == 'down':
                    # self.pose[1] += 2*self.speed
                    self.force[1] += 1
                else:
                    log('Player pose update. Key not recognized...',color='r')

        # self.gravity()
        self.drag()

        self.physics.accelerate(self.force)
        self.pose[0] += math.ceil(self.physics.velocity[0])
        self.pose[1] += math.ceil(self.physics.velocity[1])

        ### Checking bounds of environment
        if self.pose[0]+self.size[0] > width:
            self.pose[0] = width-self.size[0]
        elif self.pose[0] < 0:
            self.pose[0] = 0
    
        if self.pose[1] < 0:
            self.pose[1] = 0
        elif self.pose[1]+self.size[1] > height:
            self.pose[1] = height-self.size[1]

        if abs(self.physics.velocity[0]) < .1:
            self.geom = 'player.svg'
        
        ### Updating player image
        if self.geom != self.prev_geom:
            self.set_geometry(self.geom)
        self.prev_geom = self.geom

    def gravity(self):
        # self.pose[1] += 1*self.gravity_accel
        self.force[1] += self.grav_accel
        pass

    def drag(self):
        sign = -1 * numpy.sign(self.physics.velocity[0])
        # print('{}'.format(sign * 0.6 * self.physics.velocity[0]))
        self.force[0] += sign * 0.3 * abs(self.physics.velocity[0])


    def animate(self):
        pass