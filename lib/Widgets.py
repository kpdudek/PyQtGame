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


class Divider(QWidget,Colors,FilePaths):

    def __init__(self,text,top_spacer = True, bottom_spacer = False):
        super().__init__()
        self.layout = QVBoxLayout()

        if top_spacer:
            # Spacer 1
            self.spacer1 = QLabel()
            self.layout.addWidget(self.spacer1)

        # Divider
        self.divider = QLabel(f'{text}:')
        self.divider.setStyleSheet(f"font:bold italic 24px; color: {self.title_white}; background-color: {self.title_blue}")
        self.layout.addWidget(self.divider)

        if bottom_spacer:
            # Spacer 2
            self.spacer2 = QLabel()
            self.layout.addWidget(self.spacer2)

        # Set widget layout
        self.setLayout(self.layout)

class FormEntry(): 

    def __init__(self,label_text,return_press = None,line_edit_text = None):
        super().__init__()
        self.widget = QWidget()
        self.form = QHBoxLayout()

        label_text = label_text + ':'
        self.form_line_label = QLabel(label_text)
        self.form_line_label.setStyleSheet("font: 16px")
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.form.addWidget(self.form_line_label,1)

        self.form_line_edit = QLineEdit()
        if line_edit_text:
            self.form_line_edit.setText(line_edit_text)
        self.form_line_edit.setStyleSheet("font: 16px")
        self.form.addWidget(self.form_line_edit,3)

        self.widget.setLayout(self.form)

        if return_press:
            self.connect_return(return_press)
        
    def connect_return(self,fn):
        self.form_line_edit.returnPressed.connect(fn)

class ComboEntry(): 

    def __init__(self,label_text,combo_list,fn = None):
        super().__init__()
        self.widget = QWidget()
        self.form = QHBoxLayout()

        label_text = label_text + ':'
        self.form_line_label = QLabel(label_text)
        self.form_line_label.setStyleSheet("font: 16px")
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.form.addWidget(self.form_line_label,1)

        self.form_combo = QComboBox()
        self.form_combo.addItems(combo_list)
        self.form_combo.setStyleSheet("font: 16px")
        self.form.addWidget(self.form_combo,3)

        self.widget.setLayout(self.form)

        if fn:
            self.connect_fn(fn)

    def connect_fn(self,fn):
        self.form_combo.activated[str].connect(fn)

class SpinEntry(): 

    def __init__(self,label_text):
        super().__init__()
        self.widget = QWidget()
        self.form = QHBoxLayout()

        label_text = label_text + ':'
        self.form_line_label = QLabel(label_text)
        self.form_line_label.setStyleSheet("font: 16px")
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.form.addWidget(self.form_line_label,1)

        self.form_spin = QSpinBox()
        self.form_spin.setRange(-800,800)
        self.form_spin.setSingleStep(10)
        # self.form_spin.addItems(combo_list)
        self.form_spin.setStyleSheet("font: 16px")
        self.form.addWidget(self.form_spin,3)

        self.widget.setLayout(self.form)
        
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
    def __init__(self,ui_file,screen_width,screen_height):
        super().__init__()
        uic.loadUi(f'{self.user_path}ui/{ui_file}', self)

        width = self.geometry().width()
        height = self.geometry().height()
        self.move(math.floor((screen_width-width)/2), math.floor((screen_height-height)/2))

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

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

        self.auto_fill_background = True

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        if rect:
            self.setGeometry(rect)
        else:
            self.setGeometry(0,0,400,400)

        self.controls_label = QLabel('Controls:')
        self.controls_label.setStyleSheet(f"font:bold italic 24px")
        self.controls_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.layout.addWidget(self.controls_label)

        self.controls_list_layout = QHBoxLayout()

        self.controls_list = QListWidget()
        control_list = ['Up','Down','Left','Right','Save and exit','End turn','Previous scene','Advance scene','Pause','Sprint']
        self.controls_list.addItems(control_list)
        self.controls_list_layout.addWidget(self.controls_list)
        self.controls_list.itemClicked.connect(self.link_lists)

        self.button_list = QListWidget()
        control_buttons = ['W','S','A','D','ESC','N','B','M','P','Shift']
        self.button_list.addItems(control_buttons)
        self.controls_list_layout.addWidget(self.button_list)
        self.button_list.itemClicked.connect(self.link_button_list)
        
        self.layout.addLayout(self.controls_list_layout)

        self.ok_button = QPushButton('Close')
        self.ok_button.clicked.connect(self.close_window)
        # self.ok_button.setDefault(True)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def link_lists(self):
        curr_row = self.controls_list.currentRow()
        self.button_list.setCurrentRow(curr_row)

    def link_button_list(self):
        curr_row = self.button_list.currentRow()
        self.controls_list.setCurrentRow(curr_row)

    def close_window(self):
        self.close()

