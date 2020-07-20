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
from PyQt5 import uic

from Utils import *
from PaintUtils import *


class Divider(QWidget,Colors,FilePaths):

    def __init__(self,text,top_spacer = True, bottom_spacer = False):
        super().__init__()
        self.layout = QVBoxLayout()

        if top_spacer:
            # Spacer 1
            self.spacer1 = QLabel()
            # self.spacer1.setStyleSheet()
            # self.spacer1.setFixedHeight(3)
            self.layout.addWidget(self.spacer1)

        # Divider
        self.divider = QLabel(f'{text}:')
        self.divider.setStyleSheet(f"font:bold italic 24px; color: {self.background_color}; background-color: {self.divider_color}")
        # self.divider.setFixedHeight(3)
        self.layout.addWidget(self.divider)

        if bottom_spacer:
            # Spacer 2
            self.spacer2 = QLabel()
            # self.spacer2.setStyleSheet()
            # self.spacer1.setFixedHeight(3)
            self.layout.addWidget(self.spacer2)

        # Set widget layout
        self.setLayout(self.layout)

class FormEntry(): 

    def __init__(self,label_text,return_press = None):
        super().__init__()
        self.form = QHBoxLayout()

        label_text = label_text + ':'
        self.form_line_label = QLabel(label_text)
        self.form_line_label.setStyleSheet("font: 16px")
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.form.addWidget(self.form_line_label,1)

        self.form_line_edit = QLineEdit()
        self.form_line_edit.setStyleSheet("font: 16px")
        self.form.addWidget(self.form_line_edit,3)

        if return_press:
            self.connect_return(return_press)
        
    def connect_return(self,fn):
        self.form_line_edit.returnPressed.connect(fn)
        
class WarningPrompt(QWidget,Colors,FilePaths):

    def __init__(self,text,rect = None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        if rect:
            self.setGeometry(rect)
        else:
            self.setGeometry(400,400,200,200)

        self.warning_label = QLabel('Warning:')
        self.warning_label.setStyleSheet(f"font:bold italic 24px; color: {self.warning_text}")
        self.warning_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout.addWidget(self.warning_label)

        self.label = QLabel(text)
        self.label.setStyleSheet(f"font:bold italic 14px")
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.ok_button = QPushButton('OK')
        self.ok_button.setStyleSheet("font: 14px")
        self.ok_button.clicked.connect(self.close_window)
        self.ok_button.setDefault(True)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
        self.show()

    def close_window(self):
        self.close()

class Prompt(QWidget,Colors,FilePaths):
    def __init__(self,ui_file):
        super().__init__()
        uic.loadUi(f'{self.user_path}ui/{ui_file}', self)

        self.show()
    
class ControlButton(QPushButton,Colors,FilePaths):

    def __init__(self,text,fn = None, default = False):
        super().__init__()

        self.setText(text)
        self.setFixedSize(150,30)

        if fn:
            self.clicked.connect(fn)
        
        if default:
            self.setDefault(True)

class KeyboardShortcuts(QWidget,Colors,FilePaths):

    def __init__(self,rect=None):
        super().__init__()
        self.setWindowTitle('Keyboard Controls')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        if rect:
            self.setGeometry(rect)
        else:
            self.setGeometry(200,200,600,600)

        self.controls_label = QLabel('Controls:')
        self.controls_label.setStyleSheet(f"font:bold italic 24px")
        self.controls_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.layout.addWidget(self.controls_label)

        self.controls_list_layout = QHBoxLayout()

        self.controls_list = QListWidget()
        control_list = ['Up','Down','Left','Right','Save and exit','End turn','Previous scene','Advance scene']
        self.controls_list.addItems(control_list)
        self.controls_list_layout.addWidget(self.controls_list)
        self.controls_list.itemClicked.connect(self.link_lists)

        self.button_list = QListWidget()
        control_buttons = 'W','S','A','D','ESC','N','B','M'
        self.button_list.addItems(control_buttons)
        self.controls_list_layout.addWidget(self.button_list)
        
        self.layout.addLayout(self.controls_list_layout)

        self.ok_button = QPushButton('Close')
        self.ok_button.clicked.connect(self.close_window)
        self.ok_button.setDefault(True)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
        self.show()

    def link_lists(self):
        curr_row = self.controls_list.currentRow()
        self.button_list.setCurrentRow(curr_row)

    def close_window(self):
        self.close()

class PhysicsDisplay(QWidget,Colors,FilePaths):
    clear_keys = pyqtSignal()

    def __init__(self,rect=None):
        super().__init__()
        self.setWindowTitle('Physics Stats')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)

        self.label = QLabel('...')
        self.label.setStyleSheet(f"font:bold 16px")
        self.layout.addWidget(self.label)

        self.setGeometry(0,0,500,200)
        self.setLayout(self.layout)

        self.setFocusPolicy(Qt.NoFocus)
        
        self.show()

        self.clear_keys.emit()

    def update(self,info,keys_pressed):
        info_str = ''
        for key,val in list(info.physics_info.items()):
            if type(val) == list:
                key = str(key)
                # val = str(val)
                info_str = info_str + '%30s | '%(self.key)
                for item in val:
                    item = float(item)
                    info_str = info_str + '%-.2f\n'%(item)
                info_str = info_str + '\n'
            else:
                key = str(key)
                val = str(val)
                info_str = info_str + '%30s | %-50s\n'%(key,val)
        info_str = info_str + 'Keys pressed | {}\n'.format(keys_pressed)
            
        self.label.setText(info_str)

        self.clear_keys.emit()

    