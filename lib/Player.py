#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math

from Utils import *
from PaintUtils import *

class Player(QWidget,Colors,FilePaths):
    speed = 10
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pose = [200,200]
        self.player_pixmap = None

        self.set_geometry()

    def set_geometry(self):

        self.player_pixmap = QPixmap(f'{self.user_path}graphics/player.svg')

    def update_position(self,key_press):
        if key_press == None:
            return
        
        # self.pose[1] += 10
        if key_press == 'right':
            self.pose[0] += 1*self.speed
        elif key_press == 'left':
            self.pose[0] -= 1*self.speed
        elif key_press == 'up':
            self.pose[1] -= 1*self.speed
        elif key_press == 'down':
            self.pose[1] += 1*self.speed
        else:
            log('Player pose update. Key not recognized...',color='r')