class PhysicsDisplay(QWidget,Colors,FilePaths):

    def __init__(self,rect=None):
        super().__init__()
        self.setWindowTitle('Physics Stats')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(0,0,400,200)

        self.auto_fill_background = False

        self.layout = QVBoxLayout()

        self.title_label = QLabel('Game Physics Output')
        self.title_label.setStyleSheet(f"font:bold italic 28px; color: {self.divider_color}")
        self.title_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.divider = QLabel('')
        self.divider.setStyleSheet(f"background-color: {self.white['hex']}")
        self.divider.setFixedHeight(2)
        self.layout.addWidget(self.divider)

        self.physics_layout = QHBoxLayout()

        self.left_label = QLabel('...')
        self.left_label.setStyleSheet(f"font:bold 16px")
        self.left_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.physics_layout.addWidget(self.left_label)

        self.right_label = QLabel('...')
        self.right_label.setStyleSheet(f"font:bold 16px")
        self.right_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.physics_layout.addWidget(self.right_label)

        self.key_label = QLabel('...')
        self.key_label.setStyleSheet(f"font:bold 16px")
        self.key_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)

        self.collision_label = QLabel('...')
        self.collision_label.setStyleSheet(f"font:bold 16px")
        self.collision_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)

        self.state_label = QLabel('...')
        self.state_label.setStyleSheet(f"font:bold 16px")
        self.state_label.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)

        self.layout.addLayout(self.physics_layout)
        self.layout.addWidget(self.key_label)
        self.layout.addWidget(self.collision_label)
        self.layout.addWidget(self.state_label)
        self.setLayout(self.layout)

    def update(self,info,keys_pressed,collision,state,pose):
        left_info_str = ''
        right_info_str = ''

        # print(info.physics_info)
        if info != '':
            for key,val in info.physics_info.items():
                new_left_line = ''
                new_right_line = ''

                new_left_line = '%s'%(key)
                if type(val) == list:
                    new_right_line += '['
                    for item in val:
                        item = float(item)
                        new_right_line += '%-.2f '%(item)
                    new_right_line += ']'
                
                elif type(val) == np.ndarray:
                    new_right_line += '['
                    for item in val:
                        item = float(item)
                        new_right_line += '%-.2f '%(item)
                    new_right_line += ']'

                else:
                    try:
                        val = float(val)
                        new_right_line += '%-.2f'%(val)
                    except:
                        val = str(val)
                        new_right_line += '%s'%(val)

                new_left_line += '\n'
                new_right_line += '\n'

                left_info_str += new_left_line
                right_info_str += new_right_line 
            left_info_str += 'Pose\n'
            right_info_str += '[%-.0f %-.0f]\n'%(pose[0],pose[1])

            self.left_label.setText(left_info_str)
            self.right_label.setText(right_info_str)

        key_str = 'Keys pressed: {}\n'.format(keys_pressed)
        collision_str = f'Collision: [{collision[0]} {collision[1]}]'

        if state == True:
            state_str = 'Game is: Running'
        else:
            state_str = 'Game is: Paused'
            
        self.key_label.setText(key_str)
        self.collision_label.setText(collision_str)
        self.state_label.setText(state_str)


class ObstaclesDisplay(QWidget,Colors,FilePaths):

    def __init__(self,dynamic_obstacles):
        super().__init__()
        self.setWindowTitle('Obstacles Manager')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.dynamic_obstacles = dynamic_obstacles

        self.auto_fill_background = True

        uic.loadUi(f'{self.user_path}ui/obstacle_manager.ui', self)
        
        self.add_button.clicked.connect(self.add_obstacle)
        self.remove_button.clicked.connect(self.remove_obstacle)
        self.close_button.clicked.connect(self.close_window)

        self.refresh()

    def refresh(self):
        self.obstacle_list.clear()
        for idx in range(0,len(self.dynamic_obstacles.sprites)):
            self.obstacle_list.addItem(f'{self.dynamic_obstacles.sprites[idx].name}')

        self.obstacle_count.setText(f'Num Obstacles: {len(self.dynamic_obstacles.sprites)}')

    def add_obstacle(self):
        x = float(self.x_pose.value())
        y = float(self.y_pose.value())

        for idx in range(0,int(self.obs_qty.value())):
            self.dynamic_obstacles.ball(x,y)
        
        self.refresh()

    def remove_obstacle(self):
        self.dynamic_obstacles.remove_ball(idx=self.obstacle_list.currentRow())
        self.refresh()

    def close_window(self):
        self.close()

    