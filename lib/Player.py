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
    gravity_accel = 4

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pose = [200,600]
        self.player_pixmap = None

        self.set_geometry()

    def set_geometry(self):
        self.player_pixmap = QPixmap(f'{self.user_path}graphics/player.svg')
        self.size = [self.player_pixmap.size().width(),self.player_pixmap.size().height()]
        log('Player size: {}'.format(self.size))

    def update_position(self,key_press):
        if len(key_press) == 0:
            return
        
        # self.pose[1] += 10
        for key in key_press:
            if key == 'right':
                self.pose[0] += 1*self.speed
            elif key == 'left':
                self.pose[0] -= 1*self.speed
            elif key == 'up':
                self.pose[1] -= 2*self.speed
            elif key == 'down':
                self.pose[1] += 2*self.speed
            else:
                log('Player pose update. Key not recognized...',color='r')

    def gravity(self):
        self.pose[1] += 1*self.gravity_accel
        pass

    def animate(self):
        pass