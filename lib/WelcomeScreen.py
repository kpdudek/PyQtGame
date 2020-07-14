#!/usr/bin/env python3

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtSvg, uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random, sys, os, pwd, math

from Utils import *
from PaintUtils import *
from Widgets import *


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
        self.main_title.setMinimumHeight(250)
        self.layout.addWidget(self.main_title,2)

        ######################################################
        # Game Creator
        ######################################################
        self.layout.addWidget(Divider('Create New Game',top_spacer=False))

        self.game_name_form = FormEntry('Enter name',return_press = self.start_game)
        self.layout.addLayout(self.game_name_form.form)

        self.start_button = QPushButton('Create')
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        ######################################################
        # Game loading
        ######################################################
        self.layout.addWidget(Divider('Load Game'))

        # game load combo box sub layout
        self.game_load_layout = QHBoxLayout()

        self.game_load_label = QLabel('Saved Games:')
        self.game_load_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
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
        if not os.path.exists(f'{self.user_path}saves/'):
            try:
                os.makedirs(f'{self.user_path}saves/')
                log("Save folder didn't exist so one was created...")
            except:
                log('Could not make save game folder!',color='r')
                    
        self.file_names = os.listdir(f'{self.user_path}saves/')
    
    def start_game(self):
        if len(self.game_name_form.form_line_edit.text()) == 0:
            log('Game name cannot be empty!',color='r')
            size = self.size()
            pose = QRect(600,400,200,200)
            self.warning = WarningPrompt('Game name cannot be empty!',rect=pose)
            self.warning.show()
            return
        else:
            log(f'Creating game: {self.game_name_form.form_line_edit.text()}')
            self.create.emit(self.game_name_form.form_line_edit.text())

    def load_game(self):
        self.load_file_name = self.save_games.currentText()
        if self.load_file_name == '':
            size = self.size()
            pose = QRect(600,400,200,200)
            self.warning = WarningPrompt('There is no save game selected!',rect=pose)
            self.warning.show()
            return
            
        log(f'Loading game: {self.load_file_name}')
        self.load.emit(self.load_file_name)