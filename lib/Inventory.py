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

    def __init__(self,item_type,icon,r,c):
        super().__init__()
        self.setText(f'{item_type},{r},{c}')
        self.type = item_type
        self.icon = icon
        self.index = np.array([[r],[c]])

    def mousePressEvent(self,e):
        self.clicked_signal.emit(self.index)

class Inventory(QWidget,Colors,FilePaths):
    items = np.empty(24,dtype=object).reshape(4,6)

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

        self.generate_layout()

        self.setLayout(self.layout)

    def generate_layout(self):
        r,c = self.items.shape
        for i in range(0,r):
            for j in range(0,c):
                label = Item('t','png',i,j)
                label.setStyleSheet(f"font:bold 14px; color: {self.divider_color}")
                label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                label.clicked_signal.connect(self.inv_click)
                self.layout.addWidget(label,i,j)

    def inv_click(self,index):
        log(f'Inventory clicked: {index[0]},{index[1]}')
        
    def assign_item(self,item):
        self.items[0,0] = item