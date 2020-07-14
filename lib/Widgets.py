#!/usr/bin/env python3

import os
import sys
import time
import datetime as dt
import pwd
from threading import Thread
import inspect

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
        self.form_line_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.form.addWidget(self.form_line_label,1)

        self.form_line_edit = QLineEdit()
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
        self.ok_button.clicked.connect(self.close_window)
        self.ok_button.setDefault(True)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
        self.show()

    def close_window(self):
        self.close()

class ControlButton(QPushButton,Colors,FilePaths):

    def __init__(self,text,fn = None, default = False):
        super().__init__()

        self.setText(text)
        self.setFixedSize(150,30)

        if fn:
            self.clicked.connect(fn)
        
        if default:
            self.setDefault(True)

    