#!/usr/bin/env python3

import os
import sys
import time
import datetime as dt
from threading import Thread
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DarkColors():
    ###################################################
    # Game Colors
    ###################################################
    brown = {'hex':'#996633','rgb':[153,102,51]}
    sky_blue = {'hex':'#1BADDE','rgb':[27,173,222]}
    midnight_blue = {'hex':'#051962','rgb':[5,25,98]}
    star_gold = {'hex':'#F7D31E','rgb':[247, 211, 30]}
    white = {'hex':'#FFFFFF','rgb':[255,255,255]}

    ###################################################
    # Welcome Screen Colors
    ###################################################
    divider_color = '#ff9955'
    background_color = '#353535'
    warning_text = '#FB0101'

    def __init__(self):
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(self.background_color))
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.palette.setColor(QPalette.ToolTipText, Qt.white)
        self.palette.setColor(QPalette.Text, Qt.white)
        self.palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ButtonText, QColor(255, 153, 85)) #Qt.white
        self.palette.setColor(QPalette.BrightText, Qt.red)
        self.palette.setColor(QPalette.Link, QColor(255, 153, 85))
        self.palette.setColor(QPalette.Highlight, QColor(255, 153, 85))
        self.palette.setColor(QPalette.HighlightedText, Qt.black)

class Colors():
    ###################################################
    # Game Colors
    ###################################################
    brown = {'hex':'#996633','rgb':[153,102,51]}
    sky_blue = {'hex':'#1BADDE','rgb':[27,173,222]}
    midnight_blue = {'hex':'#051962','rgb':[5,25,98]}
    star_gold = {'hex':'#F7D31E','rgb':[247, 211, 30]}
    white = {'hex':'#FFFFFF','rgb':[255,255,255]}

    ###################################################
    # Welcome Screen Colors
    ###################################################
    divider_color = '#ff9955'
    background_color = '#353535'
    warning_text = '#FB0101'

    def __init__(self):
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(self.background_color))
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.palette.setColor(QPalette.ToolTipText, Qt.white)
        self.palette.setColor(QPalette.Text, Qt.white)
        self.palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ButtonText, QColor(255, 153, 85)) #Qt.white
        self.palette.setColor(QPalette.BrightText, Qt.red)
        self.palette.setColor(QPalette.Link, QColor(255, 153, 85))
        self.palette.setColor(QPalette.Highlight, QColor(255, 153, 85))
        self.palette.setColor(QPalette.HighlightedText, Qt.black)