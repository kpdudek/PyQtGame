#!/usr/bin/env python3

import os, sys, time, math
import numpy as np
import datetime as dt
from threading import Thread
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from Utils import *
from PaintUtils import *

class Item(QLabel,Colors,FilePaths):
    clicked_signal = pyqtSignal(object)

    def __init__(self,sprite,r,c,):
        super().__init__()
        self.sprite = sprite
        self.index = np.array([[r],[c]])

        if sprite:
            self.set_pixmap()

    def set_pixmap(self):
        # print(self.sprite.pixmaps[self.sprite.idx])
        self.setPixmap(self.sprite.pixmaps[self.sprite.idx])

    def add_pixmap(self,sprite):
        self.sprite = sprite
        self.set_pixmap()
    
    def mousePressEvent(self,e):
        self.clicked_signal.emit(self.index)

class Inventory(QWidget,Colors,FilePaths):
    '''
    Inventory entries are sprites
    '''
    def __init__(self,screen_width,screen_height):
        super().__init__()
        self.setWindowTitle('Inventory')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.auto_fill_background = True

        self.layout = QGridLayout()

        self.width = 800
        self.height = 600
        self.geom = QRect(math.floor((screen_width-self.width)/2), math.floor((screen_height-self.height)/2), self.width, self.height)
        self.setGeometry(self.geom) 

        self.full = False
        self.items = np.empty(6,dtype=object).reshape(2,3)
        self.r_max,self.c_max = self.items.shape
        self.generate_layout()
        self.idx = np.array([[0],[0]])

        self.setLayout(self.layout)

    def generate_layout(self):
        for i in range(0,self.r_max):
            for j in range(0,self.c_max):
                label = Item(None,i,j)
                label.setStyleSheet(f"font:bold 14px; color: {self.divider_color}")
                label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                label.clicked_signal.connect(self.inv_click)
                self.items[i,j] = label
                self.layout.addWidget(label,i,j)

    def add_item(self,sprite):
        r,c = self.idx
        if (r == self.r_max) and (c == self.c_max):
            if not self.full:
                self.full = True
                log('Inventory filled up!')
            return
        else:
            self.items[r,c][0].add_pixmap(sprite)
        
        if (r == self.r_max-1) and (c != self.c_max-1):
            self.idx[0] = 0
            self.idx[1] += 1
        elif (r == self.r_max-1) and (c == self.c_max-1):
            self.idx[0] += 1
            self.idx[1] += 1
        else:
            self.idx[0] += 1
        
    def inv_click(self,index):
        log(f'Clicked: {self.items[index[0],index[1]][0].sprite.name} at index {index[0]},{index[1]}')
        
    def assign_item(self,item):
        self.items[0,0] = item