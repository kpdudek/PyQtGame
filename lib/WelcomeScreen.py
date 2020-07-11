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

    divider_color = '#ff9955'

    def __init__(self):
        super().__init__()
        # Set main widget as main windows central widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)

        self.main_title = QtSvg.QSvgWidget(f'{self.user_path}graphics/title_banner.svg')
        self.layout.addWidget(self.main_title)

        self.divider = QLabel()
        self.divider.setStyleSheet(f"background-color: {self.divider_color}")
        self.divider.setFixedHeight(3)
        self.layout.addWidget(self.divider)

        ######################################################
        # Game Creator
        self.new_label = QLabel('Create a New Game:')
        self.new_label.setStyleSheet(f"font:bold italic 24px")
        self.layout.addWidget(self.new_label)

        # Game name sub layout
        self.game_name_layout = QHBoxLayout()
        
        self.game_name_label = QLabel('Enter name:')
        self.game_name_layout.addWidget(self.game_name_label,1)

        self.game_name = QLineEdit()
        # self.game_name.setText('Enter game name')
        self.game_name_layout.addWidget(self.game_name,3)

        self.layout.addLayout(self.game_name_layout)

        self.start_button = QPushButton('Create')
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)
        ######################################################

        self.layout.addStretch()
        self.layout.addWidget(self.divider)
        self.layout.addStretch()

        ######################################################
        # Game loading
        self.load_label = QLabel('Load a Game:')
        self.load_label.setStyleSheet(f"font:bold italic 24px")
        self.layout.addWidget(self.load_label)

        # game load combo box sub layout
        self.game_load_layout = QHBoxLayout()

        self.game_load_label = QLabel('Saved Games:')
        self.game_load_layout.addWidget(self.game_load_label,1)

        self.save_games = QComboBox()
        self.find_save_files()
        self.save_games.addItems(self.file_names)
        self.game_load_layout.addWidget(self.save_games,3)

        self.layout.addLayout(self.game_load_layout)

        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load_game)
        self.layout.addWidget(self.load_button)

    def find_save_files(self):
        # print(self.user_path)
        self.file_names = os.listdir(f'{self.user_path}saves/')
    
    def start_game(self):
        if len(self.game_name.text()) == 0:
            log('Game name cannot be empty!',color='r')
            return
        else:
            log(f'Creating game: {self.game_name.text()}')
            self.create.emit(self.game_name.text())

    def load_game(self):
        self.load_file_name = self.save_games.currentText()
        self.load.emit(self.load_file_name)