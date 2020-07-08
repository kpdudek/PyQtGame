#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math

from Utils import *
from PaintUtils import *


class WelcomeScreen(QWidget,FilePaths):
    create = pyqtSignal(str)
    load = pyqtSignal(str)

    save_files = None

    def __init__(self):
        super().__init__()
        # Set main widget as main windows central widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)

        self.main_title = QtSvg.QSvgWidget(f'{self.user_path}graphics/title_banner.svg')
        self.layout.addWidget(self.main_title)

        self.new_label = QLabel('Create a New Game')
        self.layout.addWidget(self.new_label)

        self.game_name = QLineEdit()
        self.game_name.setText('Enter game name')
        self.layout.addWidget(self.game_name)

        self.start_button = QPushButton('Create')
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        self.layout.addStretch()

        self.load_label = QLabel('Load a Game')
        self.layout.addWidget(self.load_label)

        self.save_games = QComboBox()
        self.find_save_files()
        self.save_games.addItems(self.file_names)
        self.layout.addWidget(self.save_games)

        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load_game)
        self.layout.addWidget(self.load_button)

    def find_save_files(self):
        print(self.user_path)
        self.file_names = os.listdir(f'{self.user_path}saves/')
    
    def start_game(self):
        self.create.emit(self.game_name.text())

    def load_game(self):
        self.load_file_name = self.save_games.currentText()
        self.load.emit(self.load_file_name)